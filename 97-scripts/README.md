---
title: "97-scripts — Orchestration Script Library"
type: reference
tags: [scripts, deployment, pipeline, maintenance]
status: active
last_updated: 2026-01-15
---

# 97-scripts — Orchestration Script Library

Canonical copies of orchestration scripts that implement vault-documented workflows. The vault is the source of truth; deployed copies on runtime hosts are derived from here.

---

## Why This Exists

The "ghost environment" problem: methodology files in `10-skills/` and `40-workflows/` reference scripts that live on runtime hosts. If a host is redeployed or a script is updated without updating the vault, an LLM using the vault will follow stale instructions or propose changes that conflict with the actual code.

This section closes that gap. Scripts live here first; runtime hosts are deployments.

---

## Contents

| Directory | Scripts | Skill / reference file | Runtime host |
|-----------|---------|----------------------|--------------|
| `malware-analysis/` | `pipeline.py`, `pipeline_local.py`, `dynamic.py`, `report.py`, `yara_gen.py` | `10-skills/malware-analysis.md` | analysis-server (REMnux) |
| `cti/` | `misp_ingestion_pipeline.py` | `10-skills/misp-ingestion.md` | analysis-server |
| `kali-worker/` | `influence_ops.py`, `osint.py` | `10-skills/influence-ops-media.md` | kali-worker (Kali) |
| `slack-intel/` | `slack_scraper.py`, `mcp_server.py`, `config.yaml.template`, `kg_triples.py` | `10-skills/slack-intel-collection.md` | analysis-server |

---

## Deployment Pattern

Scripts flow vault → runtime host, never the other direction.

```
┌──────────────────────────────┐     git pull      ┌─────────────────────┐
│  eolas-vault/97-scripts/     │ ──────────────►  │  Runtime host       │
│  (source of truth, git)      │                   │  /home/user/...     │
└──────────────────────────────┘                   │  (deployed copy)    │
                                                   └─────────────────────┘
```

**To deploy a script to a runtime host:**

```bash
# From the vault working copy
scp 97-scripts/malware-analysis/pipeline.py analysis-server:/home/user/malware-llm-pipeline/
# or rsync the whole directory
rsync -av 97-scripts/malware-analysis/ analysis-server:/home/user/malware-llm-pipeline/
```

**To update the vault when a script changes on a runtime host:**

```bash
# Copy back to vault working copy, then commit
scp analysis-server:/home/user/malware-llm-pipeline/pipeline.py \
    /path/to/vault/97-scripts/malware-analysis/
git add 97-scripts/malware-analysis/pipeline.py
git commit -m "chore(scripts): sync pipeline.py from analysis-server runtime"
git push origin main
```

---

## LLM Usage Notes

When helping with any pipeline code in this vault:

1. **Read the script here first** before proposing changes. The vault copy is the canonical version; don't assume the runtime host matches if you haven't checked the git diff.
2. **Never commit `.env` files or any credential file** to this directory — credentials follow the rule in `70-credentials/`.
3. **Hardcoded path constants** exist in some scripts. These are expected; they are host-specific and are noted for deployment reconfiguration, not for patching here.

---

## Known Deployment Gotchas

### pipeline.py — always invoke via venv

`pipeline.py` has a `#!/usr/bin/env python3` shebang. On Ubuntu 24.04 (PEP 668), this resolves to system Python which cannot find `anthropic`, `yara-python`, `pefile`, `capstone`, `vt-py` etc. (all installed in `.venv`).

**Always invoke as:**
```bash
.venv/bin/python3 pipeline.py [args]
```

Alternatively, patch the shebang to `#!/home/user/malware-llm-pipeline/.venv/bin/python3`.

### Ubuntu 24.04 — REMnux installer requires DEB822 sources format

Ubuntu 24.04 images ship with legacy `/etc/apt/sources.list`. The REMnux installer expects DEB822 format at `/etc/apt/sources.list.d/ubuntu.sources`. Without it, 3 cascading salt state failures occur.

**Pre-install step (before running REMnux installer):**
```bash
cat > /etc/apt/sources.list.d/ubuntu.sources << 'EOF'
Types: deb
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
EOF
apt-get update
```

Then run the REMnux installer as normal.

### xrdp — must add xrdp to ssl-cert group post-install

xrdp default install does not add the `xrdp` user to the `ssl-cert` group. All TLS handshakes fail with `Permission denied` reading `/etc/ssl/private/ssl-cert-snakeoil.key`. From the client this appears as connection refused or TLS error.

**Post-install:**
```bash
usermod -aG ssl-cert xrdp
systemctl restart xrdp
```

This must be included in any rebuild automation to survive host redeployments. See also `75-remote-orchestration/fresh-install-template.md`.
