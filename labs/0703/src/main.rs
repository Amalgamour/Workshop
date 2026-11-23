mod sample;
mod store;

use sample::{PAGE_COUNT, Page, SEED};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::Path;
use std::time::{Duration, Instant};
use store::{Kind, Result, Store};
use tempfile::TempDir;

const ROUNDS: usize = 7;
const ONE_READS_PER_ROUND: usize = 21;

fn scratch() -> Result<TempDir> {
    let target = Path::new(env!("CARGO_MANIFEST_DIR")).join("target");
    fs::create_dir_all(&target)?;
    Ok(tempfile::Builder::new()
        .prefix("seq-storage-")
        .tempdir_in(target)?)
}

#[derive(Default)]
struct Measurements {
    write: Vec<Duration>,
    update: Vec<Duration>,
    read_all: Vec<Duration>,
    read_one: Vec<Duration>,
    size: Vec<u64>,
}

fn timed<T>(operation: impl FnOnce() -> Result<T>) -> Result<(T, Duration)> {
    let start = Instant::now();
    let result = operation()?;
    Ok((result, start.elapsed()))
}

fn median<T: Copy + Ord>(mut values: Vec<T>) -> T {
    values.sort_unstable();
    values[values.len() / 2]
}

fn measure(
    kind: Kind,
    root: &Path,
    pages: &[Page],
    latest: &Page,
    expected: &[&Page],
    measurements: &mut Measurements,
) -> Result<()> {
    let (mut store, elapsed) = timed(|| kind.write(root, pages))?;
    measurements.write.push(elapsed);
    let ((), elapsed) = timed(|| store.update(latest))?;
    measurements.update.push(elapsed);
    measurements.size.push(store.size()?);

    let (read, elapsed) = timed(|| store.read_all())?;
    measurements.read_all.push(elapsed);
    assert!(read.iter().eq(expected.iter().copied()), "{} latest pages", kind.name());

    for _ in 0..ONE_READS_PER_ROUND {
        let (read, elapsed) = timed(|| store.read_one(&latest.id))?;
        measurements.read_one.push(elapsed);
        assert_eq!(&read, latest, "{} latest version", kind.name());
    }
    Ok(())
}

// A SHA-256 of the page ID and its ordered, length-prefixed versions. The
// benchmark retains the same expected digest outside all three stores.
fn history_sha(id: &str, versions: &[&str]) -> String {
    let mut sha = Sha256::new();
    sha.update((id.len() as u64).to_be_bytes());
    sha.update(id);
    sha.update((versions.len() as u64).to_be_bytes());
    for version in versions {
        sha.update((version.len() as u64).to_be_bytes());
        sha.update(version);
    }
    format!("{:x}", sha.finalize())
}

fn edited_body(page: &Page, version: u8) -> String {
    let probe = page.probe(version);
    page.text.replacen(&probe, &probe.replacen('S', "s", 1), 1)
}

#[derive(Debug, PartialEq, Eq)]
struct Audit {
    history_matches: bool,
    with_served_page_matches: bool,
}

impl Audit {
    const CLEAN: Self = Self { history_matches: true, with_served_page_matches: true };

    fn check(store: &Store, id: &str, outside_sha: &str) -> Result<Self> {
        let served = store.read_one(id)?;
        let history = store.history(id)?;
        let mut versions = history.iter().map(String::as_str).collect::<Vec<_>>();
        let history_matches = history_sha(id, &versions) == outside_sha;
        let latest = versions.last_mut().ok_or("missing stored history")?;
        *latest = &served.text;
        let with_served_page_matches = history_sha(id, &versions) == outside_sha;
        Ok(Self { history_matches, with_served_page_matches })
    }
}

fn tamper_trials(kind: Kind, pages: &[Page], original: &Page, latest: &Page) -> Result<()> {
    let id = &original.id;
    let outside_sha = history_sha(id, &[&original.text, &latest.text]);
    let root = scratch()?;
    let mut store = kind.write(root.path(), pages)?;
    store.update(latest)?;
    assert_eq!(Audit::check(&store, id, &outside_sha)?, Audit::CLEAN);
    store.verify_native(id)?;
    store.flip_current_byte(latest)?;
    assert_eq!(store.read_one(id)?.text, edited_body(latest, 2));
    let native = match store.verify_native(id) {
        Ok(()) => "ok".to_owned(),
        Err(error) => error.to_string(),
    };
    let audit = Audit::check(&store, id, &outside_sha)?;
    assert!(!audit.with_served_page_matches);
    println!(
        "{} latest byte: native={native}, history matches={}, with served page matches={}",
        kind.name(), audit.history_matches, audit.with_served_page_matches,
    );
    root.close()?;

    let root = scratch()?;
    let mut store = kind.write(root.path(), pages)?;
    store.update(latest)?;
    assert_eq!(Audit::check(&store, id, &outside_sha)?, Audit::CLEAN);
    let edited = Page {
        id: id.clone(),
        text: edited_body(original, 1),
    };
    store.replace_first_version(&edited, latest)?;
    assert_eq!(store.history(id)?, [edited.text, latest.text.clone()]);
    assert_eq!(&store.read_one(id)?, latest);
    store.verify_native(id)?;
    let audit = Audit::check(&store, id, &outside_sha)?;
    assert!(!audit.history_matches && !audit.with_served_page_matches);
    println!(
        "{} older version rewritten: native=ok, latest unchanged, history matches={}",
        kind.name(), audit.history_matches,
    );
    root.close()?;
    Ok(())
}

fn main() -> Result<()> {
    let pages = sample::pages(PAGE_COUNT);
    let total: usize = pages.iter().map(|page| page.text.len()).sum();
    let smallest = pages.iter().map(|page| page.text.len()).min().unwrap();
    let largest = pages.iter().map(|page| page.text.len()).max().unwrap();
    let index = pages.len() / 2;
    let original = &pages[index];
    let latest = original.revised();
    let mut expected: Vec<&Page> = pages.iter().collect();
    expected[index] = &latest;
    let sqlite = rusqlite::version();
    println!(
        "{PAGE_COUNT} pages, seed {SEED:#010x}, {total} payload bytes ({smallest}..={largest} per page)"
    );
    println!(
        "{ROUNDS} rounds, {ONE_READS_PER_ROUND} latest reads of {} per store per round, SQLite {sqlite}",
        latest.id
    );
    println!("all writes: OS-buffered, no explicit durable flush");

    let mut stats: [Measurements; 3] = std::array::from_fn(|_| Measurements::default());
    for round in 0..ROUNDS {
        let root = scratch()?;
        for offset in 0..Kind::ALL.len() {
            let index = (round + offset) % Kind::ALL.len();
            measure(Kind::ALL[index], root.path(), &pages, &latest, &expected, &mut stats[index])?;
        }
        root.close()?;
    }
    println!("store             write ms  update ms  read all ms  read one us  stored bytes");
    for (kind, stats) in Kind::ALL.into_iter().zip(stats) {
        println!(
            "{:<16}{:>10.3}{:>11.3}{:>13.3}{:>13.3}{:>14}",
            kind.name(),
            median(stats.write).as_secs_f64() * 1e3,
            median(stats.update).as_secs_f64() * 1e3,
            median(stats.read_all).as_secs_f64() * 1e3,
            median(stats.read_one).as_secs_f64() * 1e6,
            median(stats.size),
        );
    }

    for kind in Kind::ALL {
        tamper_trials(kind, &pages, original, &latest)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::{File, OpenOptions};
    use std::io::BufReader;
    use store::{record_end, verify_chain};

    fn round_trip(kind: Kind) -> Result<()> {
        let root = scratch()?;
        let mut pages = sample::pages(11);
        let revised = pages[5].revised();
        let mut store = kind.write(root.path(), &pages)?;
        assert_eq!(store.read_all()?, pages);
        assert_eq!(store.read_one(&revised.id)?, pages[5]);
        assert_ne!(revised, pages[5]);
        store.update(&revised)?;
        assert_eq!(
            store.history(&revised.id)?,
            [pages[5].text.clone(), revised.text.clone()]
        );
        pages[5] = revised;
        assert_eq!(store.read_all()?, pages);
        for page in &pages {
            assert_eq!(store.read_one(&page.id)?, *page);
        }
        root.close()?;
        Ok(())
    }

    #[test]
    fn git_round_trip_and_update() -> Result<()> {
        round_trip(Kind::Git)
    }

    #[test]
    fn chain_round_trip_and_update() -> Result<()> {
        round_trip(Kind::Chain)
    }

    #[test]
    fn sqlite_round_trip_and_update() -> Result<()> {
        round_trip(Kind::Sqlite)
    }

    #[test]
    fn same_tamper_trials_against_each_store() -> Result<()> {
        let pages = sample::pages(11);
        let original = &pages[5];
        for kind in Kind::ALL {
            tamper_trials(kind, &pages, original, &original.revised())?;
        }
        Ok(())
    }

    #[test]
    fn chain_names_the_edited_record() -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(3);
        let latest = pages[1].revised();
        let mut store = Kind::Chain.write(root.path(), &pages)?;
        store.update(&latest)?;
        let Store::Chain { path, .. } = &store else { unreachable!() };
        verify_chain(path)?;
        let before = fs::read(path)?;
        store.flip_current_byte(&latest)?;
        let after = fs::read(path)?;
        assert_eq!(before.len(), after.len());
        assert_eq!(before.iter().zip(&after).filter(|(a, b)| a != b).count(), 1);
        assert_eq!(
            verify_chain(path).unwrap_err().to_string(),
            format!("record 4 ({}): content hash mismatch", latest.id)
        );
        root.close()?;
        Ok(())
    }

    #[test]
    fn chain_refuses_a_truncated_tail() -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(3);
        let Store::Chain { path, .. } = Kind::Chain.write(root.path(), &pages)? else { unreachable!() };
        verify_chain(&path)?;
        let file = OpenOptions::new().write(true).open(&path)?;
        file.set_len(file.metadata()?.len() - 1)?;
        drop(file);
        assert_eq!(
            verify_chain(&path).unwrap_err().to_string(),
            format!("{}: incomplete or invalid record hash", pages[2].id)
        );
        root.close()?;
        Ok(())
    }

    #[test]
    fn chain_refuses_a_removed_middle_record() -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(3);
        let Store::Chain { path, .. } = Kind::Chain.write(root.path(), &pages)? else { unreachable!() };
        verify_chain(&path)?;
        let mut reader = BufReader::new(File::open(&path)?);
        let start = record_end(&mut reader)? as usize;
        let end = record_end(&mut reader)? as usize;
        drop(reader);
        let mut bytes = fs::read(&path)?;
        bytes.drain(start..end);
        fs::write(&path, bytes)?;
        assert_eq!(
            verify_chain(&path).unwrap_err().to_string(),
            format!("record 2 ({}): previous hash mismatch", pages[2].id)
        );
        root.close()?;
        Ok(())
    }
}
