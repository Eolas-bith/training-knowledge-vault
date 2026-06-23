---
title: "Lessons Log"
type: reference
id: idx-lessons-log
volatility: periodic
sensitivity: public
tags: [vault, lessons, distillation, knowledge-management]
status: active
last_updated: 2026-01-15
---

# Lessons Log

Central inbox for operational knowledge extracted from session files. Populated by distillation runs. **Skill files are not touched until the analyst explicitly initiates Phase 4 (Apply) from `10-skills/vault-curation.md`.**

---

## How to Use This File

**During a distillation run:** Append new entries to the relevant destination section. Do not modify existing entries. Do not open or read skill files.

**During analyst review:** Update the status column for each entry:
- `open` — not yet decided
- `apply` — nominated for application to the skill file
- `rejected` — not worth adding (note reason)
- `deferred` — possibly worth adding; revisit later
- `superseded` — made redundant by a newer lesson; note which one

**During a Phase 4 application session:** After applying a lesson to a skill file, update its status to `applied` and record the commit hash.

---

## Entry Format

Each section corresponds to a destination file. Within each section, lessons appear in a summary table followed by full entries.

```markdown
## [destination file path]

| ID | Date | Type | Summary | Priority | Status |
|----|------|------|---------|----------|--------|
| L-001 | YYYY-MM-DD | TOOL-EDGE-CASE | one-line summary | HIGH | applied |

### L-001 — [TYPE] [short title] — YYYY-MM-DD
**Source:** 60-sessions/analysis-server/[session-file].md
**Condition:** [when does this apply?]
**Observation:** [what was observed?]
**Recommended change:** [what should be added or changed in the destination file?]
**Status:** applied
**Applied in commit:** — (fill when applied)
```

---

## 10-skills/malware-analysis.md

| ID | Date | Type | Summary | Priority | Status |
|----|------|------|---------|----------|--------|
| L-001 | 2026-01-14 | TOOL-EDGE-CASE | floss silent exit on UPX-packed ELF with obfuscated string table | HIGH | applied |
| L-004 | 2026-01-14 | TOOL-SUCCESS | capa + floss pipeline order: floss first, strings into capa context | MED | applied |

### L-001 — TOOL-EDGE-CASE floss silent exit on UPX-packed ELF — 2026-01-14
**Source:** `60-sessions/analysis-server/2026-01-14-malware-triage-elf.md` → Key Findings
**Condition:** UPX-variant-packed ELF with obfuscated string table; floss exits silently with exit code 0, no output
**Observation:** Running floss against a UPX-packed sample produced zero output and exit code 0 — no error message. Running on the unpacked binary (after `upx -d`) with `--minimum-length 4` produced expected string output.
**Recommended change:** Add a note to the floss section: "On UPX-packed ELF samples, floss may exit silently with code 0 and produce no output. Unpack with `upx -d` first; use `--minimum-length 4` on the unpacked copy."
**Priority:** HIGH
**Status:** applied
**Applied in commit:** a1b2c3d

### L-004 — TOOL-SUCCESS capa + floss pipeline order — 2026-01-14
**Source:** `60-sessions/analysis-server/2026-01-14-malware-triage-elf.md` → Completed
**Condition:** Standard ELF static analysis pipeline
**Observation:** Running floss before capa and feeding decoded strings into the capa invocation context improved technique coverage — capa matched 3 additional rules that relied on string evidence.
**Recommended change:** Add ordering note to pipeline section: "Run floss before capa; decoded/stack strings from floss can improve capa rule matching when injected as context."
**Priority:** MED
**Status:** applied
**Applied in commit:** a1b2c3d

---

## 10-skills/threat-research-ioc.md

| ID | Date | Type | Summary | Priority | Status |
|----|------|------|---------|----------|--------|
| L-002 | 2026-01-13 | METHOD-REFINEMENT | IOC confidence gate: hold below 50% before deploying resources | HIGH | applied |
| L-003 | 2026-01-13 | FALSE-POSITIVE | CDN IP ranges (Cloudflare/Akamai) generate false C2 hits in passive DNS | MED | applied |

### L-002 — METHOD-REFINEMENT IOC confidence gate — 2026-01-13
**Source:** `60-sessions/analysis-server/2026-01-13-ioc-enrichment-pivot.md` → Key Findings
**Condition:** IOC enrichment workflow; confidence assessment before committing investigation resources
**Observation:** Confidence dropped from 75% to 20% after enrichment revealed shared infrastructure. Without a formal gate, investigation resources would have been deployed on a false lead.
**Recommended change:** Add confidence gate to Phase 3 (Pivoting): "Confidence <50% → HOLD. Do not deploy resources or push to MISP without analyst review."
**Priority:** HIGH
**Status:** applied
**Applied in commit:** a1b2c3d

### L-003 — FALSE-POSITIVE CDN IP ranges in passive DNS — 2026-01-13
**Source:** `60-sessions/analysis-server/2026-01-13-ioc-enrichment-pivot.md` → Key Findings
**Condition:** Passive DNS lookup on a target domain that uses a CDN (Cloudflare, Akamai, Fastly)
**Observation:** Passive DNS returned shared CDN exit IPs flagged as C2 — these are shared infrastructure hosting thousands of legitimate sites. The target's use of a CDN causes all its domains to resolve to CDN ranges, which appear in passive DNS alongside genuinely malicious domains.
**Recommended change:** Add to Tool Gotchas: "CDN exit IPs (Cloudflare, Akamai, Fastly) generate false positive C2 hits in passive DNS. When a target uses a CDN, filter out CDN ASN ranges before treating IPs as dedicated C2 infrastructure."
**Priority:** MED
**Status:** applied
**Applied in commit:** a1b2c3d

---

## ID Counter

**Last ID assigned:** L-005

*(Increment from L-005 in the next distillation run)*
