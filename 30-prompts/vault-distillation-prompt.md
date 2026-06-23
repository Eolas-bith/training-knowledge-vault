---
title: "Vault Distillation — Aggregation Prompt"
type: prompt
id: prompt-vault-distillation-prompt
volatility: periodic
sensitivity: public
tags: [vault, curation, distillation, lessons-learned, maintenance]
llms: [claude-sonnet]
status: active
last_updated: 2026-05-18
---

# Vault Distillation — Aggregation Prompt

**What this prompt does:** Reads recent session files, extracts lessons, and appends them to `00-index/lessons-log.md`. It does **not** read, propose changes to, or modify any skill file. Skill files are only updated in a separate, explicit Phase 4 session initiated by the analyst.

**Prerequisite:** Read `10-skills/vault-curation.md` before running this for the first time.

---

## Prompt

```
You are running a vault distillation session — Phase 2 (Aggregate) only.

Your task is to read recent session files, extract lessons learned, and append
them to 00-index/lessons-log.md.

YOU MUST NOT read, open, propose changes to, or modify any file in 10-skills/,
50-knowledge/, 85-writing/, or any other methodology directory.
The lessons log is the only file you write to during this run.

--- STEP 0: Read the curation log ---

Read 00-index/vault-curation-log.md.
Note the last run date and last session file processed.
Read 00-index/lessons-log.md to see the current ID counter and existing entries.
Report: "Last run: [date]. Last ID assigned: L-[N]. Scanning sessions from [date] onward."

--- STEP 1: Identify candidate sessions ---

List all session files in 60-sessions/ that postdate the last run.
For each, note whether it has:
  - A structured ## Lessons Learned section (extract directly)
  - Substantial ## Key Findings that may contain implicit lessons (requires inference)
  - Neither (skip)

Present the candidate list and wait for confirmation to proceed.

--- STEP 2: Extract lessons ---

For each candidate session:

  1. Structured lessons (## Lessons Learned entries):
     Extract each tagged entry verbatim. Each entry becomes one log item.

  2. Implicit lessons (## Key Findings inference):
     Look for phrases: "failed when", "workaround", "first observed", "false positive",
     "edge case", "effective combination", "unexpectedly", "better results when".
     Mark each inferred lesson [INFERRED] — the analyst decides whether to keep it.

  3. Ambiguous observations:
     If a finding is potentially a lesson but you are not confident it generalises,
     mark it [AMBIGUOUS — analyst review] and include it for the analyst to decide.

  Do not invent lessons. If a session has no distillable content, say so and move on.

--- STEP 3: Present extracted lessons before writing ---

Before writing anything to the lessons log, present all extracted lessons grouped
by proposed destination:

  Proposed for: 10-skills/malware-analysis.md
    [L-XXX] [TOOL-EDGE-CASE] [HIGH] floss silent exit on UPX-packed ELF
    [L-XXX] [TOOL-SUCCESS] [MED] capa + floss pipeline order
    ...

  Proposed for: 50-knowledge/malware-families/[family].md
    [L-XXX] [NEW-TTP] [MED] SetWindowsHookEx injection variant
    ...

  Proposed for: OTHER / NEW-SKILL-NEEDED
    [L-XXX] [NEW-SKILL-NEEDED] [HIGH] no existing skill covers X
    ...

Ask the analyst: "Do you want to proceed with writing these to the lessons log,
or exclude any entries?"

--- STEP 4: Append to the lessons log ---

After confirmation, append each lesson to 00-index/lessons-log.md:

  1. Assign the next sequential ID (increment from last assigned ID in the log)
  2. Add a row to the summary table under the correct destination section
  3. Add a full entry below the table using this format:

  ### L-[ID] — [TYPE] [short title] — [YYYY-MM-DD]
  **Source:** 60-sessions/[session-file].md → [section]
  **Condition:** [when does this lesson apply?]
  **Observation:** [what was observed or learned?]
  **Recommended change:** [what would be added/changed in the destination file when applied?]
  **Priority:** [HIGH / MED / LOW]
  **Status:** open
  **Applied in commit:** —

  4. Update the ID Counter at the bottom of the log to the last assigned ID.

  If a new destination section is needed (file not yet in the log), create it
  following the existing section format.

  Do not modify any existing log entries.

--- STEP 5: Commit ---

After all entries are written to the lessons log, create one git commit:

  chore(vault): distillation run N — M lessons added to log

  Sessions processed: [session file names]
  Lessons added: [count] ([type breakdown])
  New IDs: L-[first] through L-[last]

Report the short commit hash to the analyst.

--- STEP 6: Update the curation log ---

Update 00-index/vault-curation-log.md:
  - Set last run date
  - Set last session processed
  - Record the commit hash for this run
  - Add a Run N entry following the template in that file

--- HARD CONSTRAINTS ---

- Do NOT open any file in 10-skills/, 50-knowledge/, 85-writing/, or similar
- Do NOT propose edits to skill files
- Do NOT use the Edit tool on anything other than the lessons log and curation log
- Fabrication rule: extract only what is documented in session files; never invent
  tool behaviors, TTPs, IOCs, or observations
- If uncertain whether a finding generalises: mark [AMBIGUOUS], include it, let
  the analyst decide — do not silently drop it

Begin with Step 0.
```

---

## Phase 4 — Applying Lessons to Skill Files

This is a **separate session**, initiated by the analyst with a specific instruction. It is not part of this prompt.

When the analyst is ready to apply lessons, they say something like:
- "Apply L-003 and L-007 to malware-analysis.md"
- "I want to update threat-research-ioc.md — apply all open HIGH lessons for it"
- "Show me what L-012 would look like as an edit to structured-analytical-techniques.md"

Claude then reads the nominated lesson(s) from the log, reads the target section of the skill file, and proposes a surgical edit for analyst approval before applying. One commit per skill file updated, with the lesson IDs referenced in the commit message.

See `10-skills/vault-curation.md → Phase 4` for the full procedure.
