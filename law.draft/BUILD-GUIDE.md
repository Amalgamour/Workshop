# How this sample was built

These scripts are teaching tools supplied with the design book, not law faces or a new page role. The generated content is a proposal, not an approved kernel change.

## build.py

Read the `pages` definitions first. Each section contains its heading, proposed owner, normative statement, why, and compact form. The generator writes that material into 01, 02, 03, and 04, keeping section identities aligned while separating their jobs. It adds 08 only for the two pages with relationship/source records.

The same definitions are used to assemble the book, menus, contents, review report, and working note. The generator checks actual links and heading anchors, draft identities, duplicate headings, coverage, and reserved-face absence before producing its payload and manifest.

This is a construction example. It does not prove semantic agreement or authority. Face 04 currently reuses the normative prose with a why and compact-form explanation; a later author can improve that readable form while preserving all conditions. Independent hostile review remains necessary.

## install.py

The installer reads the generated manifest, verifies that every destination stays inside colab/designs or colab/notes, and refuses to overwrite an existing file. It writes the working note first, then the design, and verifies each file against the manifest.

The supplied copies include one correction to the original run: generated documents are written as explicit UTF-8 bytes so Windows newline conversion cannot cause the byte comparison to fail. The page content is unchanged.

## Using the example

1. Inspect the scripts before running them. Their paths are specific to this workstation.
2. In build.py, review `out` (staging), `sources` (kernel evidence), and the proposed page content. Source files and referenced anchors must actually exist.
3. In install.py, review `root` (colab destination) and the manifest path. The default manifest location matches build.py's staging output.
4. Choose a fresh staging directory and an unused destination. Update both scripts consistently. Simply changing the book folder name does not update its identity stamps, notes, or report names.
5. Run build.py with Python 3.11 or newer. Review the staged payload and manifest before running install.py.
6. Run install.py only when the destinations and content are authorized. Filesystem approval may still be required by the agent's session.

Do not rerun installation against the existing law.draft: it deliberately refuses to overwrite it. Neither script edits kernel.draft, approves a face, or performs a retirement. The installer is not a transactional update mechanism; an interrupted write can leave a partial destination needing inspection.

The scripts themselves and this guide are supplied alongside the generated book. They are not included in the generated manifest, so future rebuilds must carry them separately if desired.
