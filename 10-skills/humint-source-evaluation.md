---
title: "HUMINT Source Evaluation and Intelligence Credibility Assessment"
type: skill
tags: [HUMINT, source-evaluation, intelligence, credibility, admiralty-codes, OSINT, CTI, source-reliability]
llms: [claude-sonnet]
status: active
last_updated: 2026-05-17
---

# HUMINT Source Evaluation and Intelligence Credibility Assessment

## Purpose

Systematic evaluation of the reliability of intelligence sources and the credibility of specific pieces of information. Applies to HUMINT (human intelligence), OSINT, technical intelligence, and CTI source material. Prevents treating all evidence as equally valid — which is the most common and dangerous analytical error.

**Use when:**
- Assessing any intelligence source before incorporating its output into analysis
- Evaluating CTI feeds, dark web forum data, OSINT findings, or informant reports
- Structuring confidence levels in intelligence products
- Writing threat assessments that must convey source quality to decision-makers
- Critically assessing academic literature

**Feeds into:** [[10-skills/structured-analytical-techniques]], [[10-skills/calibrated-estimation]], [[10-skills/threat-research-ioc]], [[10-skills/poi-osint]], [[10-skills/influence-ops-media]]

---

## NATO Admiralty Codes (2x2 Matrix)

The standard professional framework for intelligence source evaluation. Applied across NATO, LE, and intelligence community products worldwide.

### Source Reliability (Letter Code)

| Code | Reliability | Definition |
|------|------------|------------|
| **A** | Completely reliable | No doubt about authenticity, trustworthiness, and competence; history of reliable reporting |
| **B** | Usually reliable | Minor doubts about authenticity or competence; mostly reliable history |
| **C** | Fairly reliable | Doubts about authenticity or competence; approximately half the time has been reliable |
| **D** | Not usually reliable | Significant doubts; more often unreliable than reliable |
| **E** | Unreliable | Lack of authenticity, trustworthiness, and competence; history of unreliable reporting |
| **F** | Reliability unknown (cannot be judged) | Insufficient basis to evaluate; new source with no track record |

### Information Credibility (Number Code)

| Code | Credibility | Definition |
|------|------------|------------|
| **1** | Confirmed | Information confirmed by at least one other independent source; consistent with other known intelligence |
| **2** | Probably true | Logical and consistent with other known intelligence; not confirmed independently |
| **3** | Possibly true | Reasonable; not confirmed; not illogical but is not consistent with other known intelligence |
| **4** | Doubtful | Not credible; inconsistent with other known intelligence |
| **5** | Improbable | No basis in known facts; internally inconsistent or contradicted by multiple sources |
| **6** | Truth unknown (cannot be judged) | Insufficient basis to evaluate this specific piece of information |

**Usage:** Annotate intelligence reports as [Source Code] [Information Code], e.g., **B2** means a usually-reliable source reporting probably-true information.

**Critical rule:** Source reliability and information credibility are evaluated independently. A completely reliable source (A) can produce doubtful information (4) — A4. An unknown source (F) can produce confirmed information (1) — F1 (rare but possible through triangulation).

---

## Source Evaluation Criteria (Beyond the Code)

The admiralty codes compress multi-dimensional assessments into a compact notation. Behind each letter code should be an assessment across these dimensions:

### Access

| Question | Why it matters |
|----------|---------------|
| Did the source have genuine access to the information claimed? | Access assessment prevents laundering: a source who claims to know what happened inside a closed meeting when they were not present has fabricated or been fed the information |
| What was the source's position relative to the information? | Firsthand vs. secondhand vs. hearsay; each layer degrades credibility |
| Is the claimed access plausible given the source's actual role or position? | A low-level technical employee claiming strategic planning knowledge is suspicious |

### Motivation

| Question | Why it matters |
|----------|---------------|
| What does the source gain from providing this information? | Financial payment, revenge, ideology, protection, or coercion all shape what a source will distort |
| Is the source motivated to embellish, minimise, or fabricate? | A source reporting on their own organisation has motivation to protect it; a disgruntled ex-employee has motivation to damage it |
| Has the source's motivation changed since their track record was established? | A source that was reliable when paid may become unreliable when payment stops |

### Corroboration

| Question | Why it matters |
|----------|---------------|
| Can the specific claim be independently verified? | If yes, do so before assigning credibility code 1 or 2 |
| What other independent sources report consistent or contradictory information? | Consistency with multiple independent sources upgrades credibility; contradiction downgrades it |
| Are the corroborating sources genuinely independent? | Sources fed from the same primary source are not independent — this is the echo chamber error |

### Consistency

| Question | Why it matters |
|----------|---------------|
| Is this information consistent with the source's prior reporting? | Sudden inconsistency with prior reliable reporting is a deception indicator |
| Is this information internally consistent? | Internal contradictions within a single report are a fabrication or confusion indicator |
| Is this information consistent with established technical or contextual knowledge? | If a source reports malware capabilities that are technically impossible, the report is wrong regardless of source reliability |

---

## Fabrication and Deception Indicators

| Indicator | Interpretation |
|-----------|---------------|
| **Overly specific operational detail** | Well-defined detail that the source could not plausibly possess; fabrication or plant |
| **Flatly contradicts technical evidence** | Source reporting on technical events that are inconsistent with physical or forensic evidence; source is wrong or lying |
| **Mirrors the consumer's expectations** | Source reporting exactly what the consumer expects to hear; confirmation bias exploitation or intelligence-to-please |
| **No access mechanism** | Cannot explain how they came to know what they claim; probable fabrication or secondhand source misrepresented as firsthand |
| **Escalating specificity under pressure** | Details become more precise as questioning increases rather than becoming less certain; confabulation or coached source |
| **Information that only benefits the source** | Reporting that steers the consumer toward action that benefits the source's interests without being disclosed |
| **Single-source isolation** | Information that cannot be corroborated by any independent source and makes significant analytical claims; hold until corroborated |

---

## OSINT and CTI Source Evaluation

Standard admiralty codes apply to open-source and technical intelligence with adaptations:

| OSINT Source Type | Reliability Notes |
|-------------------|------------------|
| **Primary source documents** (leaked, official) | Assess authenticity first; if authentic, reliability of the document depends on who created it and for what purpose |
| **Social media** | F-code default for unknown accounts; consistent account history and behavioral coherence upgrade toward C or B |
| **CTI feed (commercial)** | Evaluate collection methodology, false positive rate, and known biases; B2 is a reasonable starting assumption for reputable vendors |
| **Dark web forum posts** | D or F by default; motivation to deceive is high (competitive intelligence, trolling, disinformation); corroborate independently before incorporating |
| **Journalist reporting** | Assess publication, journalist track record, whether sources are named or anonymous, whether the claim is corroborated within the article |
| **Academic literature** | Peer-reviewed ≠ true; assess methodology, sample size, replication status, and conflicts of interest; B1-B2 for high-quality replication; C3 for single studies in small samples |

**Specific CTI context — IOC reliability:**
- Self-reported IOCs from vendors: assess their visibility and collection methodology
- Community-shared indicators (MISP): assess the original submitter's reliability rating
- Infrastructure IOCs persist longer than host-based; host-based may be reused or shared across unrelated actors
- False positive rate matters: a high-confidence IOC that generates 90% false positives in your environment is operationally useless regardless of source quality

---

## Triangulation Methodology

Triangulation is the process of converging on a conclusion using multiple independent sources, each with different access mechanisms and potential biases.

**Principle:** If three independent sources — each with different access, different motivations, and different potential biases — all report consistent information, the credibility of that information is substantially higher than any single source could provide.

**Independence test:** Two sources are genuinely independent only if:
1. They obtained their information through different access pathways
2. They were not both fed by the same upstream source
3. They have no shared motivation to report the same false information

**Triangulation failure modes:**
- **Echo chamber:** multiple sources all trace to one original source
- **Coordinated deception:** multiple sources are all under the control of an adversary who feeds them consistent false information (active measures)
- **Confirmation cascade:** analysts preferentially collect sources that confirm the prevailing assessment

**Practical approach:** When triangulating, explicitly map where each source obtained their information. Draw the source graph. Echo chamber structures are visible in the graph before they contaminate the assessment.

---

## Source Evaluation in Practice — Annotated Example

**Scenario:** A CTI report claims APT-X deployed a new variant of malware Y against targets in sector Z.

```
Source evaluation:

Source: Commercial CTI vendor (pseudonym)
  — Reliability: B (usually reliable; track record of accurate TTPs attribution; 
    two prior reports confirmed by independent analysis)
  — Access: Has visibility into the specific sector from endpoint sensors 
    (claimed and plausible given their customer base)
  — Motivation: Financial (report drives product sales); some incentive to 
    overstate severity; no specific reason to fabricate actor attribution
  — Code: B

Information credibility:
  — Claim: APT-X deployed variant of malware Y
  — Corroboration: Malware hash matches a sample analysed independently; 
    infrastructure IOCs partially overlap with prior APT-X campaign (Diamond 
    Model consistency)
  — Inconsistency: Targeting sector Z is new for APT-X; prior activity focused 
    on sector W — noted as anomaly requiring explanation, not contradiction
  — Code: 2 (probably true, not independently confirmed on actor attribution)

Combined: B2

Caveat: Targeting sector Z is novel for this actor. Either (a) actor is 
expanding mandate, (b) victim is misattributed to sector, or (c) actor 
attribution is partially wrong. Monitor for additional corroboration.
```

---

## Quick Reference — Admiralty Codes

```
Source reliability:
A — completely reliable
B — usually reliable
C — fairly reliable
D — not usually reliable
E — unreliable
F — unknown

Information credibility:
1 — confirmed (independent corroboration)
2 — probably true (consistent, not confirmed)
3 — possibly true (not illogical, not confirmed)
4 — doubtful (inconsistent with known intelligence)
5 — improbable (contradicted or physically impossible)
6 — unknown

Format: [letter][number] — e.g., B2, C3, A1, F6
```
