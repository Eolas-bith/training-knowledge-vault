---
title: "Vault Curation — Lessons Capture and Distillation"
type: skill
id: skill-vault-curation
volatility: periodic
sensitivity: public
tags: [vault, curation, distillation, lessons-learned, knowledge-management, maintenance]
llms: [claude-sonnet]
status: active
last_updated: 2026-05-18
---

# Vault Curation — Lessons Capture and Distillation

## Purpose

A four-phase process for accumulating operational knowledge from session work without touching methodology files until the analyst explicitly decides to update them.

**The core separation:**

| Phase | Who | What happens | Skill files touched? |
|-------|-----|-------------|----------------------|
| **Capture** | Claude (during session) | Tags lessons in session file | No |
| **Aggregate** | Claude (distillation run) | Reads sessions → writes to lessons log | No |
| **Review** | Analyst | Reads lessons log, decides what to do with each entry | No |
| **Apply** | Analyst + Claude (explicit session) | Analyst nominates specific lessons; Claude proposes edits | Yes — only then |

Skill files are never touched in Phases 1–3. Phase 4 only happens when the analyst initiates it with a specific instruction.

**Aggregate when:**
- 5 or more sessions have accumulated since the last run
- After a burst of malware analysis or investigation work
- Quarterly, as routine vault maintenance

**Curation state:** `00-index/vault-curation-log.md` — last run, sessions processed.  
**Lessons inbox:** `00-index/lessons-log.md` — all open and applied lessons.  
**Aggregate prompt:** `30-prompts/vault-distillation-prompt`

---

## Phase 1 — Capture (during sessions)

**The hallucination risk in Phase 1:** An LLM cannot reliably determine root cause. If a script fails because of a network timeout, the LLM may write an observation stating the API syntax changed — and a future session reads that entry and breaks the pipeline. The LLM's role in Phase 1 is **observation only**: record what happened and what was directly confirmed. Root cause analysis and fix validation belong to the analyst in Phase 3.

### Lesson Type Taxonomy

| Type tag | What it captures | Likely destination when applied |
|----------|-----------------|--------------------------------|
| `TOOL-EDGE-CASE` | Unexpected tool behavior + workaround | Skill file covering that tool |
| `NEW-TTP` | Technique not currently in any skill file | Relevant skill or `50-knowledge/` profile |
| `METHOD-REFINEMENT` | An approach that worked better or worse than documented | Methodology skill file |
| `TOOL-SUCCESS` | Effective pipeline, flag set, or sequence | Skill file — positive exemplar |
| `KNOWLEDGE-UPDATE` | New factual data about an actor, malware family, or capability | `50-knowledge/` actor or family file |
| `ANALYTICAL-INSIGHT` | Cross-case pattern or structural observation | New knowledge entry or analytical skill |
| `FALSE-POSITIVE` | Detection/IOC pattern that over-fires in a specific context | Skill file — adds explicit caveat |
| `OPSEC-LESSON` | Tradecraft or OPSEC mistake or improvement | `80-privacy-security/` or relevant skill |
| `ARCH-LESSON` | Structural/architecture observation (routing drift, schema gap, junk-drawer, broken invariant) | `CLAUDE.md`, `00-index/frontmatter-schema.md`, or this skill |

### Session File Format

Add a `## Flagged Observations` section to the session file when something unexpected was directly observed. Place it between `## Key Findings` and `## Artifacts`. Leave the section absent if nothing arose. These are candidate flags — not authoritative lessons.

```markdown
## Flagged Observations

### [TOOL-EDGE-CASE | malware-analysis | HIGH]
**Tool:** floss
**Condition:** Custom-packed ELF with obfuscated string table (UPX variant)
**Symptom:** Silent exit code 0, no output
**Observed resolution:** `--minimum-length 4` — confirmed working in this session
**Confidence:** Directly observed
**Destination:** `10-skills/malware-analysis.md` → floss section

### [FALSE-POSITIVE | threat-research-ioc | MED]
**Pattern:** CDN exit nodes (Cloudflare/Akamai ranges) flagged as C2 in passive DNS
**Context:** Occurs when target uses a CDN; shared IP generates false hits
**Observed resolution:** Not confirmed in session — analyst to investigate
**Confidence:** Inferred — not confirmed in session
**Destination:** `10-skills/threat-research-ioc.md` → passive DNS section
```

**Priority levels:**
- `HIGH` — changes recommended practice; other analysts will repeat the mistake without this
- `MED` — useful refinement, not urgent
- `LOW` — minor detail; apply opportunistically

**Capture rules:**
- One entry per distinct observation — do not combine unrelated events
- Be specific about the condition; vague observations ("tool can fail sometimes") have no value
- `**Observed resolution:**` — only populate if the resolution was directly tried and confirmed in this session; otherwise write "Not confirmed in session — analyst to investigate"
- `**Confidence:**` — always fill: "Directly observed" or "Inferred — not confirmed in session"
- Name the proposed destination file and section — this is a suggestion for later, not a commitment
- Tag `NEW-SKILL-NEEDED` if the observation implies a skill file that doesn't exist yet

---

## Phase 2 — Aggregate (distillation run)

The distillation run reads session files and writes entries to the lessons log. It does not read or modify any skill file.

**Step 0 — Read the curation log**

Read `00-index/vault-curation-log.md`. Note the date of the last run and the last session file processed. All sessions after that date are candidates.

```bash
find /home/user/eolas-vault/60-sessions/ -name "*.md" \
  -newer /home/user/eolas-vault/00-index/vault-curation-log.md \
  | sort
```

**Step 1 — Collect candidate sessions**

For each session file, note whether it has a `## Flagged Observations` section (structured, extract directly) or substantial `## Key Findings` (unstructured, requires inference). Sessions with neither can be skipped. Legacy sessions use `## Lessons Learned` — treat as equivalent.

**Step 2 — Extract lessons**

For each candidate:
1. Pull tagged `## Lessons Learned` entries directly
2. Scan `## Key Findings` for implicit lessons — phrases like "failed when", "workaround", "first observed", "false positive", "effective combination"
3. Mark inferred lessons `[INFERRED]`; mark ambiguous ones `[AMBIGUOUS — analyst review]`

Do not invent lessons. If a finding doesn't clearly generalise, skip it.

**Step 3 — Append to the lessons log**

Write each extracted lesson as a new entry in `00-index/lessons-log.md` under the appropriate destination section. Use the format specified in that file.

The lessons log is append-only during aggregation. Do not modify existing entries. Do not open or read any skill file.

**Step 4 — Commit the aggregation**

One commit per distillation run:

```
chore(vault): distillation run N — M lessons added to lessons log

Sessions processed: [session file names]
Lessons added: [count by type]
Curation log: 00-index/vault-curation-log.md
```

Record the short commit hash — it goes into the curation log.

**Step 5 — Update the curation log**

Update `00-index/vault-curation-log.md`:
- Set last run date and last session processed
- Record the commit hash
- Add a Run N entry

---

## Phase 3 — Review (analyst-driven)

No Claude involvement unless the analyst asks.

Read `00-index/lessons-log.md`. For each open lesson, decide:

| Decision | Meaning | Action |
|----------|---------|--------|
| `apply` | This lesson should update a skill file | Initiate Phase 4 |
| `reject` | Not worth adding; context-specific or already covered | Mark rejected in log |
| `defer` | Possibly worth adding but not now | Leave open |
| `superseded` | A newer lesson in the log makes this one redundant | Mark superseded |

The lessons log has a status column for this. Review can happen any time — after a distillation run, before starting a new investigation, or when writing or updating a skill file.

---

## Phase 4 — Apply (explicit, analyst-initiated)

**Trigger:** Analyst nominates one or more specific lessons from the log and asks Claude to apply them. The request should be explicit: "Apply lesson [ID] to [file]" or "I want to update malware-analysis.md — apply all open HIGH lessons for it."

**Procedure:**

1. Read the nominated lessons from the lessons log
2. Read the target section of the skill file
3. Propose a surgical edit — one paragraph or less; preserve existing structure and voice
4. Show the proposal to the analyst before applying
5. Apply only after explicit approval
6. Mark the lesson as `applied` in the lessons log with the date

**Proposal format:**

```
FILE:    10-skills/malware-analysis.md
SECTION: floss
AFTER:   "Basic usage: `floss <binary>`"
CONTENT:
---
**Edge case — packed samples:** On UPX-variant-packed ELFs with obfuscated
string tables, floss exits silently with exit code 0 and produces no output.
Workaround: use `--minimum-length 4` and run on the unpacked binary if
available. Observed: 2026-01-14.
---
Source: lessons-log entry L-001 (session 2026-01-14-malware-triage-elf.md)
APPROVE? [y/n/modify]
```

**Commit convention for applications:**

Each application session should produce one commit per skill file updated (not one per lesson):

```
feat(skills): update malware-analysis — 2 lessons applied

Applied lessons:
- L-001 (TOOL-EDGE-CASE): floss + UPX packing
- L-004 (TOOL-SUCCESS): capa + floss pipeline order

Source: 00-index/lessons-log.md
```

**Version control and recovery:**

The vault is a git repository. Because application commits are labeled, recovering a previous version of a skill file is straightforward:

```bash
# See all commits that touched a specific skill file
git log --oneline -- 10-skills/malware-analysis.md

# View the file before a specific application commit
git show <hash>~1:10-skills/malware-analysis.md

# Restore a file to its pre-application state
git checkout <hash>~1 -- 10-skills/malware-analysis.md
git commit -m "revert(skills): restore malware-analysis.md to pre-application state"
```

`00-index/lessons-log.md` records which commit hash corresponds to which application session, so you can trace "when was lesson L-001 applied?" directly to the correct git hash.

---

## Prompt Colocation Rule

When reviewing session lessons, apply this rule when deciding whether a prompt belongs in `30-prompts/` as a standalone file or embedded in the skill file that uses it:

**Move into the skill file if all three conditions hold:**
1. The prompt belongs to exactly one skill (single-skill)
2. The prompt is under ~80 lines
3. The execution trigger is not an orchestration script that calls multiple skills

**Keep in `30-prompts/` if:**
- The prompt is a multi-step orchestrator that references more than one skill
- The prompt is longer than ~100 lines (would dominate the skill file)
- The prompt is shared by more than one skill

## Vault Architecture Principles

Structural rules that apply across all phases. Learned from operational incidents; do not re-derive case-by-case.

### Execution prompts must inline external schemas (L-022)

If an execution prompt references a schema defined in another file (e.g., "see CLAUDE.md Phase 6 for the MISP schema"), that schema will be unavailable in any context where the other file is not loaded. The LLM silently falls back to fabricating the schema from training data — producing plausible-looking but incorrect output (wrong field names, invented blocks).

**Rule:** Any schema, format, or field definition that a prompt depends on must be inlined into the prompt or the skill file containing it. Cross-context schema references silently degrade to hallucination.

### Private content requires directory-level segregation, not instructions (L-023)

"Do not surface" or "do not quote" instructions are insufficient protection for private biographical or psychological content loaded into the context window. Attention leakage causes the content to implicitly shape output (register, framing, word choice) even without direct quotation.

**Rule:** Content that must never influence public-facing outputs must be in a separate directory that is structurally excluded from loading — not in the same directory with an instruction not to use it.

Two complementary mechanisms implement this:

1. **Metadata** — every file carries `sensitivity: public | internal | private`
   (see `00-index/frontmatter-schema.md`). `vault-doctor.py` enforces the invariant
   that a `public` file never links to a `private` one, so a leak shows up as a
   build error rather than a silent attention hazard.
2. **Physical separation for the most sensitive tiers** — `private` content
   (personal, financial, identity, secrets) is strongest when it lives in a
   *separate repository* pulled in as an optional git submodule, or is kept out of
   the agent's working tree entirely. A directory in the same repo guarded only by
   a load rule is the instruction-based guard this lesson warns against. Pattern:

   ```bash
   # private content as an optional submodule, never cloned by default consumers
   git submodule add git@host:you/vault-private.git 90-personal
   echo "90-personal/" >> .gitignore   # if kept local-only instead of a submodule
   ```

### Agentic git operations require absolute paths (L-028)

`cd <dir> && git mv` fails when CWD resets between invocations — common in agentic multi-step workflows where each tool call may start in the original working directory.

**Rule:** Always use `git -C /absolute/path mv <src> <dest>` with fully qualified paths. Create the destination directory first with `mkdir -p` if it doesn't exist. Never rely on `cd` + relative paths across separate tool invocations.

```bash
# WRONG — CWD reset between invocations breaks this:
# cd /home/user/eolas-vault && git mv old-path/file.md new-path/file.md

# RIGHT:
mkdir -p /home/user/eolas-vault/new-path/
git -C /home/user/eolas-vault mv old-path/file.md new-path/file.md
```

---

## Structural Integrity (vault-doctor)

The curation loop above keeps *methodology* accurate. A second, faster loop keeps
the *structure* sound. They are different problems: methodology drift is a matter
of judgement (an analyst decides), but structural drift is mechanical (a file lost
its frontmatter, a directory went unrouted, a link broke, a `public` file linked to
a `private` one) and should be caught automatically, not noticed by luck.

`97-scripts/vault-doctor.py` is that enforcement. The principle: **the vault is
strong on process discipline but needs enforced invariants — structure guaranteed
regardless of behaviour.** See `97-scripts/README.md` for the full check list.

**When it runs:**

| Moment | How |
|--------|-----|
| Every commit | `.githooks/pre-commit` (enable once: `git config core.hooksPath .githooks`) |
| Every push / PR | `.github/workflows/vault-doctor.yml` runs `--strict` |
| Every distillation run | Run `vault-doctor.py` as Step 0 — never aggregate on a structurally broken vault |
| After any move/rename/new section | Run by hand before committing |

**Architectural lessons (`ARCH-LESSON`)** are applied differently from methodology
lessons. They do not edit skill files; their destinations are `CLAUDE.md` (routing
and rules), `00-index/frontmatter-schema.md` (the field contract), or this file. When
a structural lesson implies a new invariant, the best application is **a new check in
`vault-doctor.py`** so the same drift can never recur — encode the lesson as code, not
just prose.

---

## Context-File Maintenance (System Prompt Hygiene)

The agent context file — `AGENTS.md` here, plus its tool adapters `CLAUDE.md` and `GEMINI.md` — is a system prompt, not documentation. Every token in it is paid on every exchange in every session that loads it. This is fundamentally different from skill files, which are only loaded on demand. The principles below use `AGENTS.md` as the worked example; they apply equally to any always-loaded context file.

**The key distinction:**
- Skill files in `10-skills/` — loaded explicitly when needed; their length costs nothing at session start
- `AGENTS.md` (and adapters) — always loaded; every line is a fixed per-session charge

A 5,000-line skill file is fine. A 500-line `AGENTS.md` is worth auditing. Because the adapters point back to `AGENTS.md`, audit and trim `AGENTS.md` itself — keep `CLAUDE.md`/`GEMINI.md` thin.

### Maintenance triggers

| Trigger | Action |
|---------|--------|
| `AGENTS.md` has grown by 500+ tokens since last audit | Run a trim pass |
| Migrating to a new model version | Recalibrate — recount tokens, re-verify caching threshold, re-test instruction-following |
| Session behavior is inconsistent (wrong tool chosen, instructions ignored) | Audit for conflicting or redundant instructions |
| Quarterly vault maintenance | Review the context file and adapters for stale entries |

### What to trim

- Skill table entries for skills that no longer exist or have been renamed
- Rules stated in two or more places (keep the most precise one; remove the others)
- Explanatory prose that belongs in the skill file, not the system prompt
- Sections that are never triggered in practice
- Dead cross-references (files that have moved without updating the pointer)

### Trim procedure

1. **Measure token count before.** Quick estimate: `python3 -c "t=open('AGENTS.md').read(); print(len(t.split())*1.35, 'est tokens,', len(t), 'chars')"`  
   For a precise count, use `tiktoken` — see `50-knowledge/system-prompt-token-management.md`.

2. **Remove one category at a time.** Don't bulk-delete — trim, then verify.

3. **Verify key behaviors still hold.** At minimum: does the skill table still point to existing files? Do the core rules still read coherently as instructions?

4. **For significant trims (>200 tokens removed):** run an eval suite — compare task behavior before/after. See `50-knowledge/system-prompt-token-management.md` → Evals-driven optimization.

5. **Commit:** `chore(vault): trim AGENTS.md — N tokens removed`

### Full reference

`50-knowledge/system-prompt-token-management.md` — covers token counting methods, per-model calibration, evals-driven optimization workflow, session lifecycle management.

---

## What does NOT happen automatically

To be explicit about the boundaries:

- Claude does **not** propose skill file edits during aggregation
- Claude does **not** apply lessons in the background
- Claude does **not** open skill files during a distillation run
- Lessons in the log carry no implication that they will be applied — they are observations waiting for a decision

The lessons log is an inbox, not a work queue.
