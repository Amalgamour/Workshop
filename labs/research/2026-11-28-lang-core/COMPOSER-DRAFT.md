# C vs C++ vs Rust for the Workshop Compute Core

**Author:** Cursor Composer 2.5 (first pass)  
**Date:** 2026-11-28  
**Audience:** Workshop build (Director: Matthew John Fisher; chief engineer: Prima)

The compute core is the protected heart of Workshop—“the compute is the fortress that protects the book.” Priorities: (1) safety and correctness, (2) small, auditable code with few outside dependencies, (3) speed. Current ruling: Rust for the compute core only (`wf` is already Rust).

---

## 1. What each language gives and costs

**Memory safety.** C and C++ “rely heavily on the programmer to perform the needed checks on memory references” [1]; CISA/ONCD treat both as memory-unsafe and urge roadmaps toward memory-safe languages [5][7]. C++ adds language surface (templates, STL) atop the same manual-memory baseline [1] (**audit delta vs C: UNSOURCED**). Rust enforces ownership at compile time—“If any of the rules are violated, the program won’t compile” [2]—with borrow rules blocking data races and invalid aliasing [3]. Memory errors in safe Rust are compile errors; `unsafe` blocks opt out locally and must not be used to dodge safety [4][5].

**Correctness tooling.** C’s standard permits *undefined behavior* with “no requirements” on the implementation [9]; CERT lists many UB cases such as use-after-`free` [10]. C++ low-level code inherits this burden [9][10]. Production C/C++ cannot rely on sanitizers: AddressSanitizer is “not meant to be linked against production executables” [12] (typical test overhead ~2× [11]). Rust adds static linting via Clippy (“over 800 lints”) [13] and dynamic UB detection in `unsafe` via Miri [14].

**Auditability and dependencies.** Small C sources can be read line-by-line, but UB means reviews do not guarantee defined execution [9][10]. Rust localizes unverified code to `unsafe` [4]. C has no standard package manager (**minimal-deps ease vs Rust: UNSOURCED**). Cargo defaults to crates.io [15][16], so minimal graphs need policy: “The safest dependency is the one you don't include” [17].

**Speed (third priority).** Rust is classed with other “high-performance” memory-safe systems languages [8]; ownership “will [not] slow down your program while it’s running” [2]. Whether C/C++ beat Rust on Workshop-specific hot paths is **UNSOURCED**.

**AI-authored maintenance.** LLM C→Rust translation tops out around 47% verified success on real projects [18]; repository-level safe Rust hits ~19% single-shot pass [19]. In one multi-language benchmark, Rust was among languages that failed to compile [20]. **Partially UNSOURCED:** LLMs may emit more compiling C than safe Rust, but compiling C does not prove memory safety—poor fit for a fortress unless humans/sanitizers catch every bug [1][9].

---

## 2. Why xAI chose C/C++, and does that apply here?

**What Musk claimed (Nov 2026, no public code or benchmarks):**

- Replaced JAX/SGLang with an RL + inference stack “from scratch in C/C++” [21].
- Clarified: “C with a little C++, but not too much” and “(There’s even some assembly)… This is tight code.” [22][23]
- Linked the stack to Starlink-style engineering (custom headers, timekeeping) [24].
- At TomorrowX: rewrite “using primarily C and some C++… as close to the bare metal as possible”; fewer “layers of software abstraction”; third-party stacks are a “black box”; training is a “networking problem” like Starlink [25].

Inferred drivers (**partially UNSOURCED**): maximal hardware control and latency [25]; removing JAX/SGLang “black box” layers [25]; reusing Starlink networking culture [24][25]; assembly in hot paths [23]. None of this is evidenced with benchmarks [21].

**Workshop fit:** xAI optimizes a fleet RL/inference stack; Workshop’s compute core is a smaller trusted base protecting the book—scale match is **UNSOURCED**. Shared lesson: thin stacks and few dependencies [17][25]. Divergence: Workshop ranks safety over raw training throughput [5][7]; Rust already chosen for `wf`. Musk’s posts justify **engineering control**, not a mandate to abandon memory-safe languages for security-critical new code [7].

---

## 3. Recommendation

**Keep Rust for the Workshop compute core** (consistent with current ruling and `wf`).

**Why:** (1) Government guidance prioritizes memory-safe languages for new security-sensitive code [5][7]; CISA cites ~70% Microsoft CVEs as memory-safety issues [6]. (2) Rust’s compile-time checks plus bounded `unsafe`, Clippy, and Miri match fortress audit needs [4][13][14]. (3) Rust still meets “stringent performance” systems requirements when needed [8]. (4) LLM-generated Rust fails often enough that tests and review remain mandatory [18][19].

**Risks:** `unsafe`/FFI growth [5]; crates.io dependency creep [17]; compile/agent friction; headline risk from xAI’s C stack without public proof [21]. Use C/C++ only behind a narrow FFI sandwich for unavoidable SDKs [5].

**UNSOURCED markers in body:** 5 (plus partial AI claim).

---

## Sources

1. https://media.defense.gov/2023/Apr/27/2003210083/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY_V1.1.PDF — “Commonly used languages, such as C and C++, provide a lot of freedom and flexibility in memory management while relying heavily on the programmer to perform the needed checks on memory references.”

2. https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html — “If any of the rules are violated, the program won’t compile. None of the features of ownership will slow down your program while it’s running.”

3. https://rustc-dev-guide.rust-lang.org/borrow-check.html — “That you can’t access a place while it is mutably borrowed (except through the reference).”

4. https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html — “`unsafe` doesn’t turn off the borrow checker or disable any of Rust’s other safety checks.”

5. https://www.cisa.gov/sites/default/files/2023-12/The-Case-for-Memory-Safe-Roadmaps-508c.pdf — “developers should not use this keyword to avoid introducing memory safety vulnerabilities.”

6. https://www.cisa.gov/sites/default/files/2023-12/The-Case-for-Memory-Safe-Roadmaps-508c.pdf — “About 70 percent of Microsoft common vulnerabilities and exposures (CVEs) are memory safety vulnerabilities.”

7. https://www.veracode.com/wp-content/uploads/2024/07/Final-ONCD-Technical-Report.pdf — “Using memory safe programming languages can eliminate most memory safety errors.”

8. https://www.cisa.gov/sites/default/files/2023-12/CSAC_TAC_Recommendations-Memory-Safety_Final_20231205_508.pdf — “Memory Safe Systems Languages (MSSL) such as Rust, Golang, and Swift have been used as system languages which can meet stringent performance and efficiency requirements while still maintaining memory safety.”

9. https://cstd.eisie.net/c2y — “undefined behavior — behavior, upon use of a nonportable or erroneous program construct or of erroneous data, for which this document imposes no requirements.”

10. https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/back-matter/cc-undefined-behavior/ — “The value of a pointer that refers to space deallocated by a call to the `free` or `realloc` function is used” (undefined behavior).

11. https://clang.llvm.org/docs/AddressSanitizer.html — “Typical slowdown introduced by AddressSanitizer is 2x.”

12. https://clang.llvm.org/docs/AddressSanitizer.html — “AddressSanitizer is a bug detection tool and its runtime is not meant to be linked against production executables.”

13. https://doc.rust-lang.org/clippy/ — “A collection of lints to catch common mistakes and improve your Rust code. There are over 800 lints included in this crate!”

14. https://github.com/rust-lang/miri — “Miri is an Undefined Behavior detection tool for Rust… Out-of-bounds memory accesses and use-after-free.”

15. https://doc.rust-lang.org/cargo/guide/dependencies.html — “crates.io is the Rust community’s central package registry.”

16. https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html — “Cargo is configured to look for dependencies on crates.io by default.”

17. https://rust-secure-code.github.io/rust-supply-chain-security/dependencies.html — “The safest dependency is the one you don't include.”

18. https://arxiv.org/html/2405.11514v3 — “the most successful LLM can translate 47% of our benchmarks.”

19. https://arxiv.org/abs/2504.15254 — “The best performing model, OpenAI o3, is able to solve only 19 tasks in a single-shot setting.”

20. https://arxiv.org/abs/2405.13101 — “all generated codes compiled successfully with the exceptions of Fortran and Rust” (conjugate gradient task).

21. https://elonmuskarchive.org/posts/2120088070443655190 — “We have dumped JAX/SGLang and rewritten the entire RL and inference stack from scratch in C/C++.”

22. https://elonmuskarchive.org/posts/2120090704043200865 — “C with a little C++, but not too much.”

23. https://elonmuskarchive.org/posts/2120098433159880790 — “(There’s even some assembly)… This is tight code.”

24. https://elonmuskarchive.org/posts/2120097663794483601 — “At SpaceX, we write our own headers and calculate our own time (includes leap seconds).”

25. https://elonmuskarchive.org/video/tomorrowx-summit-2026-11 — “We want to get as close to the bare metal as possible… The more layers of software abstraction that you have, the less performant your code will be.”

---

## Self-check (three least-certain claims)

1. **“LLMs compile C more readily than safe Rust, but that is worse for a fortress.”** Partially **UNSOURCED**: [20] shows one Rust compile failure, not systematic LLM C vs Rust maintenance for security-critical cores.

2. **“Workshop compute scale differs from xAI GPU networking.”** **UNSOURCED**: no public Workshop architecture doc was used; logical from role description only.

3. **“C/C++ can match or beat Rust on peak speed for Workshop-specific workloads.”** **UNSOURCED**: no Workshop benchmarks; [8] only establishes Rust can meet stringent performance requirements in general.

**Source count:** 25 numbered citations (22 unique URLs; [5]/[6] and [11]/[12] share hosts).