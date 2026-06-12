---
title: "Infosec Report & Blog — Writing Orchestrator"
type: prompt
tags: [writing, threat-report, blog, advisory, malware-analysis, policy-brief, orchestrator, pandoc, multi-format]
llms: [claude-sonnet, claude-opus]
skill: "[[85-writing/infosec-report-writing]]"
status: active
last_updated: 2026-04-08
---

# Infosec Report & Blog — Writing Orchestrator

## Use Case

Trigger the infosec writing pipeline for one or more document formats from a single set of analyst inputs. Supports single-format and multi-format generation. Two mode axes: `FACT_SHEET_MODE` (GATED / AUTO) and `SECTION_MODE` (SEQUENTIAL / PARALLEL).

## Variables

| Variable | Description | Values |
|----------|-------------|--------|
| `{INPUT_NOTES}` | Path to raw analyst notes | `input/notes.md` |
| `{IOC_DATA}` | Path to IOC file or MISP export | `iocs/misp_event.json` or `none` |
| `{FORMATS}` | One or more format codes (see skill file) | `campaign-report` / `[campaign-report, advisory, tech-blog]` |
| `{TLP}` | Traffic Light Protocol level | `TLP:CLEAR` / `TLP:AMBER` / `TLP:RED` |
| `{OUTPUT_SLUG}` | Short label for output directory | `apt-x-campaign-apr26` |
| `{FACT_SHEET_MODE}` | Gate or skip fact-sheet approval | `GATED` (default) / `AUTO` |
| `{SECTION_MODE}` | Section writing order | `SEQUENTIAL` (default) / `PARALLEL` |

**Valid format codes:**
`flash` · `intel-bulletin` · `advisory` · `sitrep` · `campaign-report` · `actor-profile` · `annual-report`
`malware-report` · `re-writeup` · `cve-advisory` · `exploit-analysis` · `rule-doc`
`tech-blog` · `strategic-blog` · `whitepaper` · `case-study` · `exec-summary`
`policy-brief` · `consultation` · `expert-witness`

---

## Prompt — Single Format (Gated, Sequential)

```
Read 85-writing/infosec-report-writing.md in full before starting.

INPUTS:
  Notes:    {INPUT_NOTES}
  IOC data: {IOC_DATA}
  Format:   {FORMAT}
  TLP:      {TLP}
  Output:   writing-runs/{OUTPUT_SLUG}/

FACT_SHEET_MODE: GATED
SECTION_MODE:    SEQUENTIAL

Phase 1 — Intake & Validation
  Confirm input files exist and are non-empty.
  Confirm {FORMAT} is a valid code in the skill file.
  Set TLP. If IOC data or a primary source is missing: STOP. List gaps.

Phase 2 — Research Synthesis
  Read all inputs. Produce writing-runs/{OUTPUT_SLUG}/fact-sheet.md containing:
    - Confirmed IOCs (no inferred values)
    - Confirmed attribution if any (with confidence level)
    - Confirmed timeline
    - Source list (sources.md)
    - Flagged gaps and [VERIFY: ...] items
  STOP. Present fact-sheet.md and wait for analyst approval.

Phase 3 — Outline
  Load the section template for {FORMAT} from the skill file.
  Produce writing-runs/{OUTPUT_SLUG}/{FORMAT}/outline.md.
  Include TLP marking in every section heading.
  STOP. Present outline and wait for approval.

Phase 4 — Section Writing (SEQUENTIAL)
  Write one section at a time in outline order.
  Each section reads fact-sheet.md as its sole source of truth.
  Do not invent IOCs, attribution, or technical detail not in the fact sheet.
  Flag [SOURCE: descriptor] for claims needing citation not yet in fact sheet.
  Flag [VERIFY: item] for anything requiring external confirmation.

Phase 5 — Diagram Generation
  Identify 1–3 diagrams that add value (ATT&CK chain, infra graph, timeline).
  Write .mmd Mermaid source to writing-runs/{OUTPUT_SLUG}/diagrams/.
  Run: mmdc -i diagrams/{name}.mmd -o diagrams/{name}.png
  Reference PNGs in the assembled draft.

Phase 6 — Coherence Review
  Read the assembled draft. Check:
    (a) TLP marking present in every section
    (b) No contradictions between sections
    (c) Terms used consistently throughout
    (d) All [SOURCE: ...] and [VERIFY: ...] flags listed in review-notes.md
    (e) Confidence levels explicit on all attribution and forecasts
    (f) Format-specific requirements met (see skill file section template)

Phase 7 — Compile
  Assemble: writing-runs/{OUTPUT_SLUG}/{FORMAT}/assembled-draft.md
  Run pandoc:
    {OUTPUT_SLUG}_{FORMAT}_{date}.pdf   (--pdf-engine=xelatex)
    {OUTPUT_SLUG}_{FORMAT}_{date}.docx
    {OUTPUT_SLUG}_{FORMAT}_{date}.html  (--standalone)
  Fix any compilation errors before finishing.

Deliver: list of output file paths, flagged gaps, unresolved [VERIFY:] items.
```

---

## Prompt — Multi-Format (Gated, Parallel Formats)

```
Read 85-writing/infosec-report-writing.md in full before starting.

INPUTS:
  Notes:    {INPUT_NOTES}
  IOC data: {IOC_DATA}
  Formats:  {FORMATS}           # e.g. [campaign-report, advisory, tech-blog]
  TLP:      {TLP}
  Output:   writing-runs/{OUTPUT_SLUG}/

FACT_SHEET_MODE: GATED
SECTION_MODE:    SEQUENTIAL

Phase 1 — Intake & Validation
  Confirm all input files exist. Confirm all format codes are valid.
  List the formats to be produced and confirm with the analyst before proceeding.

Phase 2 — Research Synthesis (shared across all formats)
  Produce one shared writing-runs/{OUTPUT_SLUG}/fact-sheet.md.
  This is the single source of truth for every format.
  STOP. Present fact-sheet.md and wait for approval before any drafting begins.

Phase 3 — Outlines (one per format, sequential)
  For each format in {FORMATS}:
    Load the section template from the skill file.
    Produce writing-runs/{OUTPUT_SLUG}/{format}/outline.md.
    Each outline must adapt depth and language to its audience
    (e.g., tech-blog omits IOC tables and ATT&CK mapping;
     advisory omits technical deep-dives;
     policy-brief omits IOCs entirely).
  Present all outlines. Wait for approval before drafting.

Phase 4 — Section Writing (parallel across formats, sequential within)
  Run one drafting pipeline per format simultaneously.
  Each format reads only fact-sheet.md — not the other formats' drafts.
  Flag [SOURCE: ...] and [VERIFY: ...] as in single-format mode.

Phase 5 — Diagrams (shared pool)
  Produce diagrams once. Reuse across formats where appropriate.
  Format-specific diagrams go into writing-runs/{OUTPUT_SLUG}/diagrams/{format}/.

Phase 6 — Coherence Review (per format + cross-format)
  Per-format: same checks as single-format mode.
  Cross-format check: ensure formats do not contradict each other on facts,
  attribution, or confidence levels.
  Write review-notes.md covering all formats.

Phase 7 — Compile (all formats)
  For each format:
    Assemble writing-runs/{OUTPUT_SLUG}/{format}/assembled-draft.md
    Produce PDF, DOCX, HTML with filename pattern:
      {OUTPUT_SLUG}_{format}_{date}.{ext}

Deliver: table of all output files produced, consolidated gap list, all [VERIFY:] items.
```

---

## Prompt — Auto Mode (No Gates)

```
Read 85-writing/infosec-report-writing.md in full before starting.

INPUTS:
  Notes:    {INPUT_NOTES}
  IOC data: {IOC_DATA}
  Formats:  {FORMATS}
  TLP:      {TLP}
  Output:   writing-runs/{OUTPUT_SLUG}/

FACT_SHEET_MODE: AUTO
SECTION_MODE:    {SECTION_MODE}

Run all 7 phases without stopping for approval.
Log all flagged gaps, [SOURCE: ...], and [VERIFY: ...] items to review-notes.md.
Deliver the full output package on completion.
```

---

## Common Multi-Format Combinations

```
# Campaign investigation
Formats: [campaign-report, advisory, tech-blog]

# Major vulnerability
Formats: [cve-advisory, tech-blog, strategic-blog]

# Incident response close-out
Formats: [sitrep, malware-report, case-study]

# New malware family discovery
Formats: [malware-report, re-writeup, rule-doc, advisory]

# Annual research publication
Formats: [annual-report, strategic-blog, policy-brief]

# ICS / critical infrastructure incident
Formats: [flash, campaign-report, policy-brief]
```

---

## Expected Output Structure

```
writing-runs/{OUTPUT_SLUG}/
├── input/                         # source material (copied)
│   ├── notes.md
│   ├── iocs.json
│   └── context.md
├── fact-sheet.md                  # shared source of truth
├── sources.md                     # all cited sources
├── {format-1}/
│   ├── outline.md
│   ├── sections/
│   │   ├── 01-*.md
│   │   └── ...
│   ├── assembled-draft.md
│   └── output/
│       ├── {slug}_{format-1}_{date}.pdf
│       ├── {slug}_{format-1}_{date}.docx
│       └── {slug}_{format-1}_{date}.html
├── {format-2}/                    # if multi-format
│   └── ...
├── diagrams/
│   ├── shared/
│   ├── {format-1}/
│   └── {format-2}/
└── review-notes.md                # all flags, gaps, coherence issues
```

---

## Notes

- **Fact sheet is law.** Section agents have no access to each other's output and no access to external knowledge beyond the fact sheet. Gaps go to review-notes, not into the draft.
- **TLP is mandatory.** Appears in filename, every section header, and document metadata. No unmarked document ever leaves the pipeline.
- **Confidence levels are mandatory** on all attribution and forecasts. `HIGH / MODERATE / LOW` with explicit basis.
- **Multi-format audience calibration.** The same fact produces different language for different audiences. The outline agent is responsible for calibrating depth and vocabulary to each format's audience — not the section writers.
- **Blog posts** omit TLP, IOC tables, and ATT&CK mapping. Include hook paragraph and concrete defender takeaway.
- **Policy briefs** omit technical IOC data entirely. Lead with the policy problem, end with numbered recommendations.
- **Expert witness statements** require declaration of truth and explicit separation of observed fact, inference, and opinion throughout.
