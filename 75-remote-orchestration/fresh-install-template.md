---
title: "Fresh Install Template — Analysis Host"
type: reference
tags: [infrastructure, deployment, setup, remnux, analysis-server]
status: active
last_updated: 2026-01-15
---

# Fresh Install Template — Analysis Host

## Purpose

Step-by-step procedure for provisioning a new analysis host from scratch. Use this when:
- Rebuilding an existing host after a compromise or failure
- Deploying to a new VPS for a new engagement
- Setting up a second analysis host

Fill in `<placeholder>` values from `70-credentials/ssh-config.md` and `70-credentials/api-keys-inventory.md`.

---

## Prerequisites

- Ubuntu 24.04 LTS (minimal server install recommended)
- Root or sudo access
- Tailscale account with this host's auth key
- Git access to the vault repository

---

## Phase 1 — Base System

```bash
# Update base system
apt-get update && apt-get upgrade -y

# Install essentials
apt-get install -y git curl wget vim tmux htop \
    python3-pip python3-venv python3-paramiko \
    jq build-essential libssl-dev

# Create analyst user (if not already present)
useradd -m -s /bin/bash user
usermod -aG sudo user
# Set password or configure SSH key auth
```

---

## Phase 2 — SSH Key Setup

```bash
# On the new host, as the analyst user:
ssh-keygen -t ed25519 -C "user@analysis-server" -f ~/.ssh/id_ed25519

# Display the public key — add this to authorized_keys on other mesh hosts
cat ~/.ssh/id_ed25519.pub

# Add SSH config (see 70-credentials/ssh-config.md)
vim ~/.ssh/config
chmod 600 ~/.ssh/config
```

---

## Phase 3 — REMnux Installation

> **Note on Ubuntu 24.04:** REMnux requires DEB822 format sources. Run the pre-install step before the REMnux installer or three cascading salt failures occur.

```bash
# Pre-install: create DEB822 sources file
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

# Install REMnux
curl -o /tmp/remnux-cli https://REMnux.org/remnux-cli
mv /tmp/remnux-cli /usr/local/bin/remnux
chmod +x /usr/local/bin/remnux
remnux install 2>&1 | tee /var/log/remnux-install.log
```

---

## Phase 4 — Tailscale

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate (use a one-time auth key from Tailscale admin console)
tailscale up --authkey <tailscale-auth-key>

# Verify
tailscale ip -4
tailscale status
```

---

## Phase 5 — Python Environment

```bash
# Create project venv for malware pipeline
python3 -m venv /home/user/malware-llm-pipeline/.venv
source /home/user/malware-llm-pipeline/.venv/bin/activate

# Install dependencies (from requirements.txt in vault)
pip install anthropic requests yara-python pefile capstone vt-py paramiko

# Verify
python3 -c "import anthropic; print('anthropic OK')"
```

---

## Phase 6 — Environment Configuration

```bash
# Create .env file (never commit this file to git)
cat > /home/user/malware-llm-pipeline/.env << 'EOF'
ANTHROPIC_API_KEY=<from api-keys-inventory>
VT_API_KEY=<from api-keys-inventory>
OPENAI_API_KEY=<from api-keys-inventory>
GOOGLE_API_KEY=<from api-keys-inventory>
OPENROUTER_API_KEY=<from api-keys-inventory>
EOF
chmod 600 /home/user/malware-llm-pipeline/.env

# Verify .env is in .gitignore
echo ".env" >> /home/user/malware-llm-pipeline/.gitignore
```

---

## Phase 7 — Vault Clone

```bash
# Clone the vault
cd /home/user
git clone <vault-repo-url> eolas-vault

# Set git identity
git config --global user.name "analyst"
git config --global user.email "user@example.com"

# Verify
ls /home/user/eolas-vault/
```

---

## Phase 8 — Claude Code

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Configure
claude config set api-key <from .env>

# Verify
claude --version
```

---

## Phase 9 — Post-Install Fixes

```bash
# xrdp: add to ssl-cert group (required for TLS handshake)
# (run this if xrdp is installed)
usermod -aG ssl-cert xrdp
systemctl restart xrdp

# Verify malware pipeline
cd /home/user/malware-llm-pipeline
.venv/bin/python3 pipeline.py --help
```

---

## Verification Checklist

- [ ] REMnux tools installed: `which floss capa signsrch re-search.py xorsearch diec`
- [ ] Python venv active and anthropic importable
- [ ] `.env` file present and not tracked by git
- [ ] Tailscale connected and mesh hosts reachable
- [ ] Vault cloned and current
- [ ] Claude Code installed and configured
- [ ] SSH keys in place and mesh SSH working
- [ ] `/home/user/files/samples/` and `/home/user/files/output/` directories created
- [ ] Test run: `pipeline.py --no-vt /path/to/benign-elf` completes without errors

---

## Known Gotchas

| Issue | Root cause | Fix |
|-------|-----------|-----|
| REMnux fails on Ubuntu 24.04 | Legacy apt sources format | DEB822 pre-install step (Phase 3) |
| `pipeline.py` fails: `ModuleNotFoundError` | System Python used instead of venv | Always invoke as `.venv/bin/python3 pipeline.py` |
| xrdp TLS error | xrdp not in ssl-cert group | `usermod -aG ssl-cert xrdp && systemctl restart xrdp` |

For detailed pipeline-specific gotchas, see `97-scripts/README.md → Known Deployment Gotchas`.
