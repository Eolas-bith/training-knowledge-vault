---
title: "Remote Orchestration — Section Index"
type: reference
tags: [remote-orchestration, infrastructure, deployment, automation]
status: active
last_updated: 2026-01-15
---

# Remote Orchestration

## Purpose

This section documents the remote infrastructure used to support analysis workflows — host roles, deployment procedures, and the orchestration patterns that connect them.

"Remote orchestration" in this vault means: coordinating work across multiple machines (analysis server, KB server, worker nodes) via SSH, Tailscale, and automated triggers. It does not mean Kubernetes or cloud orchestration.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│  Tailscale Mesh (private, encrypted)                         │
│                                                              │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  analysis-server │    │  kali-worker     │               │
│  │  Ubuntu + REMnux │    │  Kali Linux      │               │
│  │  Malware pipeline│    │  OSINT / crawl   │               │
│  │  MISP            │    │  Playwright      │               │
│  │  Claude Code     │    │                  │               │
│  └──────────────────┘    └──────────────────┘               │
│           │                                                  │
│  ┌────────▼─────────┐                                        │
│  │  kb-server       │                                        │
│  │  macOS           │                                        │
│  │  Obsidian vault  │                                        │
│  │  Git remote      │                                        │
│  └──────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Contents

| File | Description |
|------|-------------|
| `fresh-install-template.md` | Template for provisioning a new analysis host from scratch |

---

## Host Roles

| Host | Primary Role | Key Software |
|------|--------------|-------------|
| `analysis-server` | Malware analysis, CTI pipeline, MISP | REMnux, malcat, Claude Code, MISP |
| `kali-worker` | OSINT, web crawling, influence ops investigations | Kali tools, Playwright, Python |
| `kb-server` | Knowledge base, Obsidian sync, git remote | Obsidian, git |

---

## Deployment Pattern

The vault is the source of truth for scripts and methodology. Changes flow from vault to runtime hosts, not the reverse.

```
eolas-vault/97-scripts/  ──git pull──►  Runtime host deployed copy
(source of truth)
```

To deploy a script update:
```bash
scp /path/to/vault/97-scripts/malware-analysis/pipeline.py \
    analysis-server:/home/user/malware-llm-pipeline/
```

To pull a script back to the vault after modifying on host:
```bash
scp analysis-server:/home/user/malware-llm-pipeline/pipeline.py \
    /path/to/vault/97-scripts/malware-analysis/pipeline.py
# Then commit the vault change
```

---

## Linked Resources

- Script library: [[97-scripts/README]]
- SSH configuration: [[70-credentials/ssh-config]]
- Fresh install template: [[75-remote-orchestration/fresh-install-template]]
