mod sample;
mod store;

use sample::{PAGE_COUNT, Page, SEED};
use std::fs;
use std::path::Path;
use std::time::{Duration, Instant};
use store::{Kind, Result};
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
    single: &Page,
    measurements: &mut Measurements,
) -> Result<()> {
    let (store, elapsed) = timed(|| kind.write(root, pages))?;
    measurements.write.push(elapsed);
    measurements.size.push(store.size()?);

    let (read, elapsed) = timed(|| store.read_all())?;
    measurements.read_all.push(elapsed);
    assert_eq!(read, pages, "{} full read", kind.name());

    for _ in 0..ONE_READS_PER_ROUND {
        let (read, elapsed) = timed(|| store.read_one(&single.id))?;
        measurements.read_one.push(elapsed);
        assert_eq!(&read, single, "{} single read", kind.name());
    }
    Ok(())
}

fn main() -> Result<()> {
    let pages = sample::pages(PAGE_COUNT);
    let total: usize = pages.iter().map(|page| page.text.len()).sum();
    let smallest = pages.iter().map(|page| page.text.len()).min().unwrap();
    let largest = pages.iter().map(|page| page.text.len()).max().unwrap();
    let single = &pages[pages.len() / 2];
    let sqlite = rusqlite::version();
    println!(
        "{PAGE_COUNT} pages, seed {SEED:#010x}, {total} payload bytes ({smallest}..={largest} per page)"
    );
    println!(
        "{ROUNDS} rounds, {ONE_READS_PER_ROUND} single reads of {} per store per round, SQLite {sqlite}",
        single.id
    );

    let mut stats: [Measurements; 3] = std::array::from_fn(|_| Measurements::default());
    for round in 0..ROUNDS {
        let root = scratch()?;
        for offset in 0..Kind::ALL.len() {
            let index = (round + offset) % Kind::ALL.len();
            measure(Kind::ALL[index], root.path(), &pages, single, &mut stats[index])?;
        }
        root.close()?;
    }
    println!("store             write ms  read all ms  read one us  stored bytes");
    for (kind, stats) in Kind::ALL.into_iter().zip(stats) {
        println!(
            "{:<16}{:>10.3}{:>13.3}{:>13.3}{:>14}",
            kind.name(),
            median(stats.write).as_secs_f64() * 1e3,
            median(stats.read_all).as_secs_f64() * 1e3,
            median(stats.read_one).as_secs_f64() * 1e6,
            median(stats.size),
        );
    }

    // Use a separate set of stores so corruption never enters the timings.
    let root = scratch()?;
    for kind in Kind::ALL {
        let store = kind.write(root.path(), &pages)?;
        println!("{} one-byte change: {}", kind.name(), store.tamper_trial(single)?);
    }
    root.close()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use store::{Store, flip_probe, verify_chain};

    fn round_trip(kind: Kind) -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(11);
        let store = kind.write(root.path(), &pages)?;
        assert_eq!(store.read_all()?, pages);
        for page in &pages {
            assert_eq!(store.read_one(&page.id)?, *page);
        }
        root.close()?;
        Ok(())
    }

    #[test]
    fn git_round_trip() -> Result<()> {
        round_trip(Kind::Git)
    }

    #[test]
    fn chain_round_trip() -> Result<()> {
        round_trip(Kind::Chain)
    }

    #[test]
    fn sqlite_round_trip() -> Result<()> {
        round_trip(Kind::Sqlite)
    }

    #[test]
    fn chain_detects_one_changed_byte() -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(3);
        let Store::Chain { path, head } = Kind::Chain.write(root.path(), &pages)? else {
            unreachable!();
        };
        verify_chain(&path, &head)?;
        let before = fs::read(&path)?;
        flip_probe(&path, &pages[1].probe())?;
        let after = fs::read(&path)?;
        assert_eq!(before.len(), after.len());
        assert_eq!(before.iter().zip(&after).filter(|(a, b)| a != b).count(), 1);
        assert_eq!(
            verify_chain(&path, &head).unwrap_err().to_string(),
            format!("previous hash mismatch before {}", pages[2].id)
        );
        root.close()?;
        Ok(())
    }

    #[test]
    fn trusted_head_detects_a_changed_last_record() -> Result<()> {
        let root = scratch()?;
        let pages = sample::pages(2);
        let Store::Chain { path, head } = Kind::Chain.write(root.path(), &pages)? else {
            unreachable!();
        };
        verify_chain(&path, &head)?;
        flip_probe(&path, &pages[1].probe())?;
        assert_eq!(
            verify_chain(&path, &head).unwrap_err().to_string(),
            "trusted head hash mismatch"
        );
        root.close()?;
        Ok(())
    }
}
