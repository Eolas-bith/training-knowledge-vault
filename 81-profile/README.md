---
title: "Analyst Profile — Section Stub"
type: reference
id: profile-profile
volatility: periodic
sensitivity: private
publish: true
tags: [profile, persona, identity]
status: active
last_updated: 2026-01-15
---

# Analyst Profile

## What This Section Is

The `81-profile/` directory holds optional personal profile content for the vault owner — voice/style preferences, writing registers, communication patterns, and career notes.

This section is intentionally omitted from the training vault. Profile content is highly personal and only meaningful for the specific analyst who owns the vault. Adding generic placeholder profile content here would be misleading.

## How to Use This Section in Your Own Vault

If you want to configure Claude Code to write in your voice or adapt output to your style, populate this directory with:

- `00-profile-index.md` — linking to the files in this section
- `voice-style.md` — your writing register: vocabulary, sentence length, preferred analogies, what to avoid
- `communication-preferences.md` — how you prefer to receive information from the LLM (bullet lists vs prose, level of detail, etc.)

### Loading Rules for Profile Content

The vault's `CLAUDE.md` contains rules for when profile content is loaded:

- **Only load profile content when explicitly asked** — e.g., "write this in my voice", "use my style"
- **Never load during technical work** (malware analysis, CTI, OSINT, threat reporting) — loading biographical context during technical work degrades output quality by pulling the model toward an atmospheric register and away from precise technical language
- **Never load for public-facing work** without explicit analyst permission

These rules exist for analytical hygiene, not just preference. Treat them as methodology.

## Related

- AI persona contracts: [[22-personas/analyst-operator]]
- LLM configs: [[20-llm-configs/README]]
