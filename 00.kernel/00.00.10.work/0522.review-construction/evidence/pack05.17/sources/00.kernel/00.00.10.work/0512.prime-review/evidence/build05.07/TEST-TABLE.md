# Test table - 0512.prime-review/05.07

author suite: labs/review-report-app-pass01/tests/test_connector.py
result: 15 tests, 18.090 seconds, OK, exit 0, Python 3.14.0
independent: false

| Claim | Case | Result | Limit |
|---|---|---|---|
| The staged tool and the proposed command match the reporter | live 0512.prime-review/05.06, three processes | exit 0, stdout sha256 8a1e16649fd632400c49e6c68171f40df416229a76910eae5c3780c4aab566d0, 22083 bytes, stderr empty | author observation; review wbf38837cf0fa9c6b; readable |
| The same cut matches on the second live address | live 0521.return-placement/05.13, three processes | exit 0, stdout sha256 2fb63cd92c6234a1c9f734629c23cdae2a80ab99c804f604b406f908f74f7a2e, 19894 bytes, stderr empty | author observation; review webe8f0a86f3de800; readable |
| A page with no recorded review is forwarded | fixture 0592.connector-missing | state not-recorded, exit 1, stale null, three stdout hashes match | author fixture |
| A changed note is forwarded as stale | fixture 0591.connector-stale | state stale, exit 1, stale true, three stdout hashes match | author fixture; setup used review-loop |
| A record hash mismatch is forwarded as held | fixture 0593.connector-held | state held, exit 1, three stdout hashes match | author fixture |
| Mid-observation hold stays the frozen regression | pass03 test file hash | sha256 f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de, 32678 bytes, test name present | not rerun |
| A different perform root is refused | author hostile | names both roots, no launch | author hostile |
| A second copy is refused | author hostile | perform names the installed root; direct main names the copy's derived root | author hostile |
| Mutation flags and a declaration escape are refused | author hostile | empty stdout, stop line, before report.py | author hostile |
| A tampered reporter hash is refused | temp tree | message carries both lengths and both hashes; live file unchanged | author case |
| A missing pin is refused | temp tree | got missing, wanted size and sha256 | author case |
| A linked pin is not followed | temp labs junction | dependency conflict names the pin and was not followed | file symlink privilege was unavailable; junction used |
| Malformed and repeated arguments are refused | author case | exit 2, empty stdout | author case |
| Existing routes still select and do not mutate | invoke.py review-loop, authoring, authoring form, return-lines, where | unknown review-loop command; unknown authoring command; missing --book; command is not on this door; missing --root | empty authoring is the command check; the book check follows a known subcommand |
| The lab dispatcher file is not an install | direct lab librarian.py | exit 1, empty stdout, live book unchanged | author case |
| Prime's future probes | listed in the test module | not run | independent work remains future work |
