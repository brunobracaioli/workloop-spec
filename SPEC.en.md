# Workloop Spec

**Agentic Workloop Specification**

| | |
|---|---|
| Version | 0.1.0-rc5 (draft for review) |
| Status | Draft · Request for Comments |
| Date | 2026-08-18 |
| Author | Bruno Bracaioli · B2 Tech · AISAC protocol |
| Canonical URL | https://workloop.b2tech.io |
| DOI | https://doi.org/10.5281/zenodo.22004648 |
| License | CC BY 4.0 |
| Repository | https://github.com/brunobracaioli/workloop-spec |

## Summary

An **agentic workloop** is a system of two or more agentic loops that interact through explicit channels. When all participants are under one policy authority (the organization that created them), the workloop is **governed**, and this specification requires that no inter-loop interaction and no externally effecting action occur without passing through a deterministic gate that enforces that authority's policies and business rules. When the graph crosses the authority boundary, the workloop is **open** and defensive rules apply. This document defines the terms, the invariant ("freedom inside the loop, a deterministic gate at every interface"), corollaries, operational requirements, and conformance criteria.

## Abstract

An **agentic workloop** is a system of two or more agentic loops that interact through explicit channels. When every participant sits under one policy authority (the organization that created them), the workloop is **governed**: no inter-loop interaction and no externally effecting action may occur without passing through a deterministic gate that enforces that authority's policies and business rules. When the graph crosses the authority boundary, the workloop is **open** and defensive rules apply. This specification defines the terms, the invariant ("freedom inside the loop, a deterministic gate at every interface"), corollaries, operational requirements, and conformance criteria.

## 1. Motivation

Agentic loops—processes in which a model decides actions and uses tools until it stops—are no longer isolated units. In real operation, a customer-service loop writes to the CRM that another loop reads; a media loop publishes what another loop comments on; one loop asks another to execute what it cannot execute itself. This is where compliance is lost. Inside a loop, prompts, skills, and instructions are non-deterministic policy: the model may or may not follow them. The organization needs a place where policy is enforced by code, not requested by prompt. That place is the interface: between loops and between a loop and the world.

Existing vocabulary does not cover this object. "Agent loop" describes a loop. "Agentic workflow" describes a process with model steps inside a single runtime. "Agent mesh" describes traffic, identity, and routing infrastructure between agents. None names the *system of autonomous loops governed by business rules at the interface*. **Workloop** names this system, in direct opposition to workflow: a workflow is the acyclic graph owned by a runtime; a workloop is a system of loops that interact under one authority.

A governed agentic workloop is what is often called an "AI-operated company," with a precision that popular usage omits: the operation is agentic; governance is human and deterministic. Loops execute; the authority defines policies, the envelope, and escalation; meta-loops (DEF-14) improve the system within the envelope. This specification neither describes nor permits an organization in which the model defines its own policy. The thesis, in two sentences: probabilistic autonomy for thinking; deterministic governance for acting.

## 2. Conventions and terminology

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** correspond respectively to MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY as described in RFC 2119 and RFC 8174, and have normative meaning only when written in uppercase, including inflected forms (MUST, MAY).

Identifiers: `DEF-n` (definitions), `INV-n` (invariant), `COR-n` (corollaries), `REQ-n` (operational requirements), `OPEN-n` (open workloop), and `CONF-n` (conformance). Refer to clauses by identifier.

"Model" means any component whose output cannot be verified statically, typically a language model, regardless of its temperature or how predictable it may seem.

Sections marked *informative* create no obligations.

## 3. Definitions

**DEF-1 · Agentic loop.** An autonomous process with its own trigger (event, schedule, or message) and its own lifecycle, in which a model iteratively decides actions (including tool use and message emission) until a stopping condition. It may be durable (state persisted across failures) or not; durability is not definitional.

**DEF-2 · Policy authority.** The organization, or unit of it, that creates and operates loops and whose policies and business rules must be enforced. A participant is *under* the authority when the authority can change, interrupt, and inspect it.

**DEF-3 · Channel.** An explicit medium through which loops interact: (a) a directed message; (b) a published and consumed event; or (c) *mediated* shared state: a repository, database, file, or service whose access passes through a mediator that applies a gate. Shared state without a mediator is not a channel (see COR-3).

**DEF-4 · Interface.** A point where an interaction crosses the boundary of a loop or a workloop (DEF-13): emission of a message or event, writing to shared state, or an action with external effect. This is where the gate resides. Do not confuse this with a programming or user interface: here, interface means the gated boundary of a loop or workloop.

**DEF-5 · Action with external effect.** Any action whose effect is observable outside the loop: a message sent, a record written, a publication, a transaction, or a call to a third-party system.

**DEF-6 · Deterministic gate.** A computable predicate evaluated at the interface whose result is *allow*, *block*, or *escalate*, and whose value is a function only of deterministic state (schema, allow-lists, effective chain authority, budget, hop count, time window, provenance) and never of a model's judgment. Deterministic means: same input, same result; testable; reproducible in an audit.

**DEF-7 · Rule decidable at the interface.** A business rule whose violation can be detected by a deterministic gate from the message or action and the available state: structural, quantitative, authorization, temporal, and provenance rules. A **non-decidable rule** requires semantic interpretation: suitability, truthfulness, tone, or an implicit promise.

**DEF-8 · Effective chain authority.** The set of permissions resulting from the intersection of the authorities of the loops along the delegation chain that originated an action. It is never greater than the originator's authority.

**DEF-9 · Workloop contract.** A specification of the interface of a loop, or of a composite workloop at the workloop level (DEF-13): input and output schemas, declared actions with external effect, authority scope, budgets (cost, hops, rate), and applicable gates.

**DEF-10 · Agentic workloop.** A system of two or more agentic loops that interact through channels. It MAY include non-agentic components (services, APIs, deterministic workflows, and mediators) that participate in channels and interfaces without being loops; the term covers the whole system.

**DEF-11 · Governed agentic workloop.** A system of two or more agentic loops that interact through explicit channels (message, event, or mediated shared state), under one policy authority (the organization that created them), in which no inter-loop interaction and no action with external effect occurs without passing through a deterministic gate that enforces that authority's policies and business rules.

**DEF-12 · Open workloop.** A workloop whose graph crosses the authority boundary; the operator places gates only on its own arcs and must enforce termination and self-origin marking on every output.

**DEF-13 · Composite workloop.** A workloop whose participants include other workloops. Each participating workloop exposes a contract (DEF-9) at the workloop level, not only at the level of its loops. Three interfaces are distinguished: internal (between loops in one workloop), between workloops (the boundary of a participating workloop), and external (the authority boundary, section 7). The invariant and corollaries apply at every level. A participating workloop's authority is a subset of the authority of the workloop containing it (COR-1).

**DEF-14 · Meta-loop.** An agentic loop whose outputs alter other loops (prompts, parameters, models, content, schedules, or budget allocation within caps) based on data from the workloop itself. It is governed by REQ-6.

*Note.* "Governed" and "open" describe the scope of authority over the graph. "Conformant" describes satisfaction of this specification (section 8). A governed workloop that violates the invariant is not conformant; it remains governed.

## 4. Invariant: freedom inside the loop, a deterministic gate at every interface

The model is free inside the loop. Nothing crosses an interface without a deterministic gate. In one line: probabilistic autonomy for thinking, deterministic governance for acting.

**INV-1** Every interaction between loops MUST occur through an explicit channel (DEF-3).

**INV-2** Every interaction between loops and every action with external effect MUST pass through at least one deterministic gate (DEF-6) at the interface.

**INV-3** A gate's predicate MUST be a function only of deterministic state and MUST NOT depend on a model's judgment. Model-based verification MAY exist as an additional layer, but it does not count as a gate.

**INV-4** A gate MUST NOT be bypassable, disableable, or rewritable by the loop it governs. The gate resides outside the model's control (hook, mediator, proxy, or platform policy), and there MUST NOT be an ungated path to the same interface.

**INV-5** The authority MUST classify its business rules as decidable or non-decidable at the interface (DEF-7). Decidable rules MUST be enforced by a gate. Non-decidable rules MUST be converted into structure whenever possible (enumerated actions, typed outputs, templates with validated variables) and, for what remains, treated as probabilistic (model verification and/or human review), with mandatory human escalation above an impact threshold defined by the authority. Non-decidable rules MUST NOT be declared guaranteed.

**INV-6** The deterministic layer alone MUST limit the system's maximum harm (the envelope): if all probabilistic layers fail, no action outside the envelope is possible.

## 5. Corollaries

**COR-1 · Authority attenuation.** The effective authority of an action is the intersection of the authorities along the chain (DEF-8). A loop MUST NOT obtain, by delegating to another, permission it does not possess. Gates MUST evaluate the effective authority of the chain, not only that of the executing loop. Attenuation also applies to the composition hierarchy (DEF-13): a participating workloop never has greater authority than the workloop containing it. This requires every interaction to carry its origin (COR-2).

**COR-2 · Traceability.** Every interaction MUST carry an origin identifier (originating loop and authority) and an end-to-end trace identifier, propagated at every hop. Every gate decision MUST be recorded with: timestamp, trace, interface, gate, evaluated input (or its hash), result, and version of the applied policy. The gate-decision log is the system's conformance artifact.

**COR-3 · Implicit channel is a defect.** An interaction between loops outside a gated channel, through unmediated side effects in files, records, publications, or any shared state without a mediator, is an architecture defect, not an integration issue. Conformant systems MUST mediate all shared state through a gate or prevent direct access.

## 6. Operational requirements

**REQ-1 · Termination.** Every conversation between loops MUST have a hop and/or cost budget, and a cooldown per pair (origin, destination) and per subject; gates MUST block or escalate when limits are exceeded. Model loops do not stop on their own.

**REQ-2 · Provenance and contamination.** Messages between loops MUST separate data from instructions through typed structure. Content originating outside the authority MUST carry a provenance label, and gates MAY restrict downstream actions when such content is present. Gates do not detect injection; they limit what it can reach.

**REQ-3 · Idempotency and concurrency.** Actions with external effect MUST be idempotent or protected by an idempotency key. Concurrent access to shared state MUST be serialized (lease or lock) or convergent.

**REQ-4 · Published contract.** Every loop MUST expose its workloop contract (DEF-9), and the contract MUST be versioned.

**REQ-5 · Interruption.** The authority MUST be able to interrupt any loop and any channel through a mechanism independent of the model, and this capability MUST be tested periodically.

**REQ-6 · Meta-loop and self-improvement.** Every output of a meta-loop (DEF-14) that alters another loop is an action with external effect (DEF-5) and MUST pass through a gate. Changes to policies, gates, contracts, or the envelope (INV-6) MUST NOT be executed by a meta-loop; they MUST pass through a policy-change interface with human authority, versioning, and logging (COR-2). Self-improvement is permitted within the envelope; the envelope cannot modify itself. A meta-loop MUST NOT alter the gates that govern it (INV-4).

## 7. Open workloop

When the graph crosses the authority boundary:

**OPEN-1** The operator MUST apply a deterministic gate to every output arc under its control, treating every output as potentially closing a cycle.

**OPEN-2** The operator MUST mark the self-origin of every output: out-of-band metadata where the medium preserves it (email or HTTP headers, trace context, trailers), and an in-band marker where it does not; and MUST recognize its own marker on input, treating it as a return.

**OPEN-3** The operator MUST enforce termination (hop budget, cooldown) and MUST monitor the medium for recurrence (rate, near-duplicates), because markers do not survive third-party semantic transformation.

**OPEN-4** The operator MUST NOT assume end-to-end observability or trust a third-party gate.

**OPEN-5** Every output from a governed workloop to outside the authority is an open-workloop interface and MUST comply with OPEN-1 through OPEN-4.

## 8. Conformance

**CONF-L · Conformant loop.** A loop is conformant when it: exposes a versioned contract (REQ-4); sends every output through a gate (INV-2, INV-3, INV-4); propagates origin and trace (COR-2); makes its actions with external effect idempotent (REQ-3); respects budgets (REQ-1); and can be interrupted through a mechanism independent of the model (REQ-5).

**CONF-S · Conformant system.** A governed workloop is conformant when every interface has a gate at all three levels (INV-1, INV-2, DEF-13); the rule classification is published and the envelope defined (INV-5, INV-6); gates evaluate the effective authority of the chain and hierarchy (COR-1); the decision log is complete (COR-2); there is no unmediated shared state (COR-3); every meta-loop complies with REQ-6; and its external interfaces comply with section 7.

**CONF-D · Declaration.** "Conformant with Workloop Spec 0.1.0" MAY be claimed only when all applicable MUSTs are satisfied and verifiable by evidence: gate tests and the gate-decision log.

## 9. What is not a workloop

*Informative.*

- A single agentic loop, even with hooks. Hooks are intra-loop gates and the direct precedent for this specification, but a loop is not a workloop.
- A workflow with a cycle inside a single runtime whose nodes have no independent trigger and lifecycle (a state graph with model nodes, or an orchestrated pipeline). It is an agentic workflow.
- Event-driven integration with no model-decided arc (sagas, ETL, deterministic automations). It may form a workloop; it is not agentic.
- Third-party loops interacting with yours when you do not control their policy. It is not governed; it is an open workloop (section 7).
- An organization in which the model defines its own policy. It is outside this specification.

## 10. Canonical example

*Informative.*

A company operates three loops:

- **L1 · Customer service**: receives messages (WhatsApp, DM), qualifies them, and writes the lead to the CRM.
- **L2 · Offers**: reads qualified leads, decides on the offer, and sends the proposal, which may include a discount.
- **L3 · Media**: publishes content, responds to comments, and routes interested parties to L1.

**Channels.** The CRM is mediated shared state (a mediator gates every write and read); an event bus (`lead.qualified`, `offer.sent`, `comment.interested`); and direct L1→L2 messages for requests.

**Decidable gates.** Lead schema; recipient allow-list with opt-in; discount cap by profile; time window; daily message budget; hop budget per conversation; rate per recipient.

**A non-decidable rule converted into structure.** "Do not promise what you cannot deliver" is not decidable. L2 sends only approved templates with validated variables (value and time within ranges); it does not write free text at the interface. What remains semantic goes through probabilistic review and, above the impact threshold, a human.

**Chain authority (COR-1).** L1 has no discount permission. If L1 asks L2 to "offer 30%," L2's gate evaluates the effective authority (origin L1, with no discount permission) and blocks or escalates. L2 grants a discount only when the chain authorizes it.

**Traceability (COR-2).** A single trace connects the initial DM, the CRM lead, and the offer sent; each gate records its decision with the policy version.

**Defect (COR-3).** If L3 reads the spreadsheet that L1 writes directly, without a mediator, it is an implicit channel. Correction: mediate the spreadsheet or replace it with an event.

**Open interface (section 7).** A third-party bot comment on L3's post is input from outside the authority; REQ-2 labels its provenance. L3's response is an output outside the authority; it complies with OPEN-1 through OPEN-4.

**Composition (DEF-13).** The three loops form a sales domain workloop. The company operates others (paid media, content production, data) that compose with this one; the interface between workloops has a gate and a workloop-level contract, and each one's authority is a subset of the company's authority.

**Meta-loop (DEF-14, REQ-6).** A data loop reads gate logs and the results of the other loops and adjusts, within the envelope, L1 prompts, L2 active templates, and L3 schedules. When it concludes that the discount cap should rise, it does not alter the gate: it emits a proposal to the policy-change interface, which a human approves and versions.

## 11. Relation to prior work

*Informative.*

- **Code-agent hooks** (for example, in Claude Code): deterministic code executed at points in the cycle, capable of blocking an action independently of what the model decided. This is the intra-loop gate; this specification extends the idea to the interface between loops.
- **Policy as code and admission control** (OPA, Cedar, Kubernetes admission controllers): a deterministic predicate evaluated outside the governed component. The same separation principle, here applied to business rules.
- **Service mesh, agent mesh, and agent gateways**: traffic, identity, and routing policy between services and agents. Infrastructure. This specification addresses domain policy at the interface and is complementary.
- **Classical multi-agent systems** (MAS, FIPA): communication and coordination between agents. This specification assumes an opaque model and focuses on enforcement.
- **Loop prevention in distributed systems**: RFC 3834 (automatic responses), hop counting in SMTP, recursion detection in serverless platforms, and the GitHub Actions rule for events generated by `GITHUB_TOKEN`. Precedents for the OPEN clauses.
- **CaMeL** (Debenedetti et al., 2025): capabilities and deterministic policies over data flow against prompt injection. Precedent for REQ-2.
- **Confused deputy and capability attenuation** (Hardy, 1988; object-capability model). Precedent for COR-1.

## 12. Name, license, and citation

**Name.** "Workloop" and "agentic workloop" are terms of the AISAC protocol (Bruno Bracaioli / B2 Tech). Use them freely with attribution to this specification. The term is not trademarked.

**License.** This text is licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0). You may copy, redistribute, adapt, and use it commercially, provided that you attribute the authorship and indicate changes.

**How to cite.** Bracaioli, B. (2026). *Workloop Spec: Agentic Workloop Specification* (version 0.1.0). B2 Tech / AISAC protocol. DOI: 10.5281/zenodo.22004648. Canonical URL: https://workloop.b2tech.io. Repository: https://github.com/brunobracaioli/workloop-spec.

## 13. Versioning this specification

This specification follows Semantic Versioning: **MAJOR** for incompatible changes to core definitions (DEF-10 through DEF-13) or the invariant; **MINOR** for new requirements or corollaries and compatible extensions; **PATCH** for editorial corrections. Drafts use the `-rcN` suffix. Every change is recorded in `CHANGELOG.md`.

## Appendix A: Conformance checklist

| Item | Clause | Expected evidence |
|---|---|---|
| Every interaction between loops occurs through an explicit channel | INV-1 | Channel inventory; no direct access to shared state |
| Every interface has a deterministic gate | INV-2 | Interface × gate map |
| No gate depends on model judgment | INV-3 | Gate code; determinism tests |
| Gates cannot be bypassed by the governed loop | INV-4 | Gate location outside the model runtime; no ungated path |
| Rules classified; envelope defined | INV-5, INV-6 | Classification document; envelope limits |
| Gates evaluate effective chain authority | COR-1 | Origin propagation; blocked-delegation tests |
| Origin and trace propagated; decision log complete | COR-2 | End-to-end trace sample; log with policy version |
| No unmediated shared state | COR-3 | Access audit |
| Hop, cost, and cooldown budgets | REQ-1 | Configuration and over-budget conversation test |
| Data separated from instruction; provenance labeled | REQ-2 | Message schemas; labels |
| Idempotency and serialization | REQ-3 | Idempotency keys; leases |
| Contracts published and versioned | REQ-4 | Contracts by loop |
| Model-independent interruption, tested | REQ-5 | Interruption test record |
| Interfaces between workloops have a gate and workloop-level contract | DEF-13, REQ-4 | Contracts by workloop; interface map between workloops |
| Meta-loops change only within the envelope; policy changes use the human interface | REQ-6 | Meta-loop output log; policy-change record with approver and version |
| External interfaces comply with OPEN-1 through OPEN-4 | Section 7 | Self-origin marking; recurrence monitoring |
