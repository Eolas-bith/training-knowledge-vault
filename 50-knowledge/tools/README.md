---
title: "Tools — Reference Section"
type: reference
tags: [tools, reference, infrastructure, platforms]
status: active
last_updated: 2026-01-15
---

# Tools

## Purpose

Reference documentation for specific tools and platforms used in analysis work that require more than a few lines of setup. Where a tool has enough operational nuance to deserve its own document, it lives here.

This section is for:
- Tools with non-obvious configuration (MCP servers, custom APIs)
- Platform-specific setup runbooks (MISP, REMnux, sandboxing)
- Tool integrations that cross multiple workflow steps

Do not put general methodology here — methodology belongs in `10-skills/`. Do not put short tool invocations here — those belong in the relevant skill file.

---

## Contents

| File | Tool / Platform | Description |
|------|-----------------|-------------|
| `misp-mcp-setup.md` | MISP + MCP | MISP platform setup, rebuild procedure, MCP integration |
| *(add entries here)* | | |

---

## When to Add a Tool File

Add a dedicated file when:
- The tool has enough configuration state that a new analyst could not set it up from the skill file alone
- The tool has operational quirks that recur (multiple flagged observations pointing here)
- The tool integrates with the vault pipeline in a non-obvious way (e.g. MCP server, API gateway)

Do not add a file for:
- Standard CLI tools with obvious usage (floss, capa, etc.) — those are documented in skill files
- Tools with a single invocation pattern — a note in the skill file is sufficient

---

## Linked Resources

- Malware analysis skill: [[10-skills/malware-analysis]]
- MISP ingestion skill: [[10-skills/misp-ingestion]]
- Remote orchestration: [[75-remote-orchestration/README]]
- Scripts library: [[97-scripts/README]]
