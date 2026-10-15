# code

This folder is the tool shelf for book `10.10.10.lib`. It is not a law page.

- `build.py` rebuilds the `law.draft` sample into a temp payload.
- `install.py --kernel` writes draft faces `0000` through `0011` beside the law seats.
- `install.py --dry-run` shows that map and writes nothing.
- `librarian-check/` is the desk checker. `lcheck.ps1` runs it.
- `jobs.py` places a `05.NN` batch. `ran` files a reviewed one as `05.NN.md` with `state: ran`. `Authorization: signed` on that file is the run mark. It is not a signature on a face. A `#NN` lists the choice fields, or issue and recommend, then path, scale, and Ask. The Ask line holds the command and the reason. A blank line sits before reply. `ran` keeps the reply and needs a status on every line. The notes for that change are in the script.
- `rules.toml` and `moves.toml` stay as they are unless a job names them.

The check kernel is `00.00.00.kernel`. These tools write only in `00.00.00.kernel.draft`, and only as `FF.VVV` beside a seat.
