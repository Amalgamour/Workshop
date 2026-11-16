//! Current reading of each dev page, and the next pass where the design is still open.

use std::env;
use std::path::Path;

use seqbook::{Error, Tail, Writer};

const AT: &str = "2026-11-11T20:18:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book path");
    let mut writer = Writer::open(Path::new(&path)).expect("open");
    for (addr, body, tail) in NOTES {
        put(&mut writer, addr, body, *tail);
    }
    println!("len {}", writer.book().len());
}

fn put(writer: &mut Writer, addr: &str, body: &str, tail: Option<Tail>) {
    match writer.put(AT, BY, addr, body, tail) {
        Ok(()) => {}
        Err(Error::Exists { .. }) => {}
        Err(err) => {
            eprintln!("{addr}: {err}");
            std::process::exit(1);
        }
    }
}

const NOTES: &[(&str, &str, Option<Tail>)] = &[
    (
        "10.10.10.0000.06.02",
        "## current\ntype: note\naxioms: 6.7\nby: cursor\nrefs: 10.10.10.0000.01, 10.10.10.0000.04\nwhy: A person who reads the seated card still sees the stand, and the stand is no longer the state.\n\nFace 01 still says the address was not granted and that there is no build. Face 04 still says the header is 7 and that build is not authorized. Both sentences were true when the book was stood. They are not true now.\n\nThe address is 10.10.10. The core in core/ has been built and checked. These faces cannot be rewritten. There is no promote. This note is the current reading.\n",
        None,
    ),
    (
        "10.10.10.0301.06.01",
        "## current\ntype: note\naxioms: 8.6\nby: cursor\nrefs: 10.10.10.0302, 10.10.10.0303, 10.10.10.0304\nwhy: The empty build page still says no work was granted, and the work now has files.\n\nFace 01 still says no work is granted. The crate is core/. Its read path is described on 0302, the why check on 0303, and the page-shape check on 0304. Those three pages have a finding: the face 04 card module repeats the face 01 body. That wording stays until a face can be revised.\n",
        None,
    ),
    (
        "10.10.10.0401.06.04",
        "## current\ntype: note\naxioms: 5.4.6\nby: cursor\nrefs: 10.10.10.0501.05.01, 10.10.10.0401.06.02\nwhy: The page MVP and the design goal are different sizes, and the seated frame still says to stop before code.\n\nMVP of this page: the five core checks in agents.003.md. Status: met. Pack 0501.05.01 is at return. The fixture is core/fixtures/10.11.21.book. No further pack is opened on 0501. This frame does not grow into the app.\n\nThe four questions on 0401.05 are answered on 0401.06.02. Their tails are still draft. A question is not a pack, and there is no close for a question. Do not run them as jobs.\n\nFace 01 still says stop before code. That was the frame when the page was stood.\n",
        None,
    ),
    (
        "10.10.10.0402.06.02",
        "## current\ntype: note\naxioms: 5.4\nby: cursor\nrefs: 10.10.10.0502.05.01, 10.10.10.0502.05.02\nwhy: The page MVP is met, and the design's reader is still the app.\n\nMVP of this page: print one face from a book file. Status: met. seqbook read prints the timer why. Pack 0502.05.01 is at return. The note on 0402.06.01 says that pack stays draft. That sentence is no longer true.\n\nDesign.md still names the Next.js app as the reader for faces and links. That is not this page's finished MVP. The next pass is 0502.05.02. It is draft. It does not start until the questions on 0405 are answered.\n",
        None,
    ),
    (
        "10.10.10.0403.06.02",
        "## current\ntype: note\naxioms: 4.5\nby: cursor\nrefs: 10.10.10.0503.05.01, 10.10.10.0503.05.02\nwhy: A check a person can run is not the same as a compute that refuses the write.\n\nMVP of this page: fail a 01 or 02 card with no 04 why and body, and flag a copied body. Status: met as a library check. Pack 0503.05.01 is at return. Keyword branding stays out.\n\nformat.md says the compute rejects a write that fails the hard 04 rule. That rejection does not exist yet. The next pass is 0503.05.02. It is draft, and it uses the one compute named on 0405 rather than a second process.\n",
        None,
    ),
    (
        "10.10.10.0404.06.02",
        "## current\ntype: note\naxioms: 5.2\nby: cursor\nrefs: 10.10.10.0504.05.01, 10.10.10.0504.05.02\nwhy: A shape check in a test is not a refusal a person can watch.\n\nMVP of this page: fail a page with no face 00, or no content face. Face 07 does not count. Status: met as a library check. Pack 0504.05.01 is at return.\n\nThe compute does not yet refuse a bad page. The next pass is 0504.05.02. It is draft, and it is the same compute as 0503.05.02.\n",
        None,
    ),
    (
        "10.10.10.0501.06.02",
        "## current\ntype: note\naxioms: 6.7\nby: cursor\nrefs: 10.10.10.0501.01, 10.10.10.0501.05.01\nwhy: The jobs page still says it is empty, and it holds a returned pack.\n\nFace 01 still says no work is granted. Face 04 still says face 05 has no counters. Pack 0501.05.01 exists and is at return. There is no 0501.05.02. The first-build frame is met.\n",
        None,
    ),
    (
        "10.10.10.0502.06.02",
        "## current\ntype: note\naxioms: 6.7\nby: cursor\nrefs: 10.10.10.0502.01, 10.10.10.0502.05.01\nwhy: The jobs card still says the pack is waiting to be linted.\n\nFace 01 says 0502.05.01 stays draft until something lints it. That pack is at return. The work cards had no ask line. The page AGENTS.md held the ask. The next pass is 0502.05.02, and it does carry an ask.\n",
        None,
    ),
    (
        "10.10.10.0503.06.02",
        "## current\ntype: note\naxioms: 6.7\nby: cursor\nrefs: 10.10.10.0503.05.01, 10.10.10.0503.05.02\nwhy: The jobs card still describes a pack that has already returned.\n\n0503.05.01 is at return. The next pass is 0503.05.02.\n",
        None,
    ),
    (
        "10.10.10.0504.06.02",
        "## current\ntype: note\naxioms: 6.7\nby: cursor\nrefs: 10.10.10.0504.05.01, 10.10.10.0504.05.02\nwhy: The jobs card still describes a pack that has already returned.\n\n0504.05.01 is at return. The next pass is 0504.05.02.\n",
        None,
    ),
    (
        "10.10.10.0405.00",
        "address: 0405\ntitle: usable\nstate: draft\ntype: workflow\naxioms: 5.1.4\nband: dev\nthousands: 0\nmvp: A person can use an app, see a face, see the compute decide, and talk with a model.\n",
        None,
    ),
    (
        "10.10.10.0405.01",
        "## frame\ntype: rule\naxioms: 5.1\n\nMVP: a person opens one app, reads a face and its why, watches the compute accept or refuse a write, and can send a sentence to a model. The model's proposal is visible. Nothing is appended until the compute accepts it. The book file remains openable in an editor.\n\nDone does not include brands, the kernel fill, snapshots, forks, or a second writer.\n\nThis page is the aim named on 2026-11-11. It inherits the finished checks on 0402, 0403, and 0404. It does not reopen them.\n",
        None,
    ),
    (
        "10.10.10.0405.04",
        "## frame\ntype: why\nsource: [01 / frame]\naxioms: 5.1.4\nwhy: A core that only a test can run is not yet something a person can use.\n\nDesign.md names four parts. The core is the only one that runs. The compute is supposed to be the thing a person can watch validate and append. The app is supposed to be the thing a person reads. Models are supposed to propose to the compute, not write the file.\n\nThe findings of the page check are on 0405.06.01. The next packs are draft. They wait on the questions in that note: what is missing, what is needed, and whether more tools should be made.\n",
        None,
    ),
    (
        "10.10.10.0405.06.01",
        "## findings\ntype: note\naxioms: 7.4.9\nby: cursor\nrefs: 10.10.10.0401.06.04, 10.10.10.0402.06.02, 10.10.10.0403.06.02, 10.10.10.0404.06.02\nwhy: A check that is not written down will be replaced by whatever the next session remembers.\n\nChecked every page in 10.10.10 by replaying the book. Hard why gaps: none. Page-shape gaps: none. Findings: 0302, 0303, and 0304 card module copies face 01 onto face 04.\n\nComplete against their own MVPs: 0401 the five core checks, 0402 print one face, 0403 the why check, 0404 the page-shape check. Packs 0501.05.01 through 0504.05.01 are at return. They are not reviewed.\n\nNot complete against Design.md: no compute process, no Next.js app, no path for a model to propose a write, no way to revise a seated face, no return op on the same counter, no pack lint that seats an ask line, no board a person can see, no kernel book.\n\nWhat is missing: the compute, the app, and a drafting tool. The seated cards that are now false cannot be corrected in place.\n\nWhat is needed before a build: where the model runs, and whether the app talks to the compute over HTTP, MCP, or both. format.md left that open.\n\nMore tools: not a new language and not a new file format. One compute program and one app, both using the core. A way to revise a face is the tool the corrections are waiting on. A page list belongs in the reader the app already has to be.\n\nThese three questions are for the person. The packs below stay draft until they are answered.\n",
        None,
    ),
    (
        "10.10.10.0405.08",
        "## frame\ntype: link\naxioms: 8.7\nkind: 7\nwhy: The aim has to point at the passes that would build it, and at the pages whose MVPs it inherits.\n\nInherits 0402 read, 0403 why-check, and 0404 page-shape. Does not continue them.\nJobs: 0505.usable. The first pack is 0505.05.01.\nThe face view is also 0502.05.02. The why refusal is also 0503.05.02. The shape refusal is also 0504.05.02. One compute, not three.\nBuild page 0305 is not stood. There is no module yet.\n",
        None,
    ),
    (
        "10.10.10.0502.05.02",
        "by: cursor\nauthorized: person-2026-11-11-aim\nlead: M\naxioms: 5.4\noutcome: A person opens a local page and reads one face's why without cargo.\noverview: The next pass of read. The CLI MVP is met. This pass is the face in the app, read from the compute.\nstop if: The person has not answered the questions on 0405.06.01. Or the work needs a second compute beside 0505.05.01.\ngrant: A future app/ page that shows one face. It calls the compute. It does not read the book file itself.\nframe: read\nrisk: 2\npredecessor: 10.10.10.0502.05.01\n\n## w01\ntype: work\ntitle: Show one face in the app\naxioms: 5.4\nreason: The design's reader is the app. The CLI proved the face can be printed, and it is not the reader a person keeps open.\npath: app/\nask: Open the app, ask for 10.11.21.1001.04, and read the why on the screen.\n",
        Some(Tail::Draft),
    ),
    (
        "10.10.10.0503.05.02",
        "by: cursor\nauthorized: person-2026-11-11-aim\nlead: M\naxioms: 4.5\noutcome: The compute refuses a 01 card with no 04 why, and the refusal is visible.\noverview: The next pass of why-check. The library check is met. This pass is the refusal inside the one compute.\nstop if: The person has not answered the questions on 0405.06.01. Or the work would start a second process.\ngrant: The compute started by 0505.05.01. Use the core why check. Do not edit decisions.md.\nframe: why-check\nrisk: 2\npredecessor: 10.10.10.0503.05.01\n\n## w01\ntype: work\ntitle: Refuse a missing why\naxioms: 4\nreason: A test that calls why_gaps is not a write the compute stopped.\npath: compute/\nask: Submit a 01 card with no 04 twin and show the refusal, including the page and the card key. The book file must not gain that face.\n",
        Some(Tail::Draft),
    ),
    (
        "10.10.10.0504.05.02",
        "by: cursor\nauthorized: person-2026-11-11-aim\nlead: M\naxioms: 5.2\noutcome: The same compute refuses a page with no face 00, or no content face, and the refusal is visible.\noverview: The next pass of page-shape. Face 07 still does not count.\nstop if: The person has not answered the questions on 0405.06.01. Or the work would change which faces count.\ngrant: The compute started by 0505.05.01. Use the core page check.\nframe: page-shape\nrisk: 2\npredecessor: 10.10.10.0504.05.01\n\n## w01\ntype: work\ntitle: Refuse a bad page\naxioms: 5.2\nreason: The shape rule is only real when a bad page cannot be appended.\npath: compute/\nask: Submit a page whose only content face is 07, show the refusal, and show that the book did not gain the page.\n",
        Some(Tail::Draft),
    ),
    (
        "10.10.10.0505.00",
        "address: 0505\ntitle: usable\nstate: draft\ntype: workflow\naxioms: 5\nband: jobs\nthousands: 0\n",
        None,
    ),
    (
        "10.10.10.0505.01",
        "## frame\ntype: rule\naxioms: 5\n\nPacks for usable live here. 0505.05.01 is the pass that makes the compute and the model visible. It stays draft until the questions on 0405.06.01 are answered.\n",
        None,
    ),
    (
        "10.10.10.0505.04",
        "## frame\ntype: why\nsource: [01 / frame]\naxioms: 5.4\nwhy: The model has to propose to something the person can see, or the book is being written beside the conversation.\n\nThis page holds that pass. It does not itself decide HTTP or MCP, and it does not name a model host.\n",
        None,
    ),
    (
        "10.10.10.0505.08",
        "## frame\ntype: link\naxioms: 8.7\nkind: 7\nwhy: The jobs page points back at the dev page.\n\nDev page: 0405.usable.\nAlso uses 0502.05.02, 0503.05.02, and 0504.05.02. One compute.\n",
        None,
    ),
    (
        "10.10.10.0505.05.01",
        "by: cursor\nauthorized: person-2026-11-11-aim\nlead: M\naxioms: 1.5.4\noutcome: A person types a sentence, sees the model's proposal, sees the compute accept or refuse it, and can open any appended line in the book.\noverview: The aim on 0405. One local compute. One app. Models propose. The compute decides. The book stays examinable.\nstop if: The person has not answered where the model runs, or whether the app uses HTTP, MCP, or both. Stop rather than picking one.\ngrant: compute/ and app/ in this repo, using the core. Do not edit director/, seqAddr.md, decisions.md, or the root AGENTS.md. Do not rewrite a seated face.\nframe: usable\nrisk: 3\npredecessor: 10.10.10.0405.06.01\n\n## w01\ntype: work\ntitle: Run one compute over the core\naxioms: 1\nreason: The design says only the compute appends, and today the examples append directly.\npath: compute/\nask: Start one process against cursor/temp.book. Read one face through it. Stop it. The book is unchanged by the read.\n\n## w02\ntype: work\ntitle: Show the proposal and the decision\naxioms: 1.9\nreason: A person cannot see the compute working if the model writes the file itself.\npath: app/\nask: Type one sentence. Show the model's proposed write. Show the compute's accept or refusal. If it appends, the new line is visible in the book file.\n",
        Some(Tail::Draft),
    ),
];
