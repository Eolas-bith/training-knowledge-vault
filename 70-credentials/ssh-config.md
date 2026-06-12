---
title: "SSH Configuration Reference"
type: reference
tags: [credentials, ssh, infrastructure]
status: active
last_updated: 2026-01-15
---

# SSH Configuration Reference

Copy of `~/.ssh/config`. Update this whenever the live config changes.

This file is safe to store in the vault — it contains aliases and public connection details only, no private keys or passwords.

---

## ~/.ssh/config

```
# ── Analysis Server ─────────────────────────────────────────────────────────
Host analysis-server
    HostName <analysis-server-ip>
    User user
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

# ── Tailscale mesh hosts ─────────────────────────────────────────────────────
Host kb-server
    HostName <tailscale-ip>
    User user
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

Host kali-worker
    HostName <tailscale-ip>
    User kaliuser
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
```

---

## Host Inventory

| Alias | Role | OS | Notes |
|-------|------|----|-------|
| `analysis-server` | Primary analysis host | Ubuntu 24.04 + REMnux | Runs malware pipeline, MISP, Claude Code |
| `kb-server` | Knowledge base / Obsidian sync | macOS | Obsidian vault, git remote |
| `kali-worker` | OSINT, web crawling, influence ops | Kali Linux | Remote work host |

---

## SSH Key Management

| Key | Type | Public key hash | Used for | Created |
|-----|------|----------------|----------|---------|
| `~/.ssh/id_ed25519` | ed25519 | (record hash here) | All hosts | — |

**Backup:** Private key encrypted with GPG and stored externally. See `70-credentials/README.md` for procedure.

**Public key for reference** (safe to store here):

```
ssh-ed25519 AAAA... user@analysis-server
```

---

## Quick Reference

```bash
# Copy a file to a remote host
scp local-file.txt analysis-server:/home/user/destination/

# Sync a directory (vault → remote host)
rsync -av --progress local-dir/ analysis-server:/home/user/remote-dir/

# Reverse sync (remote → local)
rsync -av --progress analysis-server:/home/user/remote-dir/ local-dir/

# Port forward (e.g. MISP web UI on localhost:8080)
ssh -L 8080:localhost:443 analysis-server

# Background tunnel
ssh -fNL 8080:localhost:443 analysis-server
```
