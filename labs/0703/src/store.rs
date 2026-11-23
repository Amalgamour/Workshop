use crate::sample::Page;
use rusqlite::{Connection, OpenFlags, params};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::error::Error;
use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, BufWriter, Read, Seek, SeekFrom, Write};
use std::path::{Path, PathBuf};
use std::process::Command;

pub type Result<T> = std::result::Result<T, Box<dyn Error>>;

#[derive(Clone, Copy)]
pub enum Kind {
    Git,
    Chain,
    Sqlite,
}

impl Kind {
    pub const ALL: [Self; 3] = [Self::Git, Self::Chain, Self::Sqlite];

    pub fn name(self) -> &'static str {
        match self {
            Self::Git => "text+git",
            Self::Chain => "hash-chain",
            Self::Sqlite => "sqlite",
        }
    }

    pub fn write(self, root: &Path, pages: &[Page]) -> Result<Store> {
        match self {
            Self::Git => {
                let repo = root.join("git");
                fs::create_dir(&repo)?;
                git(&repo, &["init", "--quiet", "--template=", "--initial-branch=trial"])?;
                commit_pages(&repo, pages)?;
                Ok(Store::Git(repo))
            }
            Self::Chain => {
                let path = root.join("pages.log");
                let file = OpenOptions::new().create_new(true).append(true).open(&path)?;
                let head = write_records(file, pages, GENESIS)?;
                Ok(Store::Chain { path, head })
            }
            Self::Sqlite => {
                let path = root.join("pages.sqlite");
                write_sqlite(&path, pages, true)?;
                Ok(Store::Sqlite(path))
            }
        }
    }
}

pub enum Store {
    Git(PathBuf),
    Chain { path: PathBuf, head: String },
    Sqlite(PathBuf),
}

impl Store {
    pub fn update(&mut self, page: &Page) -> Result<()> {
        let pages = std::slice::from_ref(page);
        match self {
            Self::Git(repo) => commit_pages(repo, pages),
            Self::Chain { path, head } => {
                let file = OpenOptions::new().append(true).open(path)?;
                *head = write_records(file, pages, head)?;
                Ok(())
            }
            Self::Sqlite(path) => write_sqlite(path, pages, false),
        }
    }

    pub fn read_all(&self) -> Result<Vec<Page>> {
        match self {
            Self::Git(repo) => {
                let mut files = fs::read_dir(repo)?
                    .collect::<std::io::Result<Vec<_>>>()?
                    .into_iter()
                    .map(|entry| entry.path())
                    .filter(|path| path.extension().is_some_and(|ext| ext == "seq"))
                    .collect::<Vec<_>>();
                files.sort_unstable();
                files.iter().map(|path| read_text(path)).collect()
            }
            Self::Chain { path, .. } => {
                let mut log = BufReader::new(File::open(path)?);
                let mut latest = BTreeMap::new();
                while let Some(record) = read_record(&mut log)? {
                    latest.insert(record.page.id.clone(), record.page);
                }
                Ok(latest.into_values().collect())
            }
            Self::Sqlite(path) => {
                let connection = open_sqlite(path)?;
                let mut statement = connection.prepare(
                    "SELECT id, body FROM revisions r
                     WHERE version = (SELECT MAX(version) FROM revisions WHERE id = r.id)
                     ORDER BY id",
                )?;
                let rows = statement.query_map([], |row| {
                    Ok(Page { id: row.get(0)?, text: row.get(1)? })
                })?;
                Ok(rows.collect::<rusqlite::Result<Vec<_>>>()?)
            }
        }
    }

    pub fn read_one(&self, id: &str) -> Result<Page> {
        let text = match self {
            Self::Git(repo) => fs::read_to_string(repo.join(format!("{id}.seq")))?,
            Self::Chain { path, .. } => {
                let mut log = BufReader::new(File::open(path)?);
                let mut latest = None;
                while let Some(record) = read_record(&mut log)? {
                    if record.page.id == id {
                        latest = Some(record.page.text);
                    }
                }
                latest.ok_or_else(|| format!("page {id} missing from log"))?
            }
            Self::Sqlite(path) => open_sqlite(path)?.query_row(
                "SELECT body FROM revisions WHERE id = ? ORDER BY version DESC LIMIT 1",
                [id],
                |row| row.get(0),
            )?,
        };
        Ok(Page { id: id.to_owned(), text })
    }

    pub fn history(&self, id: &str) -> Result<Vec<String>> {
        match self {
            Self::Git(repo) => {
                let file = format!("{id}.seq");
                let commits = git(
                    repo,
                    &["log", "--first-parent", "--reverse", "--format=%H", "HEAD", "--", &file],
                )?;
                commits.lines().map(|commit| git_blob(repo, commit, &file)).collect()
            }
            Self::Chain { path, .. } => {
                let mut log = BufReader::new(File::open(path)?);
                let mut versions = Vec::new();
                while let Some(record) = read_record(&mut log)? {
                    if record.page.id == id {
                        versions.push(record.page.text);
                    }
                }
                Ok(versions)
            }
            Self::Sqlite(path) => {
                let connection = open_sqlite(path)?;
                let mut statement =
                    connection.prepare("SELECT body FROM revisions WHERE id = ? ORDER BY version")?;
                let rows = statement.query_map([id], |row| row.get(0))?;
                Ok(rows.collect::<rusqlite::Result<Vec<_>>>()?)
            }
        }
    }

    pub fn size(&self) -> Result<u64> {
        match self {
            Self::Git(repo) => directory_bytes(repo),
            Self::Chain { path, .. } | Self::Sqlite(path) => Ok(fs::metadata(path)?.len()),
        }
    }

    pub fn verify_native(&self, id: &str) -> Result<()> {
        match self {
            Self::Git(repo) => {
                git(repo, &["fsck", "--full", "--no-reflogs"])?;
                let file = format!("{id}.seq");
                if fs::read_to_string(repo.join(&file))? != git_blob(repo, "HEAD", &file)? {
                    return Err(format!("working file {file} disagrees with HEAD").into());
                }
            }
            Self::Chain { path, .. } => verify_chain(path)?,
            Self::Sqlite(path) => {
                let result: String = open_sqlite(path)?
                    .query_row("PRAGMA integrity_check", [], |row| row.get(0))?;
                if result != "ok" {
                    return Err(result.into());
                }
            }
        }
        Ok(())
    }

    pub fn flip_current_byte(&self, page: &Page) -> Result<()> {
        let path = match self {
            Self::Git(repo) => repo.join(page.filename()),
            Self::Chain { path, .. } | Self::Sqlite(path) => path.clone(),
        };
        flip_probe(&path, &page.probe(2))
    }

    // Exercise self-consistent replacement solely in stores created under the lab scratch root.
    pub fn replace_first_version(&mut self, replacement: &Page, latest: &Page) -> Result<()> {
        match self {
            Self::Git(repo) => replace_git_history(repo, replacement, latest),
            Self::Chain { path, head } => {
                let mut log = BufReader::new(File::open(&*path)?);
                let mut pages = Vec::new();
                while let Some(record) = read_record(&mut log)? {
                    pages.push(record.page);
                }
                drop(log);
                let first = pages.iter_mut().find(|page| page.id == replacement.id)
                    .ok_or("missing first log version")?;
                first.text.clone_from(&replacement.text);
                let file = OpenOptions::new().write(true).truncate(true).open(path)?;
                *head = write_records(file, &pages, GENESIS)?;
                Ok(())
            }
            Self::Sqlite(path) => {
                let connection = sqlite_writer(path)?;
                if connection.execute(
                    "UPDATE revisions SET body = ? WHERE id = ? AND version = 1",
                    params![replacement.text, replacement.id],
                )? != 1 {
                    return Err("missing first SQLite version".into());
                }
                Ok(())
            }
        }
    }
}

fn run_git(repo: &Path, args: &[&str]) -> Result<String> {
    let output = Command::new("git")
        .current_dir(repo)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .env_remove("GIT_INDEX_FILE")
        .env_remove("GIT_COMMON_DIR")
        .env_remove("GIT_OBJECT_DIRECTORY")
        .env_remove("GIT_ALTERNATE_OBJECT_DIRECTORIES")
        .env_remove("GIT_CONFIG_COUNT")
        .env_remove("GIT_CONFIG_PARAMETERS")
        .env("GIT_CONFIG_NOSYSTEM", "1")
        .env("GIT_CONFIG_GLOBAL", repo.join("unused-global-config"))
        .args([
            "-c", "core.autocrlf=false",
            "-c", "core.fsync=none",
            "-c", "commit.gpgsign=false",
            "-c", "gc.auto=0",
            "-c", "user.name=Storage Lab",
            "-c", "user.email=storage-lab@example.invalid",
        ])
        .args(args)
        .output()?;
    if !output.status.success() {
        return Err(format!("git {} failed: {}", args[0], String::from_utf8_lossy(&output.stderr)).into());
    }
    Ok(String::from_utf8(output.stdout)?)
}

fn git(repo: &Path, args: &[&str]) -> Result<String> {
    Ok(run_git(repo, args)?.trim().to_owned())
}

fn git_blob(repo: &Path, commit: &str, file: &str) -> Result<String> {
    run_git(repo, &["cat-file", "blob", &format!("{commit}:{file}")])
}

fn commit_pages(repo: &Path, pages: &[Page]) -> Result<()> {
    for page in pages {
        fs::write(repo.join(page.filename()), &page.text)?;
    }
    // Each add names specific files and stays under Windows' command-line length limit.
    for batch in pages.chunks(200) {
        let files = batch.iter().map(Page::filename).collect::<Vec<_>>();
        let mut args = vec!["add", "--"];
        args.extend(files.iter().map(String::as_str));
        git(repo, &args)?;
    }
    git(repo, &["commit", "--quiet", "-m", "Store sample pages"])?;
    Ok(())
}

fn replace_git_history(repo: &Path, replacement: &Page, latest: &Page) -> Result<()> {
    let name = replacement.filename();
    let tip = git(repo, &["rev-parse", "HEAD"])?;
    let tip_tree = git(repo, &["rev-parse", "HEAD^{tree}"])?;
    let first_tree = git(repo, &["rev-parse", "HEAD^1^{tree}"])?;

    git(repo, &["read-tree", &first_tree])?;
    fs::write(repo.join(&name), &replacement.text)?;
    git(repo, &["add", "--", &name])?;
    let tree = git(repo, &["write-tree"])?;
    let first = git(repo, &["commit-tree", &tree, "-m", "Trial replacement of first version"])?;
    let new_tip = git(repo, &["commit-tree", &tip_tree, "-p", &first, "-m", "Trial replacement tip"])?;

    fs::write(repo.join(&name), &latest.text)?;
    git(repo, &["read-tree", &tip_tree])?;
    git(repo, &["update-ref", "HEAD", &new_tip, &tip])?;
    Ok(())
}

fn read_text(path: &Path) -> Result<Page> {
    let id = path.file_stem().and_then(|stem| stem.to_str())
        .ok_or("invalid page filename")?.to_owned();
    Ok(Page { id, text: fs::read_to_string(path)? })
}

fn directory_bytes(dir: &Path) -> Result<u64> {
    let mut bytes = 0;
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        bytes += if entry.file_type()?.is_dir() {
            directory_bytes(&entry.path())?
        } else {
            entry.metadata()?.len()
        };
    }
    Ok(bytes)
}

const GENESIS: &str = "0000000000000000000000000000000000000000000000000000000000000000";

struct Record {
    header: String,
    previous: String,
    page: Page,
    hash: String,
}

fn record_hash(header: &str, body: &str) -> String {
    let mut sha = Sha256::new();
    sha.update(header);
    sha.update(body);
    format!("{:x}", sha.finalize())
}

fn write_records(file: File, pages: &[Page], previous: &str) -> Result<String> {
    let mut log = BufWriter::new(file);
    let mut previous = previous.to_owned();
    for page in pages {
        let header = format!("{} {previous} {}\n", page.id, page.text.len());
        let hash = record_hash(&header, &page.text);
        log.write_all(header.as_bytes())?;
        log.write_all(page.text.as_bytes())?;
        writeln!(log, "{hash}")?;
        previous = hash;
    }
    log.flush()?;
    Ok(previous)
}

fn hash_field(value: &str) -> bool {
    value.len() == 64 && value.bytes().all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}

fn read_record(log: &mut BufReader<File>) -> Result<Option<Record>> {
    let mut header = String::new();
    if log.read_line(&mut header)? == 0 {
        return Ok(None);
    }
    let mut fields = header.strip_suffix('\n').ok_or("incomplete record header")?.split(' ');
    let id = fields.next().ok_or("missing page ID")?.to_owned();
    let previous = fields.next().ok_or("missing previous hash")?.to_owned();
    let length: u64 = fields.next().ok_or("missing body length")?.parse()?;
    if id.is_empty() || !hash_field(&previous) || fields.next().is_some() {
        return Err(format!("invalid record header for {id}").into());
    }
    let mut text = String::new();
    if log.take(length).read_to_string(&mut text)? as u64 != length {
        return Err(format!("{id}: incomplete record body").into());
    }
    let mut hash = String::new();
    log.read_line(&mut hash)?;
    let hash = hash.strip_suffix('\n').filter(|hash| hash_field(hash))
        .ok_or_else(|| format!("{id}: incomplete or invalid record hash"))?.to_owned();
    Ok(Some(Record { header, previous, page: Page { id, text }, hash }))
}

pub fn verify_chain(path: &Path) -> Result<()> {
    let mut log = BufReader::new(File::open(path)?);
    let mut previous = GENESIS.to_owned();
    let mut number = 0;
    while let Some(record) = read_record(&mut log)? {
        number += 1;
        if record_hash(&record.header, &record.page.text) != record.hash {
            return Err(format!("record {number} ({}): content hash mismatch", record.page.id).into());
        }
        if record.previous != previous {
            return Err(format!("record {number} ({}): previous hash mismatch", record.page.id).into());
        }
        previous = record.hash;
    }
    Ok(())
}

#[cfg(test)]
pub fn record_end(log: &mut BufReader<File>) -> Result<u64> {
    read_record(log)?.ok_or("expected one log record")?;
    Ok(log.stream_position()?)
}

fn sqlite_writer(path: &Path) -> Result<Connection> {
    let connection = Connection::open(path)?;
    connection.execute_batch("PRAGMA journal_mode = DELETE; PRAGMA synchronous = OFF;")?;
    Ok(connection)
}

fn write_sqlite(path: &Path, pages: &[Page], create: bool) -> Result<()> {
    let mut connection = sqlite_writer(path)?;
    let transaction = connection.transaction()?;
    if create {
        transaction.execute(
            "CREATE TABLE revisions (
                id TEXT NOT NULL, version INTEGER NOT NULL, body TEXT NOT NULL,
                PRIMARY KEY (id, version)
             ) WITHOUT ROWID",
            [],
        )?;
    }
    {
        let mut insert = transaction.prepare(
            "INSERT INTO revisions (id, version, body)
             SELECT ?1, COALESCE(MAX(version), 0) + 1, ?2 FROM revisions WHERE id = ?1",
        )?;
        for page in pages {
            insert.execute(params![page.id, page.text])?;
        }
    }
    transaction.commit()?;
    Ok(())
}

fn open_sqlite(path: &Path) -> Result<Connection> {
    Ok(Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)?)
}

fn flip_probe(path: &Path, probe: &str) -> Result<()> {
    let bytes = fs::read(path)?;
    let mut offsets = bytes.windows(probe.len()).enumerate()
        .filter_map(|(offset, window)| (window == probe.as_bytes()).then_some(offset));
    let offset = offsets.next().ok_or("probe missing from store")?;
    if offsets.next().is_some() {
        return Err("probe appears more than once".into());
    }

    let mut file = OpenOptions::new().write(true).open(path)?;
    file.seek(SeekFrom::Start(offset as u64))?;
    file.write_all(b"s")?;
    Ok(())
}
