---
title: "Scripts — Canonical Pipeline Code"
type: reference
id: script-scripts
volatility: periodic
sensitivity: public
tags: [scripts, pipeline, automation, vault]
status: active
last_updated: 2026-06-12
---

# Scripts — Canonical Pipeline Code

This section holds canonical copies of the pipeline scripts that implement vault workflows. The vault is the **source of truth** — runtime hosts are deployments of it.

---

## The Core Idea: Scripts Are Extensions of Skills

Every script in this vault connects upward to a skill file and a workflow. The chain looks like this:

```
10-skills/skill-name.md          ← methodology: what to do and why
    └── 40-workflows/workflow.md  ← sequence: phases, inputs, outputs
            └── 97-scripts/dir/script.py  ← code: the actual implementation
                    └── 70-credentials/   ← secrets: env vars, config paths
```

**Why this matters for agentic AI:** When an LLM helps you run a workflow, it reads the skill file to understand the goal, reads the workflow for the sequence, and reads the script to understand the implementation. If any link in that chain is out of date, the LLM will give you advice that conflicts with what your code actually does. Keeping the chain intact is the vault's fundamental maintenance job.

---

## Directory Structure

```
97-scripts/
├── README.md                  ← this file
├── <domain>/
│   ├── README.md              ← what the scripts do, deployment notes
│   └── script.py             ← canonical script
└── checksums.json             ← SHA256 of each script (integrity check)
```

Each subdirectory maps to one analytical domain. Example mapping:

| Directory | Linked skill | Linked workflow | What the script does |
|-----------|-------------|----------------|---------------------|
| `ioc-enrichment/` | `10-skills/threat-research-ioc.md` | `40-workflows/ioc-triage.md` | Queries VT, DNSDB, Shodan; outputs structured JSON |
| `knowledge-graph/` | `50-knowledge/knowledge-graphs/` | `40-workflows/kg-build.md` | NER extraction, SVO triples, graph population |
| `report-generation/` | `85-writing/infosec-report-writing.md` | `40-workflows/reporting.md` | Converts structured findings JSON → HTML/MD report |

---

## Deployment Pattern

Scripts flow **vault → runtime host**, never the reverse.

```
┌─────────────────────────────┐              ┌──────────────────────┐
│  vault/97-scripts/          │  scp/rsync   │  Runtime host        │
│  (source of truth, git)     │ ──────────►  │  /home/user/...      │
└─────────────────────────────┘              └──────────────────────┘
```

When you update a script on a runtime host (during active work), copy it back to the vault and commit before closing the session. The vault copy is always the clean, session-hack-free version.

```bash
# Deploy to runtime host
scp 97-scripts/ioc-enrichment/enrich.py analysis-server:/home/user/ioc-pipeline/

# Sync back after iterating on the host
scp analysis-server:/home/user/ioc-pipeline/enrich.py 97-scripts/ioc-enrichment/
git add 97-scripts/ioc-enrichment/enrich.py
git commit -m "chore(scripts): sync enrich.py from analysis-server"
```

---

## Secrets in Scripts

Scripts read secrets from environment variables — never hardcoded values:

```python
import os

API_KEY  = os.environ["SERVICE_API_KEY"]       # mandatory — fail loud if missing
BASE_URL = os.environ.get("API_URL", "https://api.service.com")  # optional with default
```

The corresponding entry in `70-credentials/api-keys-inventory.md` records which environment variable to set and which config file holds the actual value. The vault never holds the value itself.

---

## LLM Rules for This Section

When an LLM assists with scripts in this vault:

1. **Read the script before proposing changes.** The vault copy is canonical; don't assume the runtime matches unless you've verified with a checksum or diff.
2. **Never commit `.env` or any file containing credentials** — only the environment variable name belongs here.
3. **Update the corresponding skill or workflow file** in the same commit when the script's interface (inputs, outputs, flags) changes. An LLM reading a stale skill file will give the wrong instructions.

---

## How to Add a New Script

1. Create a subdirectory for your domain.
2. Write a `README.md` there: what the script does, required inputs, expected outputs, deployment host.
3. Write the script. Use env vars for all secrets.
4. Add a `## Scripts` section to the relevant skill file linking to this script.
5. Reference the script in the relevant workflow's step table.
6. Add to `checksums.json`: `sha256sum 97-scripts/domain/script.py`.
7. Commit skill file, workflow file, and script together.

---

## vault-doctor.py — Structural Integrity Checker

`vault-doctor.py` is the vault's **enforced-invariants layer**. The curation
process governs how humans and agents *should* behave; vault-doctor guarantees
structural properties *regardless* of behaviour. It is the answer to the failure
mode where the routing layer (CLAUDE.md) silently drifts out of sync with the
filesystem, or files are created without frontmatter and become invisible to
every query.

**What it checks** (ERROR fails the run; WARN is advisory unless `--strict`):

| Check | Level | Why |
|-------|-------|-----|
| Frontmatter present | ERROR | Untyped files are invisible to grep/Dataview |
| Required fields (`title,id,type,status,volatility,sensitivity`) | ERROR | The machine contract |
| Enum conformance (type/status/volatility/sensitivity) | ERROR | Drift between schema doc and files |
| `id` globally unique | ERROR | Stable identity must be unambiguous |
| Nav parity — every `NN-section/` routed in `AGENTS.md` | ERROR | Unrouted dirs are unreachable by an agent |
| Backtick paths in `AGENTS.md` resolve | ERROR | Dead pointers in the system prompt |
| Internal links resolve (wiki-links and `(file.md)` links) | ERROR | Broken navigation |
| Sensitivity segregation — `public` ↛ `private` | ERROR | Privacy boundary, machine-checked |
| Public-repo leakage (`--public-repo`) | ERROR | `internal`/`private` file lacking `publish: true` clearance |
| Directory overload | WARN | Junk-drawer detector — split by volatility |
| Missing `last_updated` (or `date`) | WARN | Staleness signal |

Exempt from frontmatter/link checks: templates (`_template.md`) and the **root-level**
instruction docs only (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`). A `README.md`
inside a section folder is a real item and **is** validated like any other file.

**Usage:**

```bash
python3 97-scripts/vault-doctor.py                       # human-readable, errors fail
python3 97-scripts/vault-doctor.py --strict              # warnings also fail (use in CI)
python3 97-scripts/vault-doctor.py --strict --public-repo  # also flag uncleared internal/private files
python3 97-scripts/vault-doctor.py --json                # machine-readable
```

Pure standard library — no install step.

**Enforcement:**

- **Pre-commit:** `git config core.hooksPath .githooks` (once per clone). The
  `.githooks/pre-commit` hook blocks commits that introduce structural errors.
- **CI:** `.github/workflows/vault-doctor.yml` runs `--strict --public-repo` on every push and PR.
- **Secret scanning:** `.github/workflows/secret-scan.yml` runs `gitleaks` on every push and
  PR — a content-based complement to vault-doctor's classification check. vault-doctor catches a
  file *labelled* non-public; gitleaks catches a real secret regardless of label. Masked example
  values (the `•` placeholders) are allowlisted in `.gitleaks.toml` by pattern, not by path, so the
  credentials section is still scanned for genuine leaks.

The canonical field definitions it enforces live in `00-index/frontmatter-schema.md`.
