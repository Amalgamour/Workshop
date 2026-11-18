# Cold assessment — what works, what is claimed, what blocks (0707/05.19)
**Basis:** the 405 frozen pack05.19 sources only. **Labels:**
- **V-P** = verified by Prime in a frozen review;
- **V-C** = verified by me here (labs; my own cases);
- **C** = claimed by an author, not independently rerun;
- **B** = blocked.

| Component | State | Label | Evidence |
|---|---|---|---|
| v7 core (selected): N5 prepare → form → record → inspect → separate publish → read/recover | works up to 24 book sources | V-P / V-C | 0522/06.31 core review wb980a2a…; inv1 C2 boundary, C5b |
| v8 intake staged at canonical root (door, declaration, pass04 = my 05.18 bytes) | N5 parity on the live cut; N7 26/33 complete; **not selected** | V-P | 0522/06.31 |
| v8 grammar defects A-01 and A-02 (in my 05.17 design) | **open:** malformed N7 lines fall back, and a refused line is ignored beside a valid one | V-P, V-C end-to-end | 0522/06.31; inv2 X1 (decoy manifest recorded and published), X2 |
| Director decision | "Block malformed N7 declarations (Recommended)" | recorded | 0420/06.42 |
| Strict N7 successor (pass05 / v9, Grok-2 0522/05.15) | **pending:** pack frozen, no accepted output | — | pack only |
| Record capacity: prime_review pass02 `MAX_LIST = 24` on `sources` | **blocks normal-size returns.** 0512/05.09 has 29 sources; **0707/05.17 has 26 (N7, fully parsed)** | V-P (0512), V-C (boundary, 0517) | 0512/06.16; inv1 C1, C2, C4 |
| Capacity successor (Grok-1 0512/05.10) | **pending** | — | pack only |
| Supplied judgment on a refused record | preserved intact in `failed/…json`; no review stored | V-C | inv1 C1 |
| Reporter hardening v3 (0512/05.09) | accepted technically; external candidate dispatcher f1d23d45…; **not selected** | V-P | 0512/06.16 |
| Reporter versus combined selection | v3 refuses any other dispatcher, and reports v8 N7 records as stale | V-C | inv2b X6, X7 |
| First-target repair (0521/05.14) | N7 absent target created only by a cycle-committed render; isolated, pass02 lineage | V-P (isolated) | 0521/06.29 |
| First-target versus Colab N7 route | a cycle needs `custody == complete-descriptor`, and Colab N7 has none, so its record is always preliminary. The 0521 successor refuses preliminary creation of an absent N7 target, while v7/v8 create it today. | V-C (code and run) | inv2 X3, X4 |
| Custody (N1) / 01NN migration | missing (0122 pending) | V-P | 0522/06.31 |
| Dispatcher change versus history | 0522/05.13 declares `app/librarian.py`, README and the v7 door/JSON; 0522/05.14 declares the staged v8/pass04 bytes; 0512/05.07–09 declare reporter v1–v3 | V-P (05.13), V-C (inventory) | 06.18.review; inv2 X5; inv1 C5 |

## Source gaps (findings, not filled from memory)
- **No frozen artifact shows whether the 0521 successor's bind-false change is needed on the PRELIMINARY path.**
  - pass01 `call_prime` passes `--root BOOK`, and preliminary records with bind true succeed (V-C, every lifecycle).
  - So bind false is a cycle-path requirement only.
  - The builder must confirm this against the cycle call site; I did not run a cycle with custody.
- **`prime-review05.18/app-artifact-discovery.json` is cited by 06.18 and 0522/06.29, but it is not in the frozen menu.** I used my own static scan (X5) and did not read that file.

## Smallest finish criteria for "the Prime loop works"
On the ACTUAL work book, through ONE selected `app/librarian.py`, for one N5 and one N7 return each having more than 24 book sources:
1. prepare and form complete;
2. a record that retains the supplied judgment;
3. a full inspect read;
4. a separate publish;
5. exact read and recover;
6. a review-report that agrees, current.

In addition:
- Director text is protected.
- Malformed N7 is blocked.
- Stale and tampered sources are held.
- Old evidence is preserved and shown stale.

**Custody and migration stay visibly missing; they are not part of "works".**
