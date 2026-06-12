---
title: "Vault Curation Log"
type: reference
tags: [vault, curation, distillation, maintenance, log]
status: active
last_updated: 2026-01-15
---

# Vault Curation Log

State tracker for the session-to-skill distillation process. Read before starting any distillation run. See [[10-skills/vault-curation]] for the full procedure.

---

## Current State

**Last distillation run:** 2026-01-15
**Last session processed:** `60-sessions/analysis-server/2026-01-14-malware-triage-elf.md`
**Open lessons in log:** 0 (all Run 1 lessons applied 2026-01-15)
**Next scheduled run:** after 5+ sessions accumulate, or 2026-04-15 at latest

---

## Baseline Note

Sessions prior to vault setup predate this logging system. The first distillation run scanned from the earliest available sessions onward.

---

## Distillation History

### Run 1 — 2026-01-15

**Date:** 2026-01-15
**Commit hash:** a1b2c3d — recovery: `git revert a1b2c3d` | `git show a1b2c3d~1:00-index/lessons-log.md`
**Operator:** analyst + Claude (claude-sonnet-4-6)
**Sessions scanned:** 5
**Sessions with lessons:** 3 sessions had extractable lessons; 2 sessions skipped (pure ops/infra, no methodology content)

**Lessons extracted:**
- [TOOL-EDGE-CASE] floss silent exit on UPX-packed ELF → `10-skills/malware-analysis.md` (APPLIED a1b2c3d)
- [METHOD-REFINEMENT] IOC confidence gate: hold at <50% before deploying resources → `10-skills/threat-research-ioc.md` (APPLIED a1b2c3d)
- [FALSE-POSITIVE] CDN IP ranges generating false C2 hits in passive DNS → `10-skills/threat-research-ioc.md` (APPLIED a1b2c3d)
- [TOOL-SUCCESS] capa + floss pipeline order: run floss first, feed strings to capa context → `10-skills/malware-analysis.md` (APPLIED a1b2c3d)
- [KNOWLEDGE-UPDATE] GTPdoor uses BPF socket filtering; raw socket persistence not a unique IOC → `50-knowledge/malware-families/gtpdoor.md` (APPLIED a1b2c3d)

**Lessons added to log:**
- L-001 — TOOL-EDGE-CASE — floss silent exit on UPX-packed ELF (applied a1b2c3d)
- L-002 — METHOD-REFINEMENT — IOC confidence gate (applied a1b2c3d)
- L-003 — FALSE-POSITIVE — CDN IP ranges in passive DNS (applied a1b2c3d)
- L-004 — TOOL-SUCCESS — capa + floss pipeline order (applied a1b2c3d)
- L-005 — KNOWLEDGE-UPDATE — GTPdoor BPF socket persistence (applied a1b2c3d)

**Rejected proposals:**
- Session 2026-01-10 (vault setup): structural work, no methodology lessons
- Session 2026-01-12 (SSH config refresh): ops/infra, not generalizable methodology

**Next run due:** after 5+ new sessions accumulate with Flagged Observations, or 2026-04-15 at latest

---

## Pending Items

**Run 1 complete — no open lessons.** New items will appear here after Run 2 aggregation.

---

## Rejected Proposals Log

Proposals that were reviewed and rejected. Recorded so the same item is not re-proposed.

*(Run 1 rejections documented inline above)*

---

## Notes on Lesson Types Observed

Running tally of lesson types across all runs.

| Lesson type | Count (all runs) |
|-------------|-----------------|
| TOOL-EDGE-CASE | 1 |
| NEW-TTP | 0 |
| METHOD-REFINEMENT | 1 |
| TOOL-SUCCESS | 1 |
| KNOWLEDGE-UPDATE | 1 |
| ANALYTICAL-INSIGHT | 0 |
| FALSE-POSITIVE | 1 |
| OPSEC-LESSON | 0 |
| NEW-SKILL-NEEDED | 0 |

---

## Update Template (for each new run)

```markdown
### Run N — YYYY-MM-DD

**Date:** YYYY-MM-DD
**Commit hash:** [7-char short hash] — recovery: `git revert <hash>` | `git show <hash>~1:path/to/file.md`
**Operator:** analyst + Claude
**Sessions scanned:** [list of session files]
**Sessions with lessons:** [count and file names]

**Lessons extracted:**
- [TYPE] [brief description] → [destination file]
- ...

**Lessons added to log:**
- L-[ID] — [TYPE] — [one-line summary]
- ...

**Rejected proposals:**
- [brief description] — Reason: [why]

**Ambiguous items deferred:**
- [brief description] — Needs: [what information is required to resolve]

**Next run due:** [date or trigger condition]
```
