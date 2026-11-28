# C vs C++ vs Rust for the Workshop compute core

**Pass:** Grok 4.5 first pass (cheap researcher). Not a ruling.  
**For:** Prima (chief engineer), then Matthew (Director).  
**Scope:** compute core only (the fortress that protects the book). Priorities, in order: safety/correctness → small auditable code, few outside deps → speed. Current ruling: Rust for compute; `wf` already Rust.  
**xAI context (Nov 2026):** Musk said xAI rewrote Grok’s RL/inference stack from scratch in C/C++; no published code or benchmarks.

---

## 1. What each language gives and costs

### Memory safety

| | Gives | Costs |
|---|---|---|
| **C** | Full control of layout and lifetime. | No language memory safety; programmer checks every reference. NSA: C/C++ “rely heavily on the programmer” and “simple mistakes can lead to exploitable memory-based vulnerabilities.” [1] |
| **C++** | RAII and richer types; Core Guidelines aim for statically type-safe, leak-resistant style. [2] | Still memory-unsafe by language class. CISA lists new critical-infrastructure product lines in C/C++ (when MSL alternatives exist) as a bad practice. [3] ONCD: C and C++ lack memory-safety traits and are widespread in critical systems. [4] |
| **Rust** | Ownership checked at compile time; invalid programs do not compile. [5] Safe by default unless `unsafe`. [6] Listed by NSA as a memory-safe language. [1] | `unsafe` and non-MSL libs reintroduce risk (localized, still audit needed). [1][6] Learning curve / compile friction. [1] |

Industry scale: ~70% of Chromium high-severity bugs and ~70% of Microsoft MSRC CVEs are memory-safety issues in C/C++-class code. [7][8][9]

### Correctness tooling

- **C/C++:** SAST/DAST help but cannot make non-MSL code fully memory-safe; even strong SAST catches only a portion and yields many false positives. [1] C++ Core Guidelines + analyzers are process/tooling, not language enforcement. [2] MISRA C/C++ are critical-systems coding guidelines with mandatory process/deviation discipline. [10]
- **Rust:** Borrow checker at compile time. [5] Clippy: 800+ lints; `clippy::correctness` defaults to deny. [11] Miri detects UB in unsafe (out-of-bounds, use-after-free, etc.) but is dynamic and incomplete. [6][12]

### Auditability and dependency control

- **C:** Tiny surface if you own headers and avoid libs; audit is line-by-line human judgment. No standard package lock like Cargo.
- **C++:** Larger language/stdlib surface; same “bring your own deps” story (CMake/vcpkg/etc.). Guidelines push small, well-specified interfaces. [2]
- **Rust:** Empty `[dependencies]` is valid; deps are explicit in `Cargo.toml` and pinned in `Cargo.lock`. [13][14] Cost: crates.io default path makes pulling transitive trees easy—fortress policy must forbid casual deps.

### Speed

- C/C++/Rust are all systems languages with minimal/optional runtime; Microsoft MSRC treats them similarly for raw speed/control vs GC languages. [8]
- Rust ownership “will [not] slow down your program while it’s running.” [5] Official book: iterators as zero-cost abstractions (comparable to hand loops). [15]
- C++ Core Guidelines likewise claim following the rules still “will run fast.” [2]
- **No Workshop-specific or xAI public benchmarks** comparing the three for our workload. UNSOURCED if claimed otherwise.

### Long-term maintenance by AI models writing the code

- LLM-generated project study (10 languages, 110 projects): C had 39.1% critical findings (memory-heavy); Rust 0% critical in that table (still had high/medium issues). [16]
- LLM C→Rust work can remove memory classes when it lands in safe Rust, but translations are often functionally wrong without harsh differential checks. [17][18]
- Google: AI-assisted C→Rust of giflib needed expert `unsafe`/FFI review and mass differential testing; Rust then immune to a later C memory CVE. [19]
- Implication for the fortress: Rust’s compiler rejects many AI memory mistakes; C/C++ accept them unless tests/fuzzers catch them. Logic bugs remain in all three.

---

## 2. Why xAI chose C/C++ — and does it apply here?

**What Musk said (primary X posts, 10 Nov 2026):**

- Dumped JAX/SGLang; rewrote “the entire RL and inference stack from scratch in C/C++.” [20]
- Clarified: “C with a little C++, but not too much.” [21]
- “(There’s even some assembly).” [22]
- Stack “derived from” Starlink-side engineering; SpaceX “write[s] our own headers and calculate[s] our own time.” [23]
- On Rust vs C: “Rust is a good language, but C is what you use for optimal performance on bare metal. With great power comes great responsibility.” [24]

**Likely reasons for *their* workload (inferred from those posts + domain, not from published benchmarks):**

1. Replace Python/JAX and a serving framework with owned host code for GPU-scale RL+inference loops. [20]
2. Reuse / derive from existing SpaceX low-level stack culture (headers, time, assembly). [22][23]
3. Bare-metal performance priority stated over Rust. [24]

**Published evidence gap:** No code, no independent tokens/s or safety benchmarks in these posts. [20–24]

**Does that reasoning apply to Workshop compute?**

| xAI driver | Workshop compute |
|---|---|
| GPU RL/inference at frontier scale | Authority gate + book integrity (fortress), not training kernels |
| Escape JAX/SGLang | No JAX/SGLang in scope |
| Reuse Starlink/C assembly culture | Team already on Rust (`wf`, compute ruling) |
| Bare-metal micro-opt first | Safety/correctness ranked above speed |

So xAI’s C/C++ move is a **different job**. Copying it would fight our priority order and CISA/NSA/ONCD guidance for new MSL-capable systems. [1][3][4]

---

## 3. Recommendation and main risks

**Recommend: keep Rust for the compute core.**

Aligns with: language-level memory safety [1][5]; Director fortress priorities; existing `wf`/compute Rust; CISA preference for new product lines in MSLs [3]; AI-written code failing closed more often on memory classes [16][19].

**Main risks if we stay on Rust**

1. `unsafe` / FFI creep undoes the fortress story — treat like C islands. [1][6]
2. Dependency gravity via crates.io — policy: near-zero third-party crates for compute. [14]
3. AI still ships logic/auth bugs; Rust does not replace hostile trials (see prior compute trial findings).
4. Rare hot paths may want C/asm later — isolate, don’t flip the core language.

**Main risks if we switch to C/C++ “like xAI”**

1. Re-open the ~70%-class memory bug factory without their hardware/process machine. [7][8][9]
2. CISA bad-practice posture for new C/C++ critical product lines when MSLs exist. [3]
3. AI models write memory-unsafe C at high critical rates vs Rust in one cross-language study. [16]
4. We lack their Starlink-derived stack and published proof that C wins for *our* gate. [20–24]

**Speed note:** Prefer measure-then-optimize inside Rust; only then consider sealed `unsafe` or a tiny C shim.

---

## Self-check

1. **xAI “why” beyond Musk’s words** — bare-metal/Starlink motives are read from posts [21–24]; no internal xAI design doc. Soft-rollout/eval claims truncated on the API copy of [20]; not load-bearing here.
2. **AI-maintenance advantage of Rust** — supported by [16][17][19] but sample sizes/scopes differ; not Workshop-specific.
3. **“Few deps easier in C than Rust”** — culturally true for freestanding C; not a standards citation. Cargo makes deps *visible* [14]; discipline is policy either way.

---

## Sources

1. NSA CSI, *Software Memory Safety* (Apr 2023, v1.1). https://media.defense.gov/2023/Apr/27/2003210083/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY_V1.1.PDF — “Commonly used languages, such as C and C++, provide a lot of freedom and flexibility in memory management while relying heavily on the programmer… Simple mistakes can lead to exploitable memory-based vulnerabilities.” / “NSA recommends using a memory safe language when possible.” / Examples include “Rust”.
2. ISO C++ Core Guidelines (eds. Stroustrup/Sutter). https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines — “Following the rules will lead to code that is statically type safe, has no resource leaks, and catches many more programming logic errors… And it will run fast.”
3. CISA/FBI, *Product Security Bad Practices* (rev. Jan 17, 2025). https://www.cisa.gov/resources-tools/resources/product-security-bad-practices — “The development of new product lines… in a memory-unsafe language (e.g., C or C++) where readily available alternative memory-safe languages could be used is dangerous…”
4. White House ONCD, *Back to the Building Blocks* (Feb 2024). https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf — “Experts have identified a few programming languages that both lack traits associated with memory safety and also have high proliferation across critical systems, such as C and C++.” / “Using memory safe programming languages can eliminate most memory safety errors.”
5. *The Rust Programming Language*, “What is Ownership?”. https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html — “If any of the rules are violated, the program won’t compile. None of the features of ownership will slow down your program while it’s running.”
6. *The Rust Programming Language*, “Unsafe Rust” (Miri section). https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html — “One of the best ways to do that is to use Miri, an official Rust tool for detecting undefined behavior.” / “Miri doesn’t catch everything…”
7. Chromium Security, Memory safety. https://www.chromium.org/Home/chromium-security/memory-safety/ — “Around 70% of our high severity security bugs are memory unsafety problems (that is, mistakes with C/C++ pointers).”
8. Microsoft MSRC, “Why Rust for safe systems programming” (22 Jul 2019). https://www.microsoft.com/en-us/msrc/blog/2019/07/why-rust-for-safe-systems-programming — “roughly 70% of the security issues that the MSRC assigns a CVE to are memory safety issues.” / “Unless explicitly opted-out of through usage of the “unsafe” keyword, Rust is completely memory safe…”
9. CISA et al., *The Case for Memory Safe Roadmaps* (Dec 2023). https://www.cisa.gov/sites/default/files/2023-12/The-Case-for-Memory-Safe-Roadmaps-508c.pdf — cites ~70% Microsoft CVE and ~70% Chromium figures for memory safety.
10. MISRA Compliance. https://misra.org.uk/compliance/ — “a credible claim of compliance… can only be made when code is developed under a process which meets the principles laid out in the MISRA Compliance document.”
11. Clippy Documentation. https://doc.rust-lang.org/stable/clippy/ — “There are over 800 lints…” / `clippy::correctness` default **deny**.
12. rust-lang/miri README. https://github.com/rust-lang/miri — “Miri is an Undefined Behavior detection tool for Rust.” / “be aware that Miri does **not** catch every violation…”
13. *The Rust Programming Language*, “Hello, Cargo!”. https://doc.rust-lang.org/stable/book/ch01-03-hello-cargo.html — Cargo.toml may list an empty `[dependencies]` section.
14. *The Cargo Book*, Specifying Dependencies. https://doc.rust-lang.org/stable/cargo/reference/specifying-dependencies.html — “Your crates can depend on other libraries from crates.io or other registries, `git` repositories, or subdirectories…”
15. *The Rust Programming Language*, “Performance in Loops vs. Iterators”. https://doc.rust-lang.org/stable/book/ch13-04-performance.html — “Iterators are one of Rust’s zero-cost abstractions, by which we mean that using the abstraction imposes no additional runtime overhead.”
16. Wang et al., “The Hidden Vulnerabilities of AI-Generated Code…” PDF. https://carteryagemann.com/docs/Jinghao_Wang_ICCV25.pdf — “C showing an alarming 39.1% critical issue rate… The stark contrast with Rust (0% critical issues)…”
17. SafeTrans (arXiv:2505.10708). https://arxiv.org/pdf/2505.10708 — iterative LLM C→Rust; vulnerabilities in original C “effectively mitigated in the translated Rust code” (per authors).
18. “Re-Testing LLM-Based C-to-Rust Translations…” (arXiv:2611.23839). https://arxiv.org/abs/2611.23839v1 — “All eleven release defective translations…”
19. Google Bug Hunters, “Scaling Memory Safety…” https://bughunters.google.com/blog/scaling-memory-safety — AI-assisted giflib→Rust; later C CVE neutralized by Rust fork.
20. Elon Musk (@elonmusk), 10 Nov 2026. https://x.com/i/status/2120088070443655190 — “We have dumped JAX/SGLang and rewritten the entire RL and inference stack from scratch in C/C++, which took some extra time.”
21. Elon Musk (@elonmusk), 10 Nov 2026. https://x.com/i/status/2120090704043200865 — “C with a little C++, but not too much”
22. Elon Musk (@elonmusk), 10 Nov 2026. https://x.com/i/status/2120098433159880790 — “(There’s even some assembly).”
23. Elon Musk (@elonmusk), 10 Nov 2026. https://x.com/i/status/2120097663794483601 — “At SpaceX, we write our own headers and calculate our own time (includes leap seconds).” / “The new Grok AI/SI training and inference stack is derived from…”
24. Elon Musk (@elonmusk), 10 Nov 2026. https://x.com/i/status/2120220004578963572 — “Rust is a good language, but C is what you use for optimal performance on bare metal. With great power comes great responsibility.”
