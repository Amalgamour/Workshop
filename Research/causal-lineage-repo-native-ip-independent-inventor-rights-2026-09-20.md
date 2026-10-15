# Causal Lineage
## Repo-Native Intellectual Property, a Public Provenance Notary, and Independent Inventor Rights

**Author:** Matthew John Fisher  
**Drafting support:** ChatGPT  
**Status:** Working research paper — conceptual and policy proposal  
**Date:** 2026-09-20

## Abstract

Generative models sharply reduce the cost of reproducing the visible form of creative and technical work. This weakens intellectual-property systems that depend primarily on controlling copies, resemblance, or first commercial arrival. This paper proposes a repo-native alternative centered on **causal lineage**: the demonstrable development path by which a work, invention, mark, or licensed derivative came into being.

The proposed system combines five elements: a canonical private repository; a publicly governed, content-blind timestamp notary; signed repository snapshots; a public chain of authorship and commercial authorization; and an **independent inventor right** for parties that can demonstrate specific, continuous, independently anchored development without causal dependence on a competing work. Public creative releases would enter a cultural commons after a proposed ten-year commercial exclusivity period, while canonical provenance, unreleased repository contents, human identity, and truthful source association would remain protected.

The proposal changes the central question in intellectual-property disputes. Similarity would no longer be treated as sufficient evidence of descent. Adjudication would compare timestamped causal histories, access evidence, specificity, continuity, and correspondence between repository states and released work. The framework is intended to reduce lawfare, protect small creators, permit parallel discovery, improve commercial licensing, and prevent the first or largest market participant from claiming an entire idea-space. The paper distinguishes this proposal from current law and outlines technical, institutional, and empirical requirements for testing it.

## 1. The problem

Modern intellectual-property systems developed when producing, copying, and distributing finished artifacts required substantial labor and capital. Generative models alter that environment. A person may soon request additional seasons of a television series, a stylistically related novel, a software implementation, a game system, or multiple variants of a product and receive plausible outputs at negligible marginal cost.

The resulting problem is larger than unauthorized copying. The visible artifact is becoming less scarce, while the invisible intelligence that produced it remains difficult to observe:

- Why was a particular choice made?
- Which alternatives were rejected?
- What future development was already planned?
- Who had authority to approve the work?
- Did a later work descend from an earlier one?
- Did two creators independently reach similar designs?
- Which derivative is commercially authorized or canonical?

A finished episode, book, program, or product cannot answer these questions. A governed repository can.

## 2. From artifact ownership to causal lineage

This paper proposes that the most valuable intellectual asset of the model era will increasingly be the **canonical repository of intent**. The repository contains more than source files. It preserves:

- The governing theory of the work.
- Design structure and causal relationships.
- Human and model contributors.
- Authority states and approvals.
- Experiments, failures, and rejected branches.
- Independent reviews and hostile tests.
- Commercial licences and derivative permissions.
- Public releases and their exact parent states.
- Retired material and the reasons it left active use.

The public artifact is analogous to a compiled binary. The repository is the source, history, build system, decision record, and continuity engine.

Under a causal-lineage framework, rights attach less to resemblance in the abstract and more to demonstrable relationships among:

1. An accountable creator or organization.
2. A sufficiently specific body of work.
3. A continuous development history.
4. Externally anchored dates.
5. Public releases derived from identified repository states.
6. Licensed descendants linked by signed authorization.

## 3. Existing legal ideas and the proposed departure

The proposal is not a description of current law. It combines and extends concepts presently divided across copyright, trademark, patent, trade-secret, contract, and evidence systems.

Current U.S. copyright guidance already distinguishes ideas from expression. The U.S. Copyright Office states that copyright protects original works of authorship but not facts, ideas, systems, concepts, or methods of operation; it may protect the way they are expressed. Publication is not required for protection. This supports the premise that similarity at the level of a general idea should not itself establish ownership or copying.

Trademark doctrine also contains part of the proposed logic. The U.S. Patent and Trademark Office describes a trademark as a sign that identifies the source of goods or services and explicitly warns that registration does not confer ownership of a word or phrase in general. Rights attach to how the mark is used with particular goods or services. Repo-native provenance would extend this association model by linking a mark to a canonical work lineage and signed commercial descendants.

Patent systems pose the sharper conflict. Current U.S. patent law operates under a first-inventor-to-file framework for relevant modern filings. The proposed independent inventor right would therefore be a policy change, not a technical implementation of existing patent doctrine. Its purpose would be to prevent an early filer or commercially dominant party from suppressing a genuinely independent, specifically developed invention that can demonstrate its own prerelease causal history.

## 4. The Public Provenance Notary

The technical foundation would be a publicly governed timestamping service: a content-blind notary that witnesses cryptographic commitments rather than storing private work.

Internet standards already demonstrate the basic primitive. RFC 3161 describes a timestamp authority that signs a hash representation to indicate that data existed at a particular time. The proposed system extends that primitive into public, mirrored civic infrastructure designed for repository history, authorship, licensing, and public verification.

### 4.1 Basic operation

1. A creator prepares a file, decision page, commit, or repository state.
2. The local system creates a collision-resistant content hash.
3. A private repository may combine many files into a Merkle tree and expose only its root hash.
4. The creator signs the commitment with an identity or pseudonymous key.
5. The public notary records the commitment in an append-only log.
6. The notary returns a signed timestamp and inclusion proof.
7. The creator later reveals all or part of the work, together with the proof, when publication, licensing, or a dispute makes disclosure necessary.

### 4.2 What the notary proves

The notary can establish that:

- A particular data commitment existed no later than a recorded time.
- A particular key submitted or signed that commitment.
- A revealed file belonged to a previously stamped repository root.
- A release descended from a specific earlier state.
- An authorization or licence existed before a derivative was distributed.

It cannot by itself establish that:

- The submitter conceived the work.
- The submitter did not steal it before submission.
- The work is true, novel, ethical, or legally protectable.
- Similarity proves copying.
- A particular person owns every right represented by the data.

The timestamp is evidence of possession and sequence, not an oracle of justice.

### 4.3 Public governance

The notary should not depend on one corporation or model provider. It should use an open protocol, public specifications, independent mirrors, transparent operational policies, and multiple institutional witnesses. Libraries, universities, archives, courts, standards organizations, and public-interest institutions could co-sign periodic checkpoints. Attempts by one operator to rewrite history would conflict with independently retained checkpoints.

Private work should use salted or nonce-based commitments to reduce dictionary attacks against short or predictable content. The system must also support algorithm migration, key rotation, identity recovery, inheritance, pseudonymous creation, and disclosure limited to a relevant Merkle branch.

## 5. Public Chain of Authorship

The notary becomes more useful when individual timestamps are organized into a causal graph.

A **Public Chain of Authorship** would link:

- Creator identity or registered pseudonym.
- Canonical repository identifier.
- Parent repository state.
- Signed approval state.
- Contributor and employment records.
- Model and tool provenance where relevant.
- Public release manifests.
- Commercial licences.
- Authorized derivative repositories.
- Transfers, expirations, and retirements.

The public chain would not require publication of private content. It would publish commitments and relationships. The creator could prove the content later by revealing the relevant records.

An authentic development history would normally contain structured friction: early errors, competing designs, failed experiments, independent criticism, rejected alternatives, and later simplification. Continuous external anchoring makes such a history more credible than a complete narrative manufactured after a dispute arises.

## 6. Commercial licensing as signed descent

A commercial licence would become a signed child record of a canonical repository state. It could identify:

- Licensor and licensee.
- Parent work and repository commitment.
- Permitted medium and market.
- Territory and duration.
- Exclusivity or non-exclusivity.
- Authorized characters, mechanisms, assets, or claims.
- Canonical or noncanonical status.
- Attribution and revenue obligations.
- Modification and sublicensing permissions.
- Expiration, revocation, and dispute terms.

A derivative product would publish its own repository commitment and licence reference. Platforms, customers, distributors, and courts could verify the authorization chain without necessarily reading the private contract or repository.

Revocation would not erase the historical licence. It would append a new status. This preserves an accurate record of what was authorized at the time an action occurred.

## 7. Trademark as verified association

The repo-native approach reinforces the source-identification function of trademarks:

> A party does not own a word in general; it owns and protects a defined association between a mark, a source, specified goods or services, and a commercial lineage.

The public registry could bind a mark to:

- The canonical repository.
- The controlling identity.
- Defined product or service classes.
- Authorized licensees.
- Official and unofficial derivatives.
- Current and historical status.

This would make false claims of origin easier to detect while leaving ordinary language and unrelated uses available. An unauthorized continuation could exist as a commons fork without representing itself as official canon or as commercially authorized by the original creator.

## 8. Ten-year cultural commons proposal

The proposed social bargain is:

> A public creative release receives ten years of exclusive commercial control, after which the released work defaults into a cultural commons under attribution and provenance requirements.

The ten-year period is a policy hypothesis, not a conclusion established in this paper. Its purpose is to provide a meaningful opportunity to recover investment and benefit from creation without allowing permanent control over public culture.

After the exclusivity period:

- The released public work may be adapted and forked.
- The original creator retains attribution and canonical lineage.
- The private, unreleased repository remains private unless separately disclosed.
- Human likeness, identity, confidential information, and unrelated contractual rights remain separately governed.
- Forks must not falsely claim authorization or official canon.
- New derivative repositories establish their own transparent lineages.

The original creator remains advantaged by the depth of the canonical repository: future arcs, rejected alternatives, causal structure, continuity history, and accumulated design judgment. Others may compete, but they do not acquire the original private source merely because the public expression enters the commons.

## 9. Independent Inventor Rights

The central policy innovation is the **Independent Inventor Right**:

> A creator or inventor who demonstrates sufficiently specific, continuous, independently timestamped development before plausible exposure to a competing work should retain defined rights to practice and commercialize that independently developed work, even when another party published or filed first.

This is not a rule that every similar claim receives protection. The claimant must produce a coherent causal lineage.

### 9.1 Minimum showing

An independent inventor should demonstrate:

1. **Specificity:** concrete mechanisms, expressions, designs, or causal relationships—not a vague aspiration.
2. **Temporal anchoring:** external timestamps created before relevant public exposure or documented access.
3. **Continuity:** development across multiple anchored states rather than one isolated deposit.
4. **Correspondence:** a meaningful relationship between the early repository and the later commercial work.
5. **Independent causation:** no evidence that the claimed elements were imported from the competing private or public work.
6. **Contributor clarity:** documented roles, assignments, and identities.
7. **Good faith:** no backfilled, deceptive, or strategically overbroad claim to an undeveloped possibility space.

### 9.2 Effect of the right

A successful showing might establish:

- A right to continue practicing the independently developed invention.
- A defense against suppression by a first filer or first commercial entrant.
- Ownership of the claimant’s own repository lineage and improvements.
- No right to claim official association with the competing lineage.
- No right to use confidential material obtained from the competing repository.
- No automatic ownership of the entire abstract idea or problem domain.

The appropriate scope would require substantial legal and economic study. The principle is coexistence of independent causal trees rather than automatic exclusivity for calendar priority.

## 10. Parallel creation and the Dennis the Menace example

The two unrelated *Dennis the Menace* comics—one developed in the United States and one in the United Kingdom—are a useful cultural example of parallel creation. They appeared in essentially the same release window while arising from separate creators and producing visibly different characters and traditions.

Under a repo-native system, the question would not be resolved merely by determining which publication reached readers first. Each creator could present a separately anchored history:

```text
Creator A → development repo A → public release A
Creator B → development repo B → public release B
```

If neither line descended from the other, both could remain legitimate. Similarity would initiate a provenance inquiry rather than establish liability.

This protects a slower creator whose work was conceived earlier but required more time or capital to release. It also protects a later creator who independently develops a better solution without access to the earlier private work. Commercial strength and filing speed would no longer substitute automatically for causal authorship.

## 11. Conflict resolution by repository evidence

When a conflict arises, an adjudicator should compare causal histories rather than only surface artifacts.

Relevant questions include:

- What specific element is claimed?
- Is it an abstract idea, concrete expression, mechanism, mark, or confidential design?
- When did each repository first contain a sufficiently developed version?
- Were those states independently timestamped?
- Does the history show continuous work or post-dispute reconstruction?
- Could either party plausibly access the other’s work?
- Do unexplained structures appear only after that access?
- Are similarities necessary consequences of solving the same constrained problem?
- Which public releases descend from which private states?
- Were commercial rights properly assigned and licensed?

The best-supported claim would not always be the earliest thin timestamp. A later repository could provide stronger evidence of independent, continuous, specific development. Conversely, hundreds of automatically generated commits should not outweigh one well-supported, contemporaneously witnessed design history.

The standard should therefore evaluate **quality of causal evidence**, not volume of records alone.

## 12. Preventing repository land grabs

A provenance registry could be abused to claim enormous regions of future possibility. A creator might deposit one hundred vague season summaries, thousands of machine-generated inventions, or every obvious variation of a mechanism and later assert ownership when someone else develops one concretely.

The framework must reject these land grabs. Protected scope should depend on:

- Sufficient development and enablement.
- Concrete causal structure.
- Humanly accountable selection or approval.
- Evidence of genuine work rather than indiscriminate generation.
- Correspondence between the claimed scope and demonstrated repository contents.
- Reasonable expiration or disclosure rules for dormant claims.

The system protects developed lineages, not unbounded ownership of themes, genres, problems, styles, or possibility itself.

## 13. Fraud, security, and evidentiary limits

Generative systems can fabricate plausible repository histories. Security must therefore depend on contemporaneous external anchoring rather than the apparent richness of a repository produced after the fact.

Major threats include:

- Theft followed by immediate timestamping.
- Compromised signing keys.
- Identity fraud.
- Synthetic backstory between sparse public checkpoints.
- Collusion by witnesses.
- Hash-algorithm failure.
- Repository hosts modifying or withholding data.
- Employers or contractors disputing ownership.
- Automated claim flooding.
- Strategic secrecy used to surprise legitimate independent developers.

Mitigations include frequent public checkpoints, multiple independent witnesses, hardware-backed keys where appropriate, contributor signatures, clear work-for-hire or assignment records, algorithm agility, rate limits, deposits proportional to claimed scope, and sanctions for fraudulent assertions.

No provenance system can prove the absence of all access. It can create a rebuttable presumption of independent creation when a specific and continuous lineage predates plausible exposure.

## 14. Why the proposal may reduce lawfare

Large organizations already possess legal departments, controlled source systems, contract archives, and extensive communications records. Independent creators often rely on scattered notebooks, personal devices, emails, or recollection. A free public notary would provide basic evidentiary infrastructure to everyone.

Disputes could narrow earlier because the parties can verify:

- Existence dates.
- Exact repository states.
- Chains of title.
- Contributor roles.
- Licence scope.
- Release ancestry.
- Independent or dependent development.

This would not eliminate litigation. Parties would still dispute access, similarity, legal scope, identity, validity, and damages. But objective lineage evidence could reduce the ability of a wealthy first mover to win primarily through uncertainty, discovery cost, or endurance.

The system changes the default from “the larger or earlier commercial actor is presumed legitimate” to “each party must demonstrate the causal history it claims.”

## 15. Research propositions

**P1 — Evidentiary clarity.** Continuously timestamped repositories will reduce factual uncertainty concerning development chronology and licence scope.

**P2 — Parallel-creation protection.** An independent inventor right will reduce wrongful suppression of separately developed works without materially increasing protection for post-exposure copies when specificity and continuity requirements are enforced.

**P3 — Small-creator leverage.** Free public provenance infrastructure will improve the bargaining position of independent creators relative to organizations with established legal-record systems.

**P4 — Reduced dispute cost.** Signed lineage and licence graphs will resolve a meaningful portion of ownership and authorization conflicts before full litigation.

**P5 — Commons innovation.** A ten-year commercial period followed by a provenance-preserving commons will increase derivative innovation while retaining economic value in canonical repositories and official continuity.

**P6 — Fraud resistance through continuity.** Multiple contemporaneous checkpoints and independent witnesses will distinguish authentic development histories from most post hoc synthetic histories more effectively than a single deposit date.

**P7 — Source association.** Binding marks to canonical repository lineages and licensed descendants will reduce consumer confusion without granting ownership of language in general.

## 16. Pilot program

A voluntary pilot could be operated by a consortium of libraries, universities, creator organizations, technical standards groups, and public archives.

The pilot should support:

1. Private salted repository commitments.
2. Public release manifests.
3. Identity-bound and pseudonymous keys.
4. Signed contributor records.
5. Licence and derivative relationships.
6. Merkle inclusion proofs for selective disclosure.
7. Independent timestamp witnesses.
8. Open verification software.
9. A small-dispute forum testing causal-lineage evidence.

Evaluation should measure cost, accessibility, false claims, dispute resolution time, privacy failures, creator adoption, key loss, synthetic-history attacks, and whether repository evidence disadvantages creators who use nontechnical workflows.

Participation must not require Git expertise. A writer should be able to stamp a manuscript folder, an artist a sketchbook scan, an inventor a lab notebook, and a filmmaker a production bible through simple tools that generate the same open proofs.

## 17. If We Are Right — explicitly speculative

If this framework is viable, intellectual property could move away from permanent scarcity at the surface and toward verified stewardship of creative and technical lineage.

Public culture could become more open after a meaningful commercial period. Original creators would retain canonical authority, unreleased work, provenance, official source association, and the commercial value of the deepest repository. Independent creators could compete on the quality of their design rather than their ability to finance immediate release or prolonged litigation. Parallel inventors could coexist when their repositories demonstrate independent causal histories.

The most valuable asset would no longer be merely the finished artifact or the earliest filing. It would be the authenticated repository demonstrating how a body of work came into being, how it changed, who authorized it, and which later works legitimately descend from it.

This would not abolish ownership. It would redefine ownership around truthful lineage, limited exclusivity, accountable association, and contribution to a future commons.

## 18. Conclusion

Generative models make expression increasingly abundant. Intellectual-property systems must therefore become better at distinguishing copying from independent creation, canonical continuity from unauthorized association, and developed work from broad claims over ideas.

The proposed framework combines a canonical repository, public timestamp notary, chain of authorship, signed commercial licensing, a ten-year cultural commons, and independent inventor rights. Its governing principle is:

> Similarity does not establish descent. Rights should follow demonstrated causal lineage, while genuinely independent lineages may coexist.

The proposal requires extensive legal, economic, technical, and institutional refinement. It should begin as voluntary public infrastructure and an empirical research program rather than an immediate replacement for existing law. But it offers a plausible direction for a world in which the visible artifact can be reproduced easily while the authentic process of intelligent design remains valuable.

## References and grounding sources

- Fisher, Matthew John. *Fractal Intent Architecture, Workshop, and repo-native intellectual-property design discussions*. Unpublished working notes, 2026.
- U.S. Copyright Office. [What Does Copyright Protect?](https://www.copyright.gov/help/faq/faq-protect.html). Explains the current distinction between protected expression and unprotected ideas, facts, systems, and methods.
- U.S. Patent and Trademark Office. [What Is a Trademark?](https://www.uspto.gov/trademarks/basics/what-trademark). Explains source identification and that rights do not attach to a word or phrase in general.
- U.S. Patent and Trademark Office. [America Invents Act Highlights](https://www.uspto.gov/patents/laws/america-invents-act-aia/aia-highlights). Background on the current first-inventor-to-file framework.
- Adams, C., Cain, P., Pinkas, D., & Zuccherato, R. [RFC 3161: Internet X.509 Public Key Infrastructure Time-Stamp Protocol](https://www.rfc-editor.org/rfc/rfc3161.html). Internet Engineering Task Force, 2001.
- WIRED UK. [Did *Inside Out* Rip Off *The Numskulls*? The Beano Says No](https://www.wired.com/story/numskulls-inside-out-the-beano-relaunch). Discusses independent cultural similarity and notes the parallel *Dennis the Menace* creations.

## Revision agenda

- Compare the proposal with independent-creation doctrine across jurisdictions.
- Study existing prior-user, trade-secret, defensive-publication, and patent-derivation mechanisms.
- Define the precise legal effect and limits of an Independent Inventor Right.
- Model economic outcomes of ten-year versus alternative commons periods.
- Specify governance for the Public Provenance Notary.
- Produce a technical protocol for identity, commitments, Merkle proofs, licences, and key recovery.
- Run synthetic-history attacks against a prototype.
- Test accessibility with writers, artists, inventors, researchers, and small businesses.
- Invite criticism from IP scholars, archivists, cryptographers, creators, patent practitioners, and open-culture advocates.
