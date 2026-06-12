---
title: "Infosec Report & Blog Writing Pipeline"
type: skill
tags: [writing, threat-report, blog, advisory, malware-analysis, policy-brief, pandoc, mermaid, agentic, infosec-writing]
llms: [claude-sonnet, claude-opus]
status: active
last_updated: 2026-04-08
---

# Infosec Report & Blog Writing Pipeline

## Purpose

Agentic pipeline for producing any infosec document type — from flash alerts to annual threat reports to policy briefs — from raw analyst notes, IOC data, or session artifacts. Supports single-format and multi-format generation from one input. Outputs structured Markdown compiled to PDF, HTML, or Word via Pandoc.

## Compatible LLMs

| LLM | Role |
|-----|------|
| claude-sonnet | Primary — orchestration, section writing, formatting |
| claude-opus | Executive summaries, narrative coherence, policy language, editorial pass |

---

## Document Type Registry

### Threat Intelligence

| Format | Code | Length | Audience |
|--------|------|--------|----------|
| Flash report / alert | `flash` | 1–2 pp | SOC, ISAC members (urgent) |
| Intelligence bulletin | `intel-bulletin` | 2–4 pp | ISAC partners, government |
| Threat advisory | `advisory` | 2–5 pp | Defenders, sysadmins |
| Situation report | `sitrep` | 1–3 pp | IR teams, management |
| Campaign report | `campaign-report` | 5–15 pp | Technical analysts |
| Threat actor profile | `actor-profile` | 10–30 pp | Senior analysts, government |
| Annual threat report | `annual-report` | 30–80 pp | CISO, executives, press |

### Malware & Vulnerability Research

| Format | Code | Length | Audience |
|--------|------|--------|----------|
| Malware analysis report | `malware-report` | 5–20 pp | Analysts, IR teams |
| Reverse engineering write-up | `re-writeup` | 3–10 pp | Technical peers |
| CVE / vulnerability advisory | `cve-advisory` | 2–5 pp | Vendors, defenders |
| Exploit technical analysis | `exploit-analysis` | 5–15 pp | Security researchers |
| YARA / Sigma rule documentation | `rule-doc` | 1–2 pp | Detection engineers |

### Practitioner & Public Comms

| Format | Code | Length | Audience |
|--------|------|--------|----------|
| Technical blog post | `tech-blog` | 800–3,000 w | Peer practitioners |
| Strategic blog post | `strategic-blog` | 600–1,500 w | CISO, policymakers |
| Whitepaper | `whitepaper` | 15–40 pp | Customers, industry |
| Case study | `case-study` | 5–15 pp | Sales-adjacent, customers |
| Executive summary | `exec-summary` | 300–600 w | Non-technical leadership |

### Policy & Regulatory

| Format | Code | Length | Audience |
|--------|------|--------|----------|
| Policy brief | `policy-brief` | 2–4 pp | Regulators, parliament staff |
| Public consultation response | `consultation` | Variable | Regulatory bodies |
| Expert witness statement | `expert-witness` | 10–30 pp | Courts, parliamentary committees |

---

## Section Templates

Each template defines mandatory sections (M), recommended sections (R), and optional sections (O).

---

### `flash` — Flash Report / Alert

```markdown
# [TLP:COLOUR] FLASH: [SUBJECT] — [DATE]
**Tracking ID:** FLASH-YYYY-NNN | **Severity:** CRITICAL/HIGH/MEDIUM
**Issued:** YYYY-MM-DD HH:MM UTC | **Valid until:** HH:MM UTC or FURTHER NOTICE

## (M) What Happened                          (~100 words)
2–3 sentences. What, when, confirmed impact.

## (M) Who Is Affected
Affected systems, sectors, versions. Explicit scope statement.

## (M) Immediate Actions Required             (numbered list)
1. [Action within 1 hour]
2. [Action within 24 hours]
3. [Action within 72 hours]

## (M) Indicators (Abbreviated)
IP / domain / hash — one line each. Full IOC list in linked report if available.

## (R) Technical Context                      (~150 words)
Minimal: attack vector, exploit used, malware family if known.

## (M) Reporting & Contact
Who to notify. Escalation path. Next update expected at: [time].
```

---

### `intel-bulletin` — Intelligence Bulletin

```markdown
# [TLP:COLOUR] Intelligence Bulletin [REF-YYYY-NNN]
**Date:** YYYY-MM-DD | **Distribution:** [list] | **Handling:** [TLP instructions]

## (M) Summary                                (~200 words)
What this bulletin covers and why it matters now.

## (M) Background
Context: prior activity, related campaigns, threat actor history.

## (M) Current Intelligence
What is new or newly confirmed. Distinguish assessed from confirmed.

## (M) Analysis
Analyst assessment: intent, capability, likely next steps.
Confidence level: HIGH / MODERATE / LOW — state basis.

## (M) Implications
So-what for the distribution audience specifically.

## (M) Recommended Actions
Prioritised, audience-appropriate.

## (R) Sources & Methods Note
General characterisation of sources without burning specifics.

## (M) Handling Instructions
TLP level, permitted sharing, caveats.
```

---

### `advisory` — Threat Advisory

```markdown
# [TLP:COLOUR] Security Advisory: [SUBJECT]
**Date:** YYYY-MM-DD | **Severity:** [CVSS/qualitative] | **Version:** 1.0

## (M) Executive Summary                      (~200 words)
Non-technical. What the threat is, who is at risk, what to do.

## (M) Affected Products / Systems
Table: Product | Version | Status (Vulnerable / Patched / Unconfirmed)

## (M) Threat Description
How the threat works. Plain language. Link to technical details below.

## (R) Attribution
If known or assessed. Confidence level explicit.

## (M) Indicators of Compromise
Table per type: IP addresses | Domains | File hashes | URLs
Each row: indicator | type | context | first seen | last seen

## (M) Mitigation and Remediation             (numbered, prioritised)
1. Immediate mitigations (no patch required)
2. Patch / update instructions
3. Detection and monitoring guidance

## (R) Detection Opportunities
Sigma / Suricata / YARA rules inline or linked.

## (M) References
CVE links, vendor advisories, MITRE ATT&CK techniques cited.
```

---

### `sitrep` — Situation Report

```markdown
# SITREP [NNN] — [INCIDENT NAME]
[TLP:COLOUR] | Period: YYYY-MM-DD HH:MM to HH:MM UTC | Issued by: [team/analyst]

## (M) Situation Overview                     (3–5 sentences)
Current state. Scope confirmed so far.

## (M) Current Status
- Containment status: [contained / partially contained / uncontained]
- Affected systems: [count and type]
- Affected users: [count or unknown]
- Data at risk: [confirmed / suspected / ruled out]

## (M) Actions Taken Since Last SITREP
Chronological bullet list. Each bullet: [HH:MM UTC] Action.

## (M) Pending Actions
Owner | Action | ETA

## (M) Key Risks
What could get worse and under what conditions.

## (R) Resource Requirements
What additional resources, approvals, or external help is needed.

## (M) Next Update
Next SITREP at: [time]. Escalation trigger: [condition].
```

---

### `campaign-report` — Campaign Report

```markdown
# [TLP:COLOUR] [CAMPAIGN NAME] — Campaign Intelligence Report
**Date:** YYYY-MM-DD | **Version:** 1.0 | **Classification:** [TLP]

## (M) Executive Summary                      (300–500 words)
Key findings. Who, what, when, impact, confidence. Non-technical.

## (M) Key Findings                           (5–8 bullets)

## (M) Campaign Overview
Background context. How this campaign was identified. Scope and scale.

## (R) Threat Actor Attribution
Aliases, suspected origin, motivation. Confidence: HIGH / MODERATE / LOW.

## (M) Campaign Timeline
Table: Date | Event | Evidence | Confidence

## (M) Technical Analysis
### Initial Access
### Execution & Persistence
### Privilege Escalation & Defense Evasion
### Lateral Movement
### C2 Infrastructure
### Exfiltration / Impact

## (M) MITRE ATT&CK Mapping
Table: Tactic | Technique ID | Technique Name | Evidence / Example

## (M) Indicators of Compromise
### Network Indicators
### Host-Based Indicators

## (R) Detection Opportunities
Sigma rules, Suricata rules, YARA rules — with detection rationale.

## (M) Recommendations
### Immediate (0–72 hours)
### Short-term (1–4 weeks)
### Strategic (1–6 months)

## (M) References & Sources
```

---

### `malware-report` — Malware Analysis Report

```markdown
# [TLP:COLOUR] Malware Analysis Report: [MALWARE NAME / FAMILY]
**Date:** YYYY-MM-DD | **Analyst:** [name] | **Version:** 1.0
**Sample SHA256:** [hash]

## (M) Executive Summary                      (~300 words)

## (M) Sample Metadata
| Field | Value |
|-------|-------|
| SHA256 | |
| File type | |
| Compile timestamp | |
| Packer / protector | |
| First seen | |

## (M) Static Analysis
### File Structure & Headers
### Strings of Interest
### Import Table & Capabilities
### Packers, Obfuscation, Anti-Analysis

## (M) Dynamic Analysis
### Execution Behaviour Overview
### Network Activity
### File System Modifications
### Persistence Mechanisms

## (R) Code Analysis
Key functions with annotated pseudocode.

## (M) MITRE ATT&CK Mapping
Table: Tactic | Technique ID | Technique | Evidence

## (M) YARA Rules

## (M) Indicators of Compromise
Network, host-based, behavioural.

## (M) Detection & Remediation Guidance
```

---

### `policy-brief` — Policy Brief

```markdown
# [SUBJECT] — Policy Brief
**Date:** YYYY-MM-DD | **Audience:** [regulators / policymakers / committee]
**Prepared by:** [org/name] | **Classification:** [TLP]

## (M) The Problem                            (150–200 words)
The policy problem, explained for a non-technical audience.
Why this matters now. What is at stake.

## (M) Background
Context. What has been tried. What has changed.

## (M) Assessment
Current situation. Trend direction. Who is affected and how.

## (M) Policy Options
Table: Option | Pros | Cons | Estimated Cost / Effort

## (M) Recommendations                        (numbered, prioritised)
1. [Immediate — highest priority]
2. ...

## (M) Expected Outcomes
What success looks like. How to measure it. Timeline.

## (R) Supporting Evidence
Key statistics and sources. No IOC tables — summarise threat at policy level.

## (M) Contact
Who prepared this. How to request further briefing.
```

---

## Writing Pipeline

### Phase 1 — Input Preparation

Organise inputs in a `writing-runs/{slug}/input/` directory:
- `notes.md` — raw analyst notes
- `iocs.json` — IOC data (MISP export or manual)
- `context.md` — background, case history, related reports

### Phase 2 — Fact Sheet

Before writing begins, produce a `fact-sheet.md` containing:
- Confirmed IOCs only (no inferred values)
- Confirmed attribution (with confidence level)
- Confirmed timeline
- Source list
- Flagged gaps: `[VERIFY: item]`

**The fact sheet is the sole source of truth for all section writers.** Section agents do not have access to external information, other sections' drafts, or each other.

### Phase 3 — Outline

Load the section template for the chosen format (above). Produce an outline with TLP marking in every section heading. Stop for analyst approval before writing.

### Phase 4 — Section Writing

Write one section at a time (SEQUENTIAL mode) or in parallel across formats (PARALLEL mode). Each section:
- Reads only the fact sheet
- Does not invent IOCs, attribution, or technical detail
- Flags `[SOURCE: descriptor]` for claims needing citation
- Flags `[VERIFY: item]` for anything requiring external confirmation

### Phase 5 — Diagrams

Produce Mermaid (`.mmd`) diagrams for: ATT&CK chain, infrastructure graph, timeline. Compile with `mmdc`:

```bash
mmdc -i diagrams/{name}.mmd -o diagrams/{name}.png
```

### Phase 6 — Coherence Review

Check:
- TLP marking present in every section
- No contradictions between sections
- Terms used consistently
- All `[SOURCE:]` and `[VERIFY:]` flags listed in `review-notes.md`
- Confidence levels explicit on all attribution and forecasts
- Format-specific requirements met

### Phase 7 — Compile

```bash
# Assemble
cat sections/*.md > assembled-draft.md

# Pandoc compilation
pandoc assembled-draft.md -o output/{slug}.pdf --pdf-engine=xelatex
pandoc assembled-draft.md -o output/{slug}.docx
pandoc assembled-draft.md -o output/{slug}.html --standalone
```

---

## TLP Handling

- TLP appears in: filename, every section header, document metadata
- No unmarked document ever leaves the pipeline
- Default TLP for active investigations: **TLP:AMBER**
- Blog posts: no TLP marking; do not include raw IOC tables or ATT&CK mapping

## Audience Calibration by Format

| Format | Technical depth | IOC tables | ATT&CK mapping | Confidence language |
|--------|----------------|------------|----------------|-------------------|
| `tech-blog` | High | No | No | Informal |
| `campaign-report` | High | Yes | Yes | Explicit ODNI |
| `advisory` | Medium | Yes | Referenced | Brief |
| `policy-brief` | Low | No | No | Plain language |
| `expert-witness` | Medium-High | Limited | Limited | Explicit (fact/inference/opinion) |

## Expert Witness Statements

Expert witness statements require:
- A declaration of truth
- Explicit separation of observed fact, inference, and opinion throughout
- Every technical claim supported by a source or direct test result
- No probability language without a stated basis for the estimate

## Linked Prompt

- [[30-prompts/infosec-report-orchestrator]] — Full prompt templates for single-format and multi-format generation
