---
title: "Credentials — Strategy and Security Policy"
type: reference
id: cred-credentials
volatility: volatile
sensitivity: private
publish: true
tags: [credentials, security, backup, api-keys, ssh]
status: active
last_updated: 2026-01-15
---

# Credentials — Strategy and Security Policy

## What this folder is

An **inventory and reference** for all credentials, API keys, and SSH assets.

- **This vault is plaintext** — do NOT store raw private keys or full API key values here
- Store: masked values, file paths, purposes, rotation dates, and backup procedures
- Actual secrets live in their canonical locations (see each file)

## Tiers

| Tier | Examples | Storage here |
|------|----------|-------------|
| Low sensitivity | SSH config, public keys | Full plaintext copy |
| Medium | API key references, service URLs | Masked value + canonical path |
| High | Private keys, full API key values | Path only — encrypt externally |

## Encrypting secrets for backup (recommended)

```bash
# Encrypt a file with GPG symmetric cipher (AES256)
gpg --symmetric --cipher-algo AES256 ~/.ssh/id_ed25519

# Decrypt
gpg --decrypt id_ed25519.gpg > id_ed25519_restored

# Or encrypt all secrets in one archive
tar czf - ~/.ssh/id_ed25519 ~/config/api_keys.json | \
  gpg --symmetric --cipher-algo AES256 -o secrets_backup_$(date +%F).tar.gz.gpg
```

Store the `.gpg` file in a safe external location (USB, encrypted cloud, separate host).

## Rotation Policy

| Key Type | Rotation Frequency | Notes |
|----------|-------------------|-------|
| VT API key | Annually or on exposure | |
| DNSDB API key | Annually or on exposure | |
| MISP API key | Annually | |
| LLM API keys (Anthropic, OpenAI, etc.) | Annually or on exposure | Rotate immediately if exposed in git commit |
| SSH key pair | On compromise | Back up public key here; private key encrypted externally |

**On exposure:** Revoke the key at the provider console immediately. Do not wait. Generate a new key, update all canonical `.env` files, then update the masked entry here.

## Files in this folder

| File | Contents |
|------|----------|
| [[api-keys-inventory]] | All API keys — masked values + canonical paths |
| [[ssh-config]] | SSH configuration reference |
