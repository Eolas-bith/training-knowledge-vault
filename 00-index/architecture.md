---
title: "Vault Architecture — Portable Design Contract"
type: index
id: idx-vault-architecture
tags: [architecture, design, trust-zones, provenance, portability, publication]
status: active
volatility: periodic
sensitivity: public
last_updated: 2026-09-20
design_version: 2
---

# Vault Architecture — Portable Design Contract

This document describes the reusable architecture of the training vault. It is
deliberately independent of any person's data, organisation, infrastructure,
provider account, or investigation history. It defines how the vault is shaped,
where different kinds of state belong, and which boundaries must hold as a vault
grows.

## Architectural invariants

1. **Markdown remains the human-readable source of methodology.** Skills,
   workflows, prompts, references, and sessions stay readable by people, grep,
   Obsidian, and agents without a proprietary database.
2. **Methodology and runtime state are separate.** Samples, generated reports,
   temporary output, and service state do not live in the methodology tree.
3. **One tool-neutral contract routes every agent.** `AGENTS.md` is canonical;
   tool-specific files are thin adapters and must not duplicate general rules.
4. **Sensitive content is excluded structurally.** Classification metadata helps,
   but content that must never influence public output belongs outside the public
   working tree.
5. **Judgement and mechanical integrity use different loops.** Curation governs
   what the methodology should say; `vault-doctor.py` enforces properties that can
   be checked deterministically.
6. **Published design is re-authored, never synchronized from a private vault.**
   Public changes describe a generic invariant and use synthetic examples.

## Content layers

| Layer | Default location | Responsibility |
|-------|------------------|----------------|
| Routing and indexes | `00-index/` | Navigation, schemas, architecture, curation state |
| Methodology | `10-skills/`, `30-prompts/`, `40-workflows/` | How work is performed and orchestrated |
| Model behavior | `20-llm-configs/`, `22-personas/`, `25-model-map/` | Connection, behavioral contracts, model selection |
| Reference knowledge | `50-knowledge/` | Facts and background, not execution procedure |
| Operational memory | `60-sessions/` | Append-oriented record of what happened |
| Secret pointers | `70-credentials/` | Masked inventory and paths only; never secret values |
| Privacy and profile | `80-privacy-security/`, `81-profile/` | Privacy methodology and explicitly load-gated public-safe profile material |
| Canonical code | `97-scripts/` | Versioned implementations linked to skills and workflows |

The numbering groups stable responsibilities; it is not a requirement to fill
every number. New top-level sections need a distinct responsibility, a route from
`AGENTS.md`, and a reason they do not fit an existing layer.

## Trust zones and write policy

Prompt instructions are useful behavior guidance, not a security boundary. An
executor that can write anywhere under the same operating-system identity can
still alter protected methodology. Use progressively stronger controls:
filesystem permissions where practical, code-level path policy in executors, and
prompt instructions as the final layer.

| Zone | Contents | Normal write policy |
|------|----------|---------------------|
| A — Methodology | Indexes, skills, prompts, workflows, references, canonical scripts | Read-only during ordinary analysis; writable only in an explicit maintenance pass |
| B — Controlled state | Session notes, curation logs, generated indexes | Create/append or narrowly update through approved workflows |
| C — Runtime output | Samples, report builds, caches, temporary results | Writable in an external project or output directory |
| D — Secrets | API keys, cookies, private keys, session tokens | Outside the vault; referenced only by variable or config path |
| P — Publication | Files intended for a public repository | Allowlisted design or synthetic material that passes publication checks |

Any path-policy implementation should normalize absolute paths, resolve symlinks,
deny moves or redirects into protected paths, and require an explicit maintenance
mode before permitting Zone A writes.

## Scaling with program areas

When one bounded domain needs its own skills, prompts, workflows, references, and
scripts, it may become a **program area**: a top-level section with a small internal
version of the same numbered scheme.

```text
55-example-program/
├── 10-skills/
├── 30-prompts/
├── 40-workflows/
└── 50-knowledge/
```

Promote a domain only when it has several artifact types, an independent
navigation hub, and a distinct lifecycle. A large topic folder containing only
references should remain under `50-knowledge/` and be sub-structured there.

## Provider-neutral task contract

Workflows should express intent without assuming one model provider's transport or
tool-call format. An advanced runner may normalize work into a task record with:

```text
task_id, objective, inputs, context_files, allowed_tools,
read_scope, write_scope, required_output_schema, constraints,
workflow_id, requested_by
```

Provider adapters handle authentication, transport, tool syntax, and response
normalization. Provider-specific wrappers are acceptable; provider-specific copies
of the methodology are not.

## Output provenance

Meaningful generated artifacts should remain understandable after they are moved
away from their original session. Record, where applicable:

```text
timestamp, task_id, workflow_id, skill_id, provider, model,
repository_commit, execution_environment, input_artifacts,
output_schema_version, confidence_mode
```

Markdown outputs may use frontmatter. Non-Markdown output should use a sidecar
machine-readable record; a human-readable summary can accompany it.

## Self-maintenance

The vault uses two complementary loops:

- **Curation:** observations are captured in sessions, aggregated, reviewed by a
  human, and applied only after explicit approval.
- **Structural validation:** `vault-doctor.py`, local hooks, and CI catch missing
  metadata, duplicate identity, navigation drift, broken links, classification
  violations, skills-index drift, and references to deprecated material.

Neither loop replaces the other. A structurally valid file can contain poor
methodology, and excellent methodology can become unreachable if the structure
drifts.

## Public-template boundary

The public repository is its own source of truth. Do not merge, cherry-pick, or
copy trees from an operational or private vault. Instead:

1. State the reusable problem without names, paths, counts, incidents, or examples
   from the source vault.
2. Express the solution as a generic rule, template, validator check, or synthetic
   example.
3. Implement it directly in the public repository.
4. Run the clean-room workflow in
   [[40-workflows/public-template-maintenance]].

This boundary applies to Git history and commit metadata as well as file contents.
Deleting a sensitive line later does not remove it from published history.

## When to revisit the architecture

Review this contract when a new top-level section is proposed, an agent gains a
new write path, a second provider needs separate workflow logic, runtime artifacts
begin appearing in the vault, private material enters normal agent context, or a
publication check catches a leak. Apply the resulting lesson as an enforced
invariant when it is mechanically testable.
