---
title: "Session 2026-01-22 — Influence operation investigation (media coordination)"
type: session
date: 2026-01-22
status: complete
tags: [session, influence-ops, osint, media-analysis, coordination, narrative]
session_id: 2
operator: analyst
run_dir: /home/user/influence-ops/nexova-case/
models_used: [claude-sonnet]
hosts_used: [analysis-server]
artifacts_in:
  - /home/user/influence-ops/nexova-case/input/article_urls.txt
  - /home/user/influence-ops/nexova-case/input/case_notes.md
artifacts_out:
  - /home/user/influence-ops/nexova-case/reports/nexova-case_report.md
  - /home/user/influence-ops/nexova-case/reports/coordination_evidence.md
  - /home/user/influence-ops/nexova-case/reports/html_export/index.html
---

# Session — 2026-01-22 — Influence Operation Investigation (Media Coordination)

## Objective

Investigate suspected coordinated media coverage of the Nexova corporate restructuring dispute and determine whether article timing, content overlap, and byline patterns indicate an organised influence operation.

## Completed

- [x] Read `10-skills/influence-ops-media.md` before starting
- [x] Read `40-workflows/narrative-influence-investigation.md` for workflow
- [x] Phase 1: reconstructed case timeline from court registry and press releases
- [x] Phase 2: expanded POI list — identified 4 journalists, 2 PR agency contacts, 3 corporate officers
- [x] Phase 3: catalogued 23 articles across 5 outlets spanning 2025-09 to 2026-01
- [x] Phase 4: verified retrieval — 2 articles recovered via Wayback CDX (404 on live sites)
- [x] Phase 5: framing analysis — 18 of 23 articles used corporate-favorable framing
- [x] Phase 6: coordination analysis — phrase reuse, timing clusters, factual error reuse
- [x] Phase 7: generated relationship graph and master timeline
- [x] Phase 8: produced HTML report, coordination evidence document, and markdown summary
- [x] Phase 9: wrote session notes

## Key Findings

- **Coordination confirmed** at MODERATE confidence
- Phrase reuse rate: 34% of identified key phrases appeared verbatim across 3+ outlets
- Timing cluster: 6 of 9 favorable articles published within 2-hour windows — unlikely to be coincidental (assessed probability <0.5% under null hypothesis of independent publishing)
- Shared byline pattern: 3 journalists credited across 2 outlets share an employer (a PR agency with a disclosed relationship to Nexova's parent company)
- Factual error reuse: same incorrect claim about the dispute timeline appeared in 4 articles with identical wording — suggests a common briefing document or press release source
- 2 negative-framing articles (from independent outlets) showed no coordination indicators
- Attribution: organized influence operation involving PR agency coordination assessed MODERATE confidence; direct corporate direction assessed LOW confidence (no documentary evidence of direct instruction)

## Flagged Observations

### [METHOD-REFINEMENT | influence-ops-media | MED]
**Method:** Phrase overlap detection
**Condition:** Articles from the same PR wire service share boilerplate phrases that are not coordination indicators
**Symptom:** Initial phrase overlap score inflated by wire service attribution language that appeared in all articles
**Observed resolution:** Filtering out standard attribution phrases ("according to company representatives", "in a statement released by") before running overlap analysis reduced false positive rate significantly
**Confidence:** Directly observed — filtering approach tested manually on two article pairs
**Destination:** 10-skills/influence-ops-media.md → coordination detection section

### [ANALYTICAL-INSIGHT | structured-analytical-techniques | LOW]
**Context:** Attribution of coordination to corporate direction vs. PR agency autonomous decision
**Observation:** The ACH matrix showed that most available evidence was consistent with *either* hypothesis — corporate direction or PR agency acting on general mandate without explicit per-article instruction. The distinction matters legally but the evidence does not currently discriminate between the two.
**Confidence:** Inferred analytical observation — not a confirmed tool behavior
**Destination:** 10-skills/structured-analytical-techniques.md → ACH section (note on evidence discrimination)

## Artifacts

- Coordination evidence: `/home/user/influence-ops/nexova-case/reports/coordination_evidence.md`
- Full report (TLP:AMBER): `/home/user/influence-ops/nexova-case/reports/nexova-case_report.md`
- Interactive HTML report: `/home/user/influence-ops/nexova-case/reports/html_export/index.html`
- Article catalog: `/home/user/influence-ops/nexova-case/media_analysis/article_catalog.json`
- Relationship map: `/home/user/influence-ops/nexova-case/network/relationship_map.json`

## Next Steps

- [ ] Obtain documentary evidence of PR agency–corporate communication to upgrade attribution confidence
- [ ] Monitor for new articles — is the campaign ongoing or concluded?
- [ ] Check whether the PR agency has been linked to similar operations in other cases (cross-case pivot)
- [ ] Consider TLP:AMBER → TLP:GREEN downgrade for the methodology section only (case details remain AMBER)
