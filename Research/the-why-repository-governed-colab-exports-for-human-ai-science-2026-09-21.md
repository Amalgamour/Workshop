# The Why Repository

## Governed Colab Exports as a Research Standard for Human–AI Science

**Author:** Matthew John Fisher  
**Drafting and research support:** ChatGPT  
**Date:** 2026-09-21  
**Status:** Research paper draft for review  
**Rights:** The originating concepts and design are the work of Matthew John Fisher. All rights retained.

## Abstract

Scientific research preserves conclusions, data, software, and selected methodological descriptions, yet much of the causal reasoning that produced them remains fragmented across notebooks, meetings, correspondence, local practice, and human memory. This missing layer becomes especially consequential when artificial-intelligence systems participate in literature review, experimental design, analysis, replication, and scientific synthesis. A model can retrieve published outcomes but often cannot reliably reconstruct why a claim has its present form, which rule is current, what was tried and rejected, which deviations were deliberate, or who authorized a change.

This paper proposes the **Why Repository**: a lean, fractal, governed repository in which scientific claims, protocols, experiments, deviations, failures, reviews, and successor interpretations form a machine-walkable causal lineage. Its portable unit is the **colab export**, a bounded research packet assembled for a particular participant and task. A colab export contains the smallest sufficient set of live rules, relevant historical neighbors, explicit deviations, evidence, authority states, and return requirements. Human researchers, models, reviewers, and computational clerks receive different projections of the same research object according to their roles.

The proposal builds upon FAIR data principles, Research Objects and RO-Crate, W3C provenance, preregistration, version control, and reproducible computational workflows. Its distinctive claim is that packaging artifacts and recording provenance are necessary but insufficient for AI-mediated science. Research infrastructure must also preserve **governed why**: the evolution of claims, the reasons for change, the status of competing explanations, the difference between a candidate and accepted scientific speech, and the explicit deviations from inherited procedure. The paper defines the architecture, describes its prospective effects on reproducibility and scientific collaboration, identifies risks, and proposes a falsifiable pilot study. If the central hypothesis is correct, a research paper without a corresponding colab repository would remain readable but become substantially diminished as a reusable scientific object.

## 1. Introduction

The scientific paper is a powerful compression format. It converts a long, uncertain research process into a stable public argument. That compression is also its limitation. Published prose normally preserves the rationale the authors considered essential for readers, but not the full sequence of decisions from which the final work emerged.

The missing material can include failed protocols, null results, calibration problems, rejected hypotheses, changes of interpretation, tacit laboratory judgments, post hoc exploration, disagreements among collaborators, and the local reasons a procedure differs from its canonical form. Some of these details appear in supplementary files, preregistrations, data repositories, electronic notebooks, issue trackers, or code history. Many remain distributed or disappear entirely.

This is not merely an archival problem. It is a problem of **causal legibility**.

A future reader—or an AI model—may find a current conclusion without being able to answer:

- What prior claim did this conclusion replace?
- Why was the earlier claim rejected or narrowed?
- Which protocol was inherited?
- What changed in this experiment?
- Was the change planned, observed, exploratory, or corrective?
- Which failures constrain the next experiment?
- Which part of the record is authoritative now?
- What evidence would justify another successor?

The proposed Why Repository addresses these questions by treating the research process as a governed lineage rather than a folder of outputs. Its premise is simple:

> Science needs repositories not only of what was produced, but of why the current claim exists.

The proposal is particularly relevant to AI-assisted science. Models can search and synthesize at scales humans cannot, but they are unreliable administrators of ambiguous state. When old and new protocols coexist, authority is implicit, negative results are absent, and similar text is retrieved without causal context, additional model capability does not by itself resolve the problem. The working environment must tell the model what is current, what is historical, what changed, what may be changed, and where uncertainty requires human judgment.

## 2. Existing Foundations and the Remaining Gap

The Why Repository is not proposed as a replacement for contemporary open-science infrastructure. It is a coordination and reasoning layer that can use existing standards.

### 2.1 FAIR and machine-actionable research objects

The FAIR Guiding Principles call for scholarly digital objects to be Findable, Accessible, Interoperable, and Reusable. Importantly, FAIR explicitly considers computational agents as stakeholders and extends beyond conventional data to algorithms, tools, and workflows. It also requires detailed provenance for reuse. This establishes the need for research assets that machines can discover and act upon, rather than artifacts optimized solely for human reading.[1]

FAIR, however, intentionally precedes implementation choices. It defines desired properties, not a complete working method for governing the evolving reasoning of a research program.

### 2.2 Research Objects and RO-Crate

Research Object work addresses the fragmentation of scientific artifacts. RO-Crate provides a lightweight, community-developed method for packaging data, software, workflows, people, instruments, identifiers, and contextual metadata in a machine-readable and human-readable form. Its designers emphasize the interconnection of artifacts and a pragmatic “just enough” use of linked-data standards.[2]

RO-Crate answers an important question: **What artifacts belong to this research object, and how are they related?**

The Why Repository adds a different but compatible question: **Which scientific speech is current, how did it become current, what did it replace, and why?**

An implementation of the Why Repository could use an RO-Crate profile for transport and interoperability. The colab export may therefore be treated as a specialized Research Object rather than a competing container format.

### 2.3 Formal provenance

The W3C PROV family provides a general model for representing entities, activities, agents, derivations, revisions, responsibility, usage, generation, and invalidation.[3] It supplies much of the formal vocabulary needed to express that a dataset was generated by an activity, that an agent held a role, or that one entity was revised from another.

Provenance can establish how an artifact came to exist. The Why Repository requires provenance, but also introduces operational governance over the research lineage: candidate versus accepted speech, retirement without deletion, conflict handling, model-facing projections, inherited rules, task-bounded packets, and required returns.

### 2.4 Preregistration

Preregistration distinguishes a priori plans from analyses developed after observing results. Advocates argue that it can improve transparency, rigor, and reproducibility by making prior commitments inspectable while leaving exploratory work possible when labeled honestly.[4]

The Why Repository incorporates this distinction but extends it across the entire project. A protocol, hypothesis, exclusion rule, or analysis plan can be recorded before execution; later deviations can be appended as explicit causal events rather than silently incorporated into the final narrative.

### 2.5 Reproducibility and replicability

The National Academies’ report on reproducibility and replicability distinguishes computational reproduction using the same inputs from replication through new data or evidence, while emphasizing that transparency alone cannot eliminate the irreducible variability of scientific systems.[5]

Conventional reproducibility packages help rerun a result. A Why Repository should additionally help a new investigator understand why those inputs, transformations, exclusions, and interpretations were selected—and which alternatives already failed.

### 2.6 The remaining gap

Existing practices can preserve artifacts, metadata, execution environments, provenance, and prior commitments. The proposed gap is the lack of a lean, general mechanism for preserving and serving **causal scientific judgment** to humans and models.

The Why Repository is intended to fill that gap without requiring every participant to read the entire history.

## 3. Core Definitions

### 3.1 Why Repository

A **Why Repository** is a governed research repository that preserves the current scientific state together with the inspectable lineage of claims, protocols, deviations, evidence, failures, reviews, and authority transitions that produced it.

It is not merely a versioned directory. It must distinguish:

- live from retired scientific speech;
- candidate claims from accepted claims;
- base rules from experiment-specific deviations;
- evidence from interpretation;
- planned analysis from post-result exploration;
- model suggestions from human authorization;
- compact model context from full human explanation;
- current execution artifacts from historical rationale.

### 3.2 Colab export

A **colab export** is a bounded, portable projection of the Why Repository assembled for a particular task, role, and participant. “Colab” here means governed collaboration and is not a reference to Google Colab.

The export may contain:

- the live hypothesis or protocol;
- the applicable base rules;
- the explicit deviations for the current experiment;
- the minimal relevant evidence;
- the compact machine-facing representation;
- selected historical neighbors when the task concerns why or repair;
- the authority and provenance required to interpret the packet;
- hostile tests and known failure modes;
- required questions;
- the required form of the return.

The packet is intentionally incomplete with respect to the whole repository. Its goal is the smallest sufficient governed context.

### 3.3 Clerk

The **Clerk** is the deterministic coordination layer between the repository and human or model workers. It resolves identifiers and titles, validates structure, selects current objects, applies access rules, assembles packets, records returns, and halts on conflicts it is not authorized to decide.

The Clerk is not the scientific authority and need not be an AI personality. It is infrastructure.

### 3.4 Brand

A **brand** is a complete generation of a scientific claim, protocol, or governing page. A successor restates the inherited claim and incorporates the accepted change. Older brands remain readable after retirement.

Brands serve two distinct purposes:

1. **Live resolution:** identify which generation currently speaks for execution.
2. **Lineage:** preserve how the scientific object changed and why.

These purposes must not be collapsed. Ordinary work receives the live brand. Historical review receives the necessary portion of the stack.

### 3.5 Face and projection

A single research object may have multiple governed projections:

- a compact model-facing face;
- a human-readable face;
- structured data and code twins;
- a private or sensitive-data projection;
- an audit or provenance projection.

The underlying identity remains stable. Different participants receive the face required for their role.

## 4. The Fractal Rule: Inherit the Base, Record the Deviation

The Why Repository is designed around a lean principle:

> Do not restate a stable rule for every experiment. Inherit it, then record the deviations required by this exact task.

Consider a locked cell-assay protocol. A new experiment may inherit that protocol while changing incubation temperature, reagent concentration, or observation window. The experiment record should not reproduce the full protocol in free prose. It should name the inherited protocol and enumerate each deviation with its reason, expected effect, and observed consequence.

This structure reduces duplication and ambiguity. A model need not compare two long methods sections to infer what changed. The Clerk provides:

- the live base protocol;
- the experiment’s explicit deviations;
- any known hostile cases triggered by those deviations.

The same pattern can apply at multiple scales:

- one instrument run inherits a laboratory procedure;
- one experiment inherits a study protocol;
- one study inherits a disciplinary method;
- one replication inherits the original research object;
- one review inherits a claim graph;
- one institution inherits a governance profile.

The system is fractal because the rule is structurally repeated rather than separately reinvented.

## 5. Proposed Scientific Lifecycle

### 5.1 Observation and question

An observation is recorded with its source, conditions, uncertainties, and author. A research question is linked to the observation but remains distinct from it.

### 5.2 Candidate hypothesis

A hypothesis begins as a candidate. It may be proposed by a human or model, but proposal does not equal acceptance. Competing candidates may coexist.

### 5.3 Protocol and preregistration

The experiment names its inherited protocol, planned deviations, analysis plan, exclusion rules, stopping conditions, and required ethical approvals. The preregistered state is timestamped.

### 5.4 Execution and observed deviation

During execution, deviations are recorded as events. The repository distinguishes planned deviations from unexpected deviations and later corrective changes.

### 5.5 Data, analysis, and interpretation

Raw data, transformations, analysis code, environments, and outputs are connected through provenance. Interpretations remain separate from measurements. Alternative analyses can coexist without silently overwriting the primary plan.

### 5.6 Hostile review

Human reviewers and specialized models attempt to break the claim under its own declared rules. They test statistical assumptions, protocol fidelity, contrary evidence, data leakage, alternative explanations, and replication feasibility.

### 5.7 Promotion

An authorized human or review body promotes a candidate claim when the governing standard is met. Promotion is an atomic causal transition:

- the successor becomes accepted scientific speech;
- the predecessor is marked retired or superseded;
- the reason and evidence are linked;
- no interval exposes two conflicting live generations or no live generation.

### 5.8 Publication and colab export

The paper is generated as the human-readable account. The colab export is released as the governed research object required for machine reuse, replication, and future extension.

### 5.9 Replication and successor work

A replication inherits the original protocol and states its environmental and procedural deviations. Its return becomes a linked research object. A failed replication does not automatically erase the original claim; it creates structured pressure on the live explanation and may trigger a successor.

## 6. Model–Clerk Interaction

The proposed system does not default to giving an AI model the entire repository. Context is a governed projection.

For an ordinary reasoning task, a model might receive:

- the title of the research object;
- the live brand;
- a compact claim face;
- experiment-specific deviations;
- relevant evidence summaries;
- instructions and required return.

The internal repository coordinates may remain Clerk-only. When a model recognizes a missing dependency, it can request possible titles:

> “This anomaly may depend on sample preparation, instrument calibration, or exclusion criteria. Resolve relevant live objects under those titles.”

The Clerk then:

1. restricts retrieval to the authorized research scope;
2. resolves titles and live states;
3. handles collisions;
4. selects the appropriate faces;
5. returns only the necessary context;
6. records the request as part of the work trace.

This changes retrieval from undirected similarity search to a governed dialogue about missing conceptual dependencies.

The model is allowed to identify what might help. It is not allowed to invent a repository object, silently choose between conflicting live claims, or promote its own suggestion into accepted science.

## 7. The Scientific Value of Failure

Negative results and failed methods are often poorly rewarded by publication systems. In a Why Repository, failure is valuable because it constrains future action.

A failed experiment may become:

- evidence against a hypothesis;
- a retired protocol branch;
- a known hostile case;
- a warning attached to an inherited method;
- a boundary condition;
- evidence that an apparent replication is not equivalent;
- a reason not to repeat an expensive path.

This is especially important for AI systems. Without access to preserved failures, models may repeatedly propose plausible experiments that laboratories have already attempted without success. A governed failure record converts local disappointment into reusable scientific intelligence.

Failure must still be interpreted cautiously. An unsuccessful experiment can reflect a false hypothesis, an inadequate protocol, insufficient statistical power, environmental variation, or implementation error. The repository should therefore preserve the failure and its competing explanations rather than encode “failed” as a universal conclusion.

## 8. From Paper-Centric to Repository-Centric Value

The strong future claim of this proposal is:

> A scientific paper without a corresponding governed colab repository will become substantially diminished in research value.

This does not mean the paper becomes invalid or worthless. It means its usefulness for machine-assisted reconstruction, replication, synthesis, and extension is limited because the model cannot reliably recover the missing why.

The transition may resemble the growing expectation that computational studies release data and code. In a mature Why Repository ecosystem, reviewers and readers may ask:

- Where is the live protocol?
- Where are the declared deviations?
- Where are the failed paths?
- Which hypothesis generation does the paper represent?
- What was preregistered?
- What changed after observing the data?
- Can a Clerk generate a replication packet?
- Can a model request the causal neighbors of this claim?

The publication remains the principal human argument. The colab export becomes the durable research substrate.

## 9. Potential Changes to Scientific Practice

### 9.1 Peer review becomes surface-specific

Different reviewers can inspect statistical analysis, protocol fidelity, provenance, ethics, contrary evidence, or causal lineage without reconstructing the entire project. Models may assist with bounded hostile review while humans retain judgment and promotion authority.

### 9.2 Replication becomes a structured comparison

A replication packet contains the original live protocol and the replicating laboratory’s deviations. Differences become explicit rather than hidden in prose. Returns can be compared mechanically and interpreted scientifically.

### 9.3 Living reviews become governed claim graphs

Systematic reviews can maintain live claims, supporting and contradictory evidence, boundary conditions, replication status, and successor interpretations. New studies update the affected lineage rather than merely appending citations.

### 9.4 Cross-disciplinary discovery becomes safer

Models can propose structural similarities across fields, while the Clerk retrieves bounded context and records whether the analogy survives expert review. A rejected analogy remains useful as a negative connection.

### 9.5 Expert tacit knowledge becomes preservable

Laboratory heuristics, instrument quirks, diagnostic judgments, and common novice errors can be preserved as governed methods and hostile cases rather than disappearing when experts retire.

### 9.6 Scientific priority gains stronger evidence

Timestamped, signed lineage can show when a hypothesis, method, or interpretation existed and how it developed. This cannot eliminate disputes, but it supplies stronger evidence than a final artifact alone and may help distinguish independent convergence from copying.

## 10. Governance and Ethics

The Why Repository must not confuse visibility with legitimacy. A claim is not true because it is well structured, and provenance does not guarantee scientific quality.

### 10.1 Human authority

Models may propose, inspect, synthesize, and attack. They should not independently promote consequential scientific claims. Promotion authority must be explicit and appropriate to the domain.

### 10.2 Privacy and controlled access

FAIR does not require unrestricted public access. Sensitive medical, personal, commercial, or national-security data may remain restricted while metadata, access conditions, and non-sensitive causal structure remain available. Colab exports must be generated according to role and authorization.

### 10.3 Protection against false structure

A structured repository can create an illusion of certainty. The system must preserve uncertainty, competing interpretations, missing evidence, and unresolved conflict. A clean graph must never substitute for empirical support.

### 10.4 Ontology rigidity

Scientific vocabularies evolve. The repository kernel should define minimal structural invariants while allowing disciplines and projects to own their local categories. The rule is stable; deviations and domain profiles carry specialization.

### 10.5 Incentive and authority capture

Institutions may manipulate authority states, suppress negative results, or restrict access for strategic reasons. Public timestamping, independent mirrors, signed exports, and plural review institutions may reduce—but cannot eliminate—these risks.

### 10.6 Documentation burden

If researchers must manually maintain an elaborate ontology, adoption will fail. The Clerk should capture structure from ordinary work, propose records, validate packets, and ask only high-value questions. Lean operation is not an aesthetic preference; it is an adoption requirement.

## 11. Testable Hypotheses

The proposal should be evaluated empirically rather than accepted because it is conceptually attractive.

### H1 — State reconstruction

Researchers or models using a Why Repository will identify the current hypothesis, protocol, and unresolved conflict more accurately and quickly than participants using conventional papers, folders, and notes.

### H2 — Deviation detection

Participants using inherited rules plus explicit deviations will detect meaningful procedural differences more accurately than participants comparing complete prose protocols.

### H3 — Failure reuse

Participants with governed access to negative and failed paths will repeat fewer previously unsuccessful proposals.

### H4 — Explanation quality

Why Repository participants will produce more accurate explanations of why the current conclusion exists, as judged by blinded domain experts.

### H5 — Context efficiency

Task-specific colab exports will require fewer model tokens than whole-repository retrieval while maintaining or improving task performance.

### H6 — Auditability

Independent reviewers will reconstruct claim lineage, authority transitions, and post-result changes with fewer disagreements.

### H7 — Replication readiness

Independent laboratories receiving a generated replication packet will require fewer clarification exchanges before attempting the study.

## 12. Minimal Pilot

The first experiment should be intentionally small.

Select one research program with:

- a reusable base protocol;
- three to five experiments;
- at least one planned deviation;
- at least one unplanned deviation;
- one null or failed result;
- one current hypothesis;
- one competing or successor interpretation;
- associated data and analysis code.

Construct a minimal Why Repository containing:

1. one live protocol;
2. explicit experiment deviations;
3. one hypothesis lineage;
4. one preserved failed path;
5. compact model and human faces;
6. one Clerk-generated colab export;
7. one hostile review return.

Then compare two conditions:

- **Control:** conventional paper, supplement, notebook excerpts, code, and data folder.
- **Why Repository:** the same underlying evidence delivered through governed colab exports.

Use both human researchers and multiple model families. Measure reconstruction accuracy, time, clarification requests, repeated failed proposals, token use, deviation detection, next-experiment quality, and causal-explanation quality.

The architecture should be considered unsupported if it adds substantial documentation cost without measurable improvement in comprehension, reuse, or auditability.

## 13. A Twenty-Year Adoption Path

A plausible adoption path would be gradual rather than revolutionary.

### Years 1–3: Demonstration

- Build a minimal Clerk.
- Test one or two scientific domains.
- Define a colab-export profile compatible with RO-Crate and PROV.
- Measure performance against conventional research packages.
- Refine the smallest stable kernel.

### Years 3–7: Tool integration

- Integrate with electronic laboratory notebooks, version control, data repositories, workflow systems, and preregistration platforms.
- Generate paper supplements and replication packets automatically.
- Develop discipline-specific profiles.
- Create model adapters and hostile-review procedures.

### Years 7–12: Institutional adoption

- Funding agencies accept colab repositories as research outputs.
- Journals request machine-actionable lineage for selected article types.
- Universities preserve expert methods and failed paths.
- Research groups use Clerk-generated onboarding and replication packets.

### Years 12–20: Norm formation

- Colab exports become expected alongside papers in data-intensive and AI-assisted disciplines.
- Peer review includes repository-level checks.
- Living reviews operate over governed claim lineages.
- Papers without causal repositories remain publishable but are recognized as less reusable by humans and machines.

This trajectory is speculative. Its purpose is to define an adoption hypothesis, not predict inevitability.

## 14. If We Are Right

*This section is intentionally speculative.*

If the Why Repository works, scientific knowledge could change from a collection of published artifacts into a governed, executable lineage of reasons.

AI systems would not need to become omniscient scientists. They would work inside an environment capable of answering:

- What is currently believed?
- Why is it believed?
- What preceded it?
- What failed?
- Which rule applies here?
- What changed in this experiment?
- What information is missing?
- What am I authorized to propose or alter?
- Who decides whether a result becomes authoritative?

The resulting system would not be “human or model.” Human researchers would continue to choose questions, assess meaning, weigh risk, interpret consequences, and authorize scientific commitments. Models would extend attention, comparison, hostile testing, synthesis, and traversal. Clerks would preserve structure, enforce boundaries, and deliver the smallest sufficient context. Repositories would retain the cumulative why.

Scientific progress could become less dependent on reconstructing the intentions of absent researchers from compressed prose. Failed experiments could become shared constraints instead of forgotten cost. Expert judgment could remain inspectable after experts leave. Independent laboratories could compare deviations directly. Models could request missing conceptual objects by title rather than fabricate context from similarity.

The paper would still matter. It would remain the coherent human argument and public explanation. But it would no longer be expected to carry the whole research process by itself.

The colab repository would be the scientific object that can be walked.

## 15. Conclusion

Science already has repositories for publications, data, software, workflows, and identifiers. It increasingly has standards for machine actionability, artifact packaging, provenance, and preregistration. The proposed Why Repository adds a missing operational layer: governed causal memory.

Its central mechanisms are intentionally small:

- stable rules inherited fractally;
- explicit deviations for the exact experiment;
- complete successor claims rather than silent rewrites;
- retirement without deletion;
- separate candidate and authoritative states;
- compact role-specific projections;
- Clerk-mediated retrieval of missing conceptual dependencies;
- bounded colab exports and durable returns.

The proposal’s strongest claim is also its clearest test: participants using governed colab exports should reconstruct research state faster, detect deviations more accurately, repeat fewer failed paths, use less context, and explain the present conclusion more faithfully than participants using conventional research artifacts alone.

If that claim survives experiment, then the colab export could become more than a supplement. It could become a standard unit of scientific collaboration in a world where humans and models jointly conduct research.

Without the repo, a model may recover the result.

With the Why Repository, it may recover the reason.

## References

1. Wilkinson, M. D., et al. (2016). “The FAIR Guiding Principles for scientific data management and stewardship.” *Scientific Data*, 3, 160018. [https://doi.org/10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
2. Soiland-Reyes, S., et al. (2022). “Packaging research artefacts with RO-Crate.” *Data Science*, 5(2), 97–138. [https://doi.org/10.3233/DS-210053](https://doi.org/10.3233/DS-210053)
3. W3C Provenance Working Group. (2013). “PROV-O: The PROV Ontology.” W3C Recommendation. [https://www.w3.org/TR/prov-o/](https://www.w3.org/TR/prov-o/)
4. Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). “The preregistration revolution.” *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606. [https://doi.org/10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114)
5. National Academies of Sciences, Engineering, and Medicine. (2019). *Reproducibility and Replicability in Science*. Washington, DC: The National Academies Press. [https://doi.org/10.17226/25303](https://doi.org/10.17226/25303)

## Revision Agenda

- Formalize a minimal colab-export schema.
- Map brands, promotion, retirement, and faces onto RO-Crate and PROV terms.
- Define the boundary between scientific authority and repository authorization.
- Design the minimal pilot and blinded scoring rubric.
- Test whether title-driven model requests outperform unconstrained semantic retrieval.
- Measure documentation burden as a primary outcome, not an afterthought.
- Specify privacy-preserving exports for sensitive research.
- Compare model-specific adapters across at least three model families.
