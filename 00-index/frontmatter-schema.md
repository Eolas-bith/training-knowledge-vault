---
title: "Frontmatter Schema — Canonical Field Reference"
type: index
id: idx-frontmatter-schema
tags: [schema, frontmatter, metadata, validation, architecture]
status: active
volatility: periodic
sensitivity: public
last_updated: 2026-06-23
---

# Frontmatter Schema — Canonical Field Reference

This file is the **single source of truth** for vault frontmatter. `CLAUDE.md`
summarises it; the validator (`97-scripts/vault-doctor.py`) enforces it; the
`_template.md` files instantiate it. If any of those disagree with this file,
this file wins — fix the others.

Every content and index file carries a YAML frontmatter block delimited by `---`
at the very top of the file. The root `README.md` and `CLAUDE.md` are the only
exempt files (they are documents *about* the vault, not items *in* it).

---

## Fields

| Field | Required | Applies to | Allowed values |
|-------|----------|-----------|----------------|
| `title` | yes | all | free text |
| `id` | yes | all (except `_template.md`) | stable slug, globally unique — see below |
| `type` | yes | all | `skill \| prompt \| llm-config \| persona \| workflow \| reference \| session \| index \| section-index \| session-index` |
| `status` | yes | all | `active \| draft \| deprecated \| in-progress \| complete` |
| `volatility` | yes | content + index | `stable \| periodic \| volatile` |
| `sensitivity` | yes | content + index | `public \| internal \| private` |
| `tags` | recommended | all | list |
| `llms` | optional | skill, prompt, llm-config, persona | list |
| `source_playbook` | optional | skill | path to canonical source |
| `last_updated` | recommended | all | `YYYY-MM-DD` |
| `publish` | optional | any `internal`/`private` file | `true` — explicit clearance to ship in a public repo |

Type-specific extra fields (e.g. `session_id`, `run_dir`, `cut_off_date`,
`actor_type`) are documented in the relevant `_template.md` and are not
constrained by the validator beyond presence checks where noted.

---

## `publish` — publication clearance, separate from classification

`sensitivity` answers *"who may load this?"*; `publish` answers a different
question: *"is this specific file cleared to ship in a published (public) repo?"*
They are distinct axes — a file can be classified `private` yet still be safe to
publish because its content is **redacted or synthetic** (e.g. the credential
inventory in this training vault holds only masked placeholders, and the profile
is a stub with no real biographical data).

When `vault-doctor.py` is run with `--public-repo`, any file classified `internal`
or `private` is reported as a **leak** unless it carries `publish: true`. This
catches the failure mode where a genuinely sensitive file is committed to a public
remote, while letting deliberately-published synthetic examples through. The value
must be exactly `true` (no inline comment — the frontmatter parser is line-based).
CI and the pre-commit hook in this repo run with `--public-repo`; drop that flag if
you fork the vault into a private repository.

---

## `id` — identity decoupled from path

**The problem it solves.** When the only identifier for a file is its path, the
path *is* the identity. Every cross-reference, every session log, every index
hard-codes a location — so the structure cannot be reorganised without breaking
references. In an append-only vault (sessions are never edited) this is fatal:
moving a knowledge file silently breaks historical session links that may not be
touched.

**The rule.** Every file gets a permanent `id` that **never changes, even when
the file moves**. Cross-references that must survive reorganisation — especially
from append-only sessions — record the `id`, not the path. Human-facing
navigation can still use Obsidian wikilinks (which resolve by name, not full
path); the `id` is the durable handle for machines and for the audit trail.

**Convention.** `<section-prefix>-<slug>`:

| Section | Prefix | Example |
|---------|--------|---------|
| `00-index/` | `idx` | `idx-skills-index` |
| `10-skills/` | `skill` | `skill-vault-curation` |
| `20-llm-configs/` | `cfg` | `cfg-claude-sonnet` |
| `22-personas/` | `persona` | `persona-analyst-operator` |
| `30-prompts/` | `prompt` | `prompt-vault-distillation` |
| `40-workflows/` | `wf` | `wf-ioc-triage` |
| `50-knowledge/` | `kb` | `kb-ontology-and-llm` |
| `60-sessions/` | `session` | `session-2026-01-15-example-research-synthesis` |
| `70-credentials/` | `cred` | `cred-api-keys-inventory` |
| `80-privacy-security/` | `sec` | `sec-readme` |
| `81-profile/` | `profile` | `profile-readme` |
| `97-scripts/` | `script` | `script-readme` |

Slugs are stable and lowercase; do not encode the path in the slug beyond the
section prefix, so a file can move between sub-folders without its id implying a
stale location.

---

## `volatility` — how often the content changes

Drives review cadence and, critically, **where a file belongs**. The most common
structural failure mode is a single "knowledge" folder becoming a junk drawer
because everything that is not a procedure lands there regardless of how often it
changes. Separate by volatility, not just topic.

| Value | Meaning | Typical content | Review cadence |
|-------|---------|-----------------|----------------|
| `stable` | rarely changes once written | domain reference, ontologies, finished entity profiles, append-only sessions | yearly / on new evidence |
| `periodic` | evolves with practice | methodology (skills, workflows, prompts, personas), indexes | each curation pass |
| `volatile` | changes on an external clock | tool/platform reference, LLM configs, credentials, org/people info | whenever the upstream changes |

**Promotion rule.** When a sub-folder of `stable` knowledge accumulates a cluster
of `volatile` files (e.g. tool runbooks under `50-knowledge/`), that cluster has
outgrown its parent and should be promoted to its own top-level section. The
validator's overload check flags candidates; the decision stays with the analyst.

---

## `sensitivity` — who may load the file

Machine-checkable segregation. Instruction-based guards ("do not surface this")
are insufficient — attention leakage shapes output even without direct quotation.
Sensitivity is the metadata half of the defence; physical separation is the other
half (see `10-skills/vault-curation.md` → Private Content Segregation).

| Value | Meaning | Loading policy |
|-------|---------|----------------|
| `public` | shareable; safe in any output | always loadable |
| `internal` | operational; not for external outputs | loadable for internal work |
| `private` | personal/financial/identity/secrets | load-gated; never influences public outputs; ideally in a separate repo |

**Validator invariant.** A `public` file must not link to a `private` file. A
broken segregation boundary is an error, not a warning.

---

## See also

- `CLAUDE.md` → "Frontmatter fields" (the loaded-every-session summary)
- `97-scripts/vault-doctor.py` (the enforcement)
- `10-skills/vault-curation.md` → "Structural Integrity" (when to run the checks)
