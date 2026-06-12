---
title: "Scripts — Canonical Pipeline Code"
type: reference
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
