---
title: "Influence Operations - Media & Court Coverage"
type: skill
tags: [influence-ops, narrative, media, court, DISARM, disinformation, framing]
llms: [claude-sonnet, gpt-4o, openrouter]
status: active
last_updated: 2026-06-12
source_playbook: /home/user/threat-research/playbooks/influence_ops_media.md
---

# Influence Operations - Media & Court Coverage

## Purpose

Investigate media activity around court cases and public events for framing bias, witness exposure risk, and potential coordination.

## Auto-Run Profile (Minimal Input)

This skill is runnable with only:

```yaml
case_name: "..."
primary_personas: ["...", "..."]
```

Defaults:
- Applicable jurisdiction and language scope
- 7-year lookback
- infer additional POIs from sources
- preserve cookies for render crawling
- include Wayback lookup for unavailable pages

## 8-Phase Process

| Phase | Goal |
|-------|------|
| 1 | Case reconstruction - legal status, hearings, key dates |
| 2 | Person expansion - infer/add witnesses, lawyers, journalists, editors |
| 3 | Media catalog - collect all case-related articles with metadata |
| 4 | Verification - static + render + cookie runs + archive fallback |
| 5 | Framing and violations - score narratives and legal-risk indicators |
| 6 | Coordination analysis - timing/phrase/error overlap evidence |
| 7 | Network and timeline - relationship map + event chronology |
| 8 | Output export - HTML, JSON artifacts, MISP, session log |

## POI Inference Rules

Add actor to POI set when any condition is true:
- Named in article body/title with case relation
- Named witness/counsel/court expert in at least one source
- Journalist byline appears on >=2 relevant articles
- Repeatedly appears in coordination evidence clusters

## Coordination Evidence Levels

| Evidence | Level |
|----------|-------|
| Identical verbatim phrases across outlets | CONFIRMED |
| Same factual error across outlets | CONFIRMED |
| Same framing angle, same day, different outlets | HIGH |
| Repeated framing over weeks | MEDIUM |
| Timing alignment without content overlap | LOW |

## Graph Regeneration Guardrails

- Preserve inferred/unconfirmed relationships; do not remove them unless explicitly disproven.
- Keep explicit confidence level per relationship and retain evidence/provenance field.
- Run mandatory integrity checks after every graph rebuild:
  - unique entity IDs
  - zero dangling edges
  - no accidental isolated nodes from dropped links
  - inferred edge count equals pre-rebuild total (discrepancy = silently dropped edges)
- Run HTML render smoke test for the final report.
- For conflict-of-interest investigations, enforce chain-presence checks for key hypotheses before final export.

## Mandatory Deliverables

- `media_analysis/article_catalog.json`
- `media_analysis/article_summaries.json`
- `media_analysis/publication_timing.json`
- `media_analysis/coordination_evidence.json`
- `timeline/master_timeline.json`
- `network/relationship_map.json`
- `reports/html_export/index.html`
- `reports/{case}_misp.json`
- `reports/{case}_report.md`

## HTML Minimum Features

- interactive social graph (all POIs present)
- timeline view
- coordination evidence section
- violations summary cards/table
- article verification/framing table
- graph legend/coloring by entity class

## Crawl + Browser Emulation Notes

- Static fetch is usually sufficient, but some outlets enforce consent walls or require JS rendering.
- Use Playwright to collect a storage-state cookie jar (consent accepted), then pass it to the crawler.
- Prefer sitemap-batch crawling for full-coverage studies (resumable with a progress pointer).
- Preserve full graph outputs for offline analysis (JSONL edge lists, Gephi exports); cap the HTML report graph for browser stability.

### Full Graph Preservation (Large Social Graphs)

- Write the *full* node list and *full* edge list(s) to machine-friendly formats (JSON/JSONL).
- Generate a separate, capped subset graph only for the HTML report UI to prevent browser crashes.
- Prefer JSONL for very large edge sets (streaming-friendly, easy to post-process).
- Always emit a manifest (counts + file paths) so downstream tooling can validate completeness.
- Add Gephi exports (CSV + GEXF) to enable interactive clustering/community analysis outside the HTML report.

---

## Linked Workflow

- `[[40-workflows/narrative-influence-investigation]]`

## Behavioral Analysis Methods

- [[50-knowledge/behavioral-analysis/01-computational-digital]] — CIB detection, bot taxonomy, network analysis
- [[50-knowledge/behavioral-analysis/02-psycholinguistic]] — framing analysis, NLP, narrative detection
- [[50-knowledge/behavioral-analysis/05-behavioral-economics]] — cognitive bias exploitation, dual-process theory, inoculation
- [[50-knowledge/behavioral-analysis/07-social-group-behavioral]] — SIT, radicalization pathways, coordinated behavior dynamics
- [[50-knowledge/behavioral-analysis/06-psychographic-profiling]] — personality-based targeting, OCEAN model, microtargeting
