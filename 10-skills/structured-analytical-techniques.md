---
title: "Structured Analytical Techniques & Intelligence Frameworks"
type: skill
tags: [SAT, ACH, diamond-model, kill-chain, mitre-attack, CTI, cognitive-bias, intelligence-analysis]
llms: [claude-sonnet]
status: active
last_updated: 2026-04-09
---

# Structured Analytical Techniques & Intelligence Frameworks

## Purpose

Formal mechanisms for externalising cognitive processes during intelligence analysis — filtering confirmation bias, structuring competing hypotheses, and mapping intrusion events to adversary behaviour. This layer precedes threat modeling and risk quantification in the analytical continuum.

**Use these techniques when:**
- Evaluating raw intelligence with high ambiguity or competing explanations
- Mapping an intrusion event to adversary capability, infrastructure, and intent
- Correlating TTPs across campaigns or attributing activity to a known threat actor

**Feeds into:** [[10-skills/threat-modeling]], [[10-skills/quantitative-risk-management]]

---

## The Analytical Continuum

The full pipeline:

```
Raw Intelligence
      ↓
SATs (bias mitigation, hypothesis testing)
      ↓
Diamond Model (intrusion event taxonomy)
      ↓
Kill Chain / ATT&CK (TTP sequencing and mapping)
      ↓
Threat Modeling (architectural vulnerability mapping)
      ↓
Quantitative Risk Management (financial loss quantification)
```

---

## Structured Analytical Techniques (SATs)

SATs are categorised into three types:

| Category | Purpose | Example Techniques |
|----------|---------|-------------------|
| Diagnostic | Evaluate the quality and validity of evidence | Key Assumptions Check, Quality of Information Check, Indicators of Change |
| Imaginative | Generate alternative perspectives and future scenarios | Outside-In Thinking, Alternative Futures Analysis |
| Contrarian | Formally challenge the prevailing assessment | Red Team Analysis, Devil's Advocacy |

### Cognitive Bias Background

The human brain is predisposed to pattern recognition, leading analysts to project their own mindsets onto foreign adversaries — **mirror-imaging**. Diagnostic SATs deconstruct implicit beliefs. Imaginative and contrarian techniques counteract groupthink and institutional inertia.

### Operational Guide: SAT Execution

| Technique | Category | How-To |
|-----------|----------|--------|
| **Key Assumptions Check (KAC)** | Diagnostic | 1. Assemble cross-functional team. 2. List all premises driving the current assessment. 3. Challenge each: "Why is this believed to be true?" 4. Categorise as solid / unsupported / false. 5. Adjust intelligence trajectory for unsupported assumptions. |
| **Quality of Information Check** | Diagnostic | 1. Aggregate all source data (telemetry, OSINT, HUMINT). 2. Evaluate origin, collection mechanism, and historical reliability. 3. Identify intelligence gaps and potential deception. 4. Annotate reports with confidence levels. |
| **Indicators of Change** | Diagnostic | 1. Define the intelligence target. 2. Establish a list of observable events, technological shifts, or behavioural anomalies that signal a shift in adversary tactics. 3. Monitor telemetry against this list continuously. |
| **Outside-In Thinking** | Imaginative | 1. Map the immediate intelligence problem. 2. Identify macroscopic forces (geopolitical shifts, economic trends, regulatory changes) influencing the threat actor. 3. Analyse how external pressures alter adversary capability or intent. |
| **Alternative Futures Analysis** | Imaginative | 1. Identify core uncertainties in the threat environment. 2. Matrix the two most critical variables to create four future quadrants. 3. Draft adversary operating narratives for each quadrant. |
| **Red Team Analysis** | Contrarian | 1. Isolate a specific threat scenario. 2. Appoint a team to adopt the adversary's exact persona, motivations, and operational constraints. 3. Model how the adversary would bypass current defensive architecture, ignoring internal corporate assumptions. |

---

## Analysis of Competing Hypotheses (ACH)

Developed by Richards J. Heuer Jr. for the CIA. The scientific foundation is **falsification**: rather than seeking evidence to confirm a preferred hypothesis, the analyst evaluates evidence to *refute* hypotheses — mitigating confirmation bias.

**Important limitation:** Empirical decision-science research indicates ACH may not universally mitigate serial position effects. In some control group studies, unstructured analysts occasionally generated more accurate hypotheses. ACH is a rigorous data-structuring mechanism, not a guarantee of analytical accuracy.

### Operational Guide: ACH Execution

**Phase 1 — Scoping and Hypothesis Generation**
Define the intelligence problem precisely. Generate a comprehensive set of mutually exclusive hypotheses covering all plausible explanations.

**Phase 2 — Evidence Aggregation**
Collect all relevant indicators, intelligence reports, and logical arguments. Evaluate each piece of evidence for its **diagnosticity** — its specific capacity to shift relative hypothesis likelihood.

**Phase 3 — Matrix Construction**
Hypotheses on the horizontal axis; evidence on the vertical axis. For each cell, mark the evidence as Consistent / Inconsistent / Neutral relative to the hypothesis.

Example matrix:

| Intelligence Evidence | H1: State-Sponsored APT | H2: Insider Sabotage | H3: Cybercriminal Syndicate |
|-----------------------|------------------------|---------------------|----------------------------|
| E1: Data exfiltrated to unknown foreign IP | Consistent | Inconsistent | Consistent |
| E2: Use of proprietary internal developer tools | Inconsistent | Consistent | Inconsistent |
| E3: Zero-day exploit used for lateral movement | Consistent | Inconsistent | Inconsistent |

**Phase 4 — Hypothesis Elimination**
Focus on evidence that actively *disproves* hypotheses. Eliminate hypotheses with the highest number of inconsistencies. The surviving hypothesis carries the least disconfirming evidence.

**Phase 5 — Sensitivity Analysis**
Evaluate how the conclusion shifts if a single critical piece of evidence is proven false or deceptive.

**Phase 6 — Milestone Tracking**
Define future indicators (signposts) that, if observed, would necessitate re-evaluation of the surviving hypothesis.

---

## Diamond Model of Intrusion Analysis

Established by Caltagirone, Pendergast, and Betz. Models every cyber intrusion as an **atomic event** composed of four interconnected vertices:

```
         Adversary
        /          \
 (socio-political)  (technology axis)
      /                  \
Capability ←————————→ Infrastructure
      \                  /
       ——————————————————
               |
            Victim
```

### The Seven Axioms

| Axiom | Statement |
|-------|-----------|
| 1 | Every intrusion event involves an adversary using a capability over infrastructure against a victim |
| 2 | Events follow an ordered sequence |
| 3 | Capabilities and infrastructure possess directionality |
| 4 | A fully described event populates all four vertices |
| 5 | Adversaries operate under personas |
| 6 | Capabilities may be incomplete but are bounded |
| 7 | **Infrastructure reuse** — adversaries reuse C2 nodes; graph theory links disparate intrusions through shared infrastructure |

Axiom 7 is analytically critical: it enables pivoting across campaigns.

**Extended meta-features:**
- **Socio-political axis:** adversary motivations and intent
- **Technology axis:** specific hardware and software enabling the intrusion
- **Multi-actor extension:** adds a relationship layer for supply chains and RaaS handoffs (e.g., tracking payloads "purchased from" or "leaked from" secondary actors)

### Operational Guide: Pivoting and Activity Threading

**Pivoting** exploits a known vertex feature to discover unknown features via bidirectional edge traversal.

1. Begin with a single verified IOC (e.g., a malicious domain = Infrastructure vertex).
2. Traverse the **Infrastructure → Victim** edge: identify additional compromised networks or delivery mechanisms.
3. Traverse the **Infrastructure → Capability** edge: discover malware payloads hosted on that server.
4. Traverse the **Capability → Adversary** edge: identify the threat actor based on malware signatures or tooling.

**Activity Threading** links chronologically ordered Diamond events to reconstruct the full attack lifecycle:

1. Map events chronologically: reconnaissance → delivery → exploitation → C2 → exfiltration.
2. Identify causal linkages between phases.
3. Cluster multiple activity threads sharing characteristics (identical malware signatures, overlapping C2) into **activity groups** — the analytical representation of an APT campaign.

---

## Cyber Kill Chain

Developed by Lockheed Martin. Models adversary intrusion as a sequential seven-phase chain. Disrupting any phase breaks the chain and defeats the attack.

| Phase | Adversary Action | Defensive Implication |
|-------|-----------------|----------------------|
| 1. Reconnaissance | Harvests target information (OSINT, scanning) | Reduce external attack surface; monitor for pre-attack probing |
| 2. Weaponisation | Creates exploit + payload bundle (e.g., malicious PDF) | Track new exploit kits; monitor threat actor tooling via CTI |
| 3. Delivery | Transmits weapon to target (phishing, watering hole, USB) | Email/web filtering; user awareness training |
| 4. Exploitation | Executes payload, triggers vulnerability | Patch cadence; EDR coverage; application whitelisting |
| 5. Installation | Establishes persistent backdoor/implant | File integrity monitoring; privilege controls |
| 6. C2 (Command & Control) | Adversary establishes remote command channel | Network egress filtering; DNS monitoring; proxy inspection |
| 7. Actions on Objectives | Exfiltration, destruction, lateral movement | DLP; network segmentation; UEBA |

**Relationship to Diamond Model:** The Kill Chain sequences the *phases* of an attack; the Diamond Model structures the *entities and relationships* within each event. Used together: Kill Chain provides temporal ordering, Diamond Model provides analytical depth at each phase.

---

## MITRE ATT&CK Framework

A globally accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. Maintained by MITRE Corporation.

**Structure:**

| Component | Description |
|-----------|-------------|
| **Tactics** (14) | The adversary's tactical objective — the *why* (e.g., Initial Access, Persistence, Lateral Movement, Exfiltration) |
| **Techniques** (~200+) | The specific method used to achieve a tactic (e.g., T1566 Phishing, T1078 Valid Accounts) |
| **Sub-techniques** (~400+) | Granular variants of a technique (e.g., T1566.001 Spearphishing Attachment) |
| **Procedures** | Documented instances of a specific threat actor using a technique |

**Three matrices:**

| Matrix | Scope |
|--------|-------|
| Enterprise | Windows, macOS, Linux, cloud, network, containers |
| Mobile | Android, iOS |
| ICS | Industrial control systems |

**Relationship to Diamond Model:** ATT&CK populates the **Capability** vertex of the Diamond Model with standardised TTP identifiers. A Diamond event with "Capability: T1059.003 (Windows Command Shell)" is immediately actionable — it links to documented detection opportunities, mitigations, and known threat actor usage.

**Relationship to Kill Chain:** ATT&CK tactics map loosely to Kill Chain phases but are more granular. Kill Chain is a high-level campaign model; ATT&CK is an enumeration of specific techniques within those phases.

### Operational Guide: ATT&CK Usage in CTI

**Step 1 — TTP Extraction:** From malware analysis (e.g., `capa` output), PCAP analysis, or incident response findings, extract observed behaviours and map them to ATT&CK technique IDs.

**Step 2 — Navigator Heatmap:** Load technique IDs into ATT&CK Navigator. Overlay the heatmap against the organisation's detection coverage to identify blind spots.

**Step 3 — Actor Profiling:** Cross-reference extracted TTPs against documented threat actor profiles in ATT&CK (e.g., APT28, Lazarus Group). Assess overlap to inform attribution assessments via [[10-skills/ta-attribution-map]].

**Step 4 — Detection Engineering:** Use ATT&CK's documented data sources and detection notes to write detection rules (e.g., Sigma rules, YARA signatures via [[10-skills/yara-generation]]).

**Step 5 — MISP Tagging:** Tag MISP events with `mitre-attack-pattern` galaxy clusters as documented in [[10-skills/threat-intel]].

---

## Quick Reference: Framework Relationships

| Framework | Layer | Primary Output |
|-----------|-------|---------------|
| SATs (ACH, KAC, Red Team) | Intelligence analysis | Validated, bias-mitigated intelligence judgements |
| Diamond Model | Event taxonomy | Structured adversary-capability-infrastructure-victim mapping |
| Cyber Kill Chain | Campaign sequencing | Phase-based attack lifecycle model |
| MITRE ATT&CK | TTP enumeration | Standardised technique IDs, detection opportunities, actor profiles |
| → feeds into → | Threat Modeling | See [[10-skills/threat-modeling]] |
| → feeds into → | Risk Quantification | See [[10-skills/quantitative-risk-management]] |

## Behavioral Analysis Methods Reference

- [[50-knowledge/behavioral-analysis/03-forensic-behavioral]] — behavioral consistency/distinctiveness; linkage logic for ATT&CK attribution
- [[50-knowledge/behavioral-analysis/04-structured-threat-assessment]] — SPJ instruments; structured risk assessment complementing ACH
- [[50-knowledge/behavioral-analysis/07-social-group-behavioral]] — radicalization models; group dynamics underlying adversary behavior
