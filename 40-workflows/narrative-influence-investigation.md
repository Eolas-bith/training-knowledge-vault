---
title: "Narrative / Influence Operations Investigation"
type: workflow
tags: [influence-ops, narrative, osint, compound-investigation]
llms: [claude-sonnet, gpt-4o, openrouter]
status: active
last_updated: 2026-04-18
---

# Narrative / Influence Operations Investigation

## Purpose

End-to-end workflow for court/media influence investigations with repeatable outputs and evidence grading. Used when investigating coordinated narrative shaping across media, social platforms, or legal proceedings.

## Minimal Kickoff Input (Auto Mode)

Only these fields are required:

```yaml
case_name: "Smith vs Nexova"
primary_personas:
  - "John Smith"
  - "Nina Nexova"
```

Everything else is defaulted and inferred unless explicitly overridden.

## Default Assumptions

- Jurisdiction/language: configure per case
- Timeframe: last 7 years from run date
- Search scope: target-language domains first, then international
- Crawl strategy: static first, render second, consent-cookie render third
- Recovery strategy: Wayback CDX for deleted/404 pages
- Privacy: no pseudonyms unless requested
- Session logging: mandatory in `60-sessions/{host}/...`

## Browser Emulation (Playwright)

Some outlets require consent flows, JS rendering, or session cookies. Use Playwright when static fetch fails.

Guidelines:
- Static-first: try normal HTTP fetch for cost/scale.
- Render-second: enable browser rendering for pages that require JS to populate content.
- Cookies-third: collect storage-state cookies (consent accepted) and re-run render/static crawl with cookies to pass consent walls.
- Archive fallback: if blocked/deleted, pull from Wayback CDX for verification and completeness.

## Automatic Inference Rules

When only case/personas are provided, infer and include:

- Aliases, spelling variants, role labels (defendant, witness, counsel, journalist)
- Secondary persons from co-mentions in >=2 sources or direct witness/court references
- Journalist bylines as persons of interest when they repeatedly cover the case
- Institutional actors (outlets, ownership clusters, court entities)

## Recommended Execution Order

1. Phase 1 (case reconstruction): legal timeline, key hearings, status
2. Phase 2 (person expansion): build POI list from seed names + inferred actors
3. Phase 3 (media catalog): discover and normalize article set across outlets
4. Phase 4 (verification): render + cookies + archive recovery for blocked pages
5. Phase 5 (framing/violations): score framing and legal/ethical violation indicators
6. Phase 6 (coordination): timing clusters + phrase overlap + factual error reuse
7. Phase 7 (graph/timeline): regenerate relationship map and master timeline
8. Phase 8 (reporting): HTML report + MISP JSON + markdown summaries
9. Phase 9 (session close): write detailed session log and update workflow notes

## Coverage and Quality Gates (Must Pass)

- Source gate: do not rely on a single outlet cluster; include diverse coverage
- Verification gate: each article has `verification_level` and retrieval method
- Coordination gate: `coordination_evidence.json` and report section included
- Graph gate: all direct and inferred POIs present in `relationship_map.json`
- Report gate: interactive HTML has timeline, social graph, violation summary, coordination evidence, article table

## Large-Graph Preservation (Full vs Report Subset)

When the relationship graph is large (10k+ nodes or 100k+ edges), the HTML report must remain a *subset* for stability, but the underlying data must be preserved in full for offline analysis.

Rules:
- Always write full nodes + full edges to disk (do not downsample the source artifacts).
- Prefer edges as JSONL for streaming post-processing and to avoid memory blowups.
- Generate a render-friendly subset graph for `reports/html_export/index.html` only.
- Emit a manifest with counts + file paths (nodes, typed edges, co-mention edges) as a completeness contract.
- Export to Gephi (GEXF/CSV) for modularity/community analysis and layout at scale.

Reference output structure:
- Full nodes: `{case}/network/entities_full.json`
- Full edges: `{case}/network/edges_typed_full.jsonl`, `{case}/network/edges_comention_full.jsonl`
- Manifest: `{case}/network/full_graph_manifest.json`
- Gephi: `{case}/network/gephi/{case}_full.gexf`

## Graph Preservation Rules (Critical)

- Inference-preservation gate: inferred/unconfirmed edges must survive every graph regeneration pass.
- Confidence handling rule: downgrade/upgrade edge confidence (`confirmed` / `inferred` / `unconfirmed`) instead of deleting hypothesis edges.
- Provenance rule: every inferred edge must keep an `evidence` provenance note (source or explicit inference basis).
- Integrity rule: enforce unique node IDs, zero dangling edges, and no silent node drops.
- Regression check: if a case has a flagged conflict chain, verify it still exists after rebuild.

## Mandatory Output Structure

```
{run_dir}/
├── scope.json
├── timeline/master_timeline.json
├── network/relationship_map.json
├── media_analysis/article_catalog.json
├── media_analysis/article_summaries.json
├── media_analysis/publication_timing.json
├── media_analysis/coordination_evidence.json
├── reports/coordination_evidence.md
├── reports/html_export/index.html
├── reports/{case}_report.md
└── reports/{case}_misp.json
```

## Session Logging Contract

Every run must record:

- Inputs and inferred assumptions
- Exact outlet coverage and unresolved gaps
- Infrastructure deviations (DNS/proxy/cookie handling) and restoration steps
- Artifact paths and status of each quality gate
- Re-run recipe for next analyst/LLM

## DNS Troubleshooting

If crawling fails due to DNS resolution:

1. Backup `/etc/resolv.conf`
2. Temporarily switch to public DNS (1.1.1.1 / 8.8.8.8)
3. Run crawl / Playwright tasks
4. Restore original resolver config
5. Log the change in session notes

## Classification

Default: **TLP:AMBER** for active proceedings.
