---
title: "Session YYYY-MM-DD — {topic}"
type: session
date: YYYY-MM-DD
status: in-progress
tags: [session, {topic-tags}]
session_id: N
operator: analyst
run_dir: /path/to/run/dir/
# Optional fields — include when relevant, delete when not:
# case_id: INV-XXX
# workflow_id: workflow-slug
# models_used: [claude-sonnet]
# hosts_used: [analysis-server]
# misp_events: []
# artifacts_in: []
# artifacts_out: []
---

# Session — YYYY-MM-DD — {topic}

## Objective

{one sentence}

## Completed

- [x] ...

## Key Findings

- ...

## Flagged Observations

<!-- Optional. Populate when something unexpected was directly observed.
     Leave absent if nothing arose this session.
     These are CANDIDATE flags for analyst review — not authoritative lessons.
     The analyst decides in Phase 3 of vault curation what is genuine and
     what (if anything) becomes permanent methodology.
     Do NOT assert root causes or fixes that were not verified in this session.

     Format: ### [TYPE | destination-skill-slug | HIGH|MED|LOW]
     Types: TOOL-EDGE-CASE, NEW-TTP, METHOD-REFINEMENT, TOOL-SUCCESS,
            KNOWLEDGE-UPDATE, ANALYTICAL-INSIGHT, FALSE-POSITIVE, OPSEC-LESSON

     Example:
     ### [TOOL-EDGE-CASE | malware-analysis | HIGH]
     **Tool:** floss
     **Condition:** UPX-packed ELF with obfuscated string table
     **Symptom:** Silent exit 0, no output
     **Observed resolution:** `--minimum-length 4` — confirmed working in this session
     **Confidence:** Directly observed | Inferred — not confirmed in session
     **Destination:** 10-skills/malware-analysis.md → floss section
-->

## Artifacts

- ...

## Next Steps

- [ ] ...
