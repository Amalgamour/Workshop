use crate::sample::Page;
use rusqlite::{Connection, OpenFlags, params};
use sha2::{Digest, Sha256};
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
                write_git(&repo, pages)?;
                Ok(Store::Git(repo))
            }
            Self::Chain => {
                let path = root.join("pages.log");
                let head = write_chain(&path, pages)?;
                Ok(Store::Chain { path, head })
            }
            Self::Sqlite => {
                let path = root.join("pages.sqlite");
                write_sqlite(&path, pages)?;
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
                let mut pages = Vec::new();
                while let Some(record) = read_record(&mut log)? {
                    pages.push(record.page);
                }
                Ok(pages)
            }
            Self::Sqlite(path) => {
                let connection = open_sqlite(path)?;
                let mut statement = connection.prepare("SELECT id, body FROM pages ORDER BY id")?;
                let rows = statement.query_map([], |row| {
                    Ok(Page {
                        id: row.get(0)?,
                        text: row.get(1)?,
                    })
                })?;
                Ok(rows.collect::<rusqlite::Result<Vec<_>>>()?)
            }
        }
    }

    pub fn read_one(&self, id: &str) -> Result<Page> {
        match self {
            Self::Git(repo) => read_text(&repo.join(format!("{id}.seq"))),
            Self::Chain { path, .. } => {
                let mut log = BufReader::new(File::open(path)?);
                while let Some(record) = read_record(&mut log)? {
                    if record.page.id == id {
                        return Ok(record.page);
                    }
                }
                Err(format!("page {id} missing from log").into())
            }
            Self::Sqlite(path) => {
                let connection = open_sqlite(path)?;
                let text =
                    connection.query_row("SELECT body FROM pages WHERE id = ?", [id], |row| {
                        row.get(0)
                    })?;
                Ok(Page {
                    id: id.to_owned(),
                    text,
                })
            }
        }
    }

    pub fn size(&self) -> Result<u64> {
        match self {
            Self::Git(repo) => directory_bytes(repo),
            Self::Chain { path, .. } | Self::Sqlite(path) => Ok(fs::metadata(path)?.len()),
        }
    }

    pub fn tamper_trial(&self, original: &Page) -> Result<String> {
        let probe = original.probe();
        match self {
            Self::Git(repo) => {
                let file = original.filename();
                let pinned = git(repo, &["rev-parse", &format!("HEAD:{file}")])?;
                let raw_hash = || git(repo, &["hash-object", "--no-filters", "--", &file]);
                if raw_hash()? != pinned {
                    return Err("clean file does not match the committed blob".into());
                }
                flip_probe(&repo.join(&file), &probe)?;
                let matched = raw_hash()? == pinned;
                Ok(format!("raw blob hash matches committed blob: {matched}"))
            }
            Self::Chain { path, head } => {
                verify_chain(path, head)?;
                flip_probe(path, &probe)?;
                match verify_chain(path, head) {
                    Ok(()) => Ok("chain verification passed".to_owned()),
                    Err(error) => Ok(error.to_string()),
                }
            }
            Self::Sqlite(path) => {
                flip_probe(path, &probe)?;
                let structural: String =
                    open_sqlite(path)?.query_row("PRAGMA integrity_check", [], |row| row.get(0))?;
                let matched = digest(b"", self.read_one(&original.id)?.text.as_bytes())
                    == digest(b"", original.text.as_bytes());
                Ok(format!(
                    "integrity_check: {structural}; payload SHA-256 matches baseline: {matched}"
                ))
            }
        }
    }
}

fn git(repo: &Path, args: &[&str]) -> Result<String> {
    let output = Command::new("git")
        .current_dir(repo)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .env_remove("GIT_INDEX_FILE")
        .env("GIT_CONFIG_NOSYSTEM", "1")
        .env("GIT_CONFIG_GLOBAL", repo.join("unused-global-config"))
        .args([
            "-c",
            "core.autocrlf=false",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "gc.auto=0",
            "-c",
            "user.name=Storage Lab",
            "-c",
            "user.email=storage-lab@example.invalid",
        ])
        .args(args)
        .output()?;
    if !output.status.success() {
        return Err(format!("git {} failed: {}", args[0], String::from_utf8_lossy(&output.stderr))
            .into());
    }
    Ok(String::from_utf8(output.stdout)?.trim().to_owned())
}

fn write_git(repo: &Path, pages: &[Page]) -> Result<()> {
    fs::create_dir(repo)?;
    git(repo, &["init", "--quiet", "--template="])?;
    for page in pages {
        fs::write(repo.join(page.filename()), &page.text)?;
    }
    // Windows limits the command-line length. Every add still names specific files.
    for batch in pages.chunks(200) {
        let files = batch.iter().map(Page::filename).collect::<Vec<_>>();
        let mut args = vec!["add", "--"];
        args.extend(files.iter().map(String::as_str));
        git(repo, &args)?;
    }
    git(repo, &["commit", "--quiet", "-m", "Store sample pages"])?;
    Ok(())
}

fn read_text(path: &Path) -> Result<Page> {
    let id = path
        .file_stem()
        .and_then(|stem| stem.to_str())
        .ok_or("invalid page filename")?
        .to_owned();
    Ok(Page {
        id,
        text: fs::read_to_string(path)?,
    })
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
}

fn digest(header: &[u8], body: &[u8]) -> String {
    let mut sha = Sha256::new();
    sha.update(header);
    sha.update(body);
    format!("{:x}", sha.finalize())
}

fn write_chain(path: &Path, pages: &[Page]) -> Result<String> {
    let file = OpenOptions::new().create_new(true).append(true).open(path)?;
    let mut log = BufWriter::new(file);
    let mut previous = GENESIS.to_owned();
    for page in pages {
        let header = format!("{} {previous} {}\n", page.id, page.text.len());
        log.write_all(header.as_bytes())?;
        log.write_all(page.text.as_bytes())?;
        previous = digest(header.as_bytes(), page.text.as_bytes());
    }
    log.flush()?;
    Ok(previous)
}

fn read_record(log: &mut BufReader<File>) -> Result<Option<Record>> {
    let mut header = String::new();
    if log.read_line(&mut header)? == 0 {
        return Ok(None);
    }
    let mut fields = header
        .strip_suffix('\n')
        .ok_or("incomplete record header")?
        .split(' ');
    let id = fields.next().ok_or("missing page ID")?.to_owned();
    let previous = fields.next().ok_or("missing previous hash")?.to_owned();
    let length: u64 = fields.next().ok_or("missing body length")?.parse()?;
    if id.is_empty() || previous.len() != GENESIS.len() || fields.next().is_some() {
        return Err("invalid record header".into());
    }
    let mut text = String::new();
    if log.take(length).read_to_string(&mut text)? as u64 != length {
        return Err("incomplete record body".into());
    }
    Ok(Some(Record {
        header,
        previous,
        page: Page { id, text },
    }))
}

pub fn verify_chain(path: &Path, expected_head: &str) -> Result<()> {
    let mut log = BufReader::new(File::open(path)?);
    let mut previous = GENESIS.to_owned();
    while let Some(record) = read_record(&mut log)? {
        if record.previous != previous {
            return Err(format!("previous hash mismatch before {}", record.page.id).into());
        }
        previous = digest(record.header.as_bytes(), record.page.text.as_bytes());
    }
    if previous != expected_head {
        return Err("trusted head hash mismatch".into());
    }
    Ok(())
}

fn write_sqlite(path: &Path, pages: &[Page]) -> Result<()> {
    let mut connection = Connection::open(path)?;
    connection.execute_batch("PRAGMA journal_mode = DELETE; PRAGMA synchronous = FULL;")?;
    let transaction = connection.transaction()?;
    transaction.execute("CREATE TABLE pages (id TEXT PRIMARY KEY, body TEXT NOT NULL) WITHOUT ROWID", [])?;
    {
        let mut insert = transaction.prepare("INSERT INTO pages (id, body) VALUES (?, ?)")?;
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

// Change exactly one on-disk byte and keep the payload syntactically plausible.
pub fn flip_probe(path: &Path, probe: &str) -> Result<()> {
    let bytes = fs::read(path)?;
    let mut offsets = bytes
        .windows(probe.len())
        .enumerate()
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
