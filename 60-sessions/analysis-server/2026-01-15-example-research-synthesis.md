---
title: "Session 2026-01-15 — Research synthesis (MFA hardware keys vs TOTP)"
type: session
id: session-2026-01-15-example-research-synthesis
volatility: stable
sensitivity: public
date: 2026-01-15
status: complete
tags: [session, example, research, synthesis, methodology]
session_id: 1
operator: analyst
run_dir: /home/user/research/mfa-comparison/
models_used: [claude-sonnet]
hosts_used: [analysis-server]
artifacts_in:
  - /home/user/research/mfa-comparison/input/question.md
artifacts_out:
  - /home/user/research/mfa-comparison/reports/briefing.md
---

# Session — 2026-01-15 — Research Synthesis (Example)

> **Teaching example.** A sanitised, domain-neutral session showing what a worked
> run of the [[40-workflows/example-research-synthesis]] workflow looks like — and how
> a session log feeds the curation loop. Contains no real or sensitive content.

## Objective

Answer a generic research question — *"What does the public evidence say about the
security benefits of hardware security keys versus TOTP apps for MFA?"* — by running the
example research-synthesis workflow end to end, producing a sourced briefing.

## Completed

- [x] Read [[40-workflows/example-research-synthesis]] before starting
- [x] Phase 1 — Collect: applied [[10-skills/example-source-collection]]; logged 6 public sources (standards, vendor docs, independent reporting)
- [x] Phase 1 gate: each sub-question (phishing resistance, usability, cost, recovery) had ≥1 source
- [x] Phase 2 — Evaluate: applied [[10-skills/example-source-evaluation]]; rated source reliability (A–F) and claim credibility (1–6) with a rationale per rating
- [x] Phase 2 gate: every key claim rated; one single-sourced claim flagged
- [x] Phase 3 — Synthesize: wrote the briefing, every assertion carrying source `id`(s) and an overall confidence
- [x] Phase 3 gate: no unsourced assertion
- [x] Wrote session notes

## Key Findings

- **Phishing resistance** is the clearest differentiator: hardware security keys (FIDO2/WebAuthn) resist credential-phishing by binding the assertion to the origin; TOTP codes can be relayed to a phishing site. Supported by S1 (standard) and S3 (independent reporting) — reliability A, credibility 1.
- **Usability/recovery** is the main trade-off: hardware keys require a spare/backup key or a recovery path; loss-of-device handling is the most common adoption friction (S4, S5).
- **Cost** is a per-user hardware expense for keys vs essentially zero for TOTP apps (S2).
- One claim — a specific phishing-success-rate percentage — rested on a **single source** (S6) and is flagged as weak; the briefing states it with low confidence.
- **Overall:** for phishing-resistant MFA the public evidence favours hardware keys; the decision turns on recovery process and cost, not on disputed security facts. Confidence: **high** on the security comparison, **low** on the single-sourced statistic.

## Flagged Observations

### [METHOD-REFINEMENT | example-source-evaluation | MED]
**Method:** Claim-credibility rating
**Condition:** A vendor source (the key manufacturer) made favourable security claims about its own product
**Symptom:** Rating the claim purely on the source's reliability would have over-credited a self-interested source
**Observed resolution:** Rated source reliability and claim credibility *separately* (per the skill) and required an independent corroborating source before assigning credibility 1; the vendor-only claims were held at 3
**Confidence:** Directly observed in this session
**Destination:** `10-skills/example-source-evaluation.md` → rationale/independence note

## Artifacts

- Briefing (the workflow's final deliverable): `/home/user/research/mfa-comparison/reports/briefing.md`
- Source + claims tables: embedded in the briefing's Evidence section

## Next Steps

- [ ] Obtain a second independent source for the flagged single-sourced statistic, or drop it
- [ ] Reuse this question as a regression check when editing the example skills
