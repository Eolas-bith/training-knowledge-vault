---
title: "LLM Configs — Overview"
type: index
id: cfg-llm-configs
volatility: volatile
sensitivity: public
section: 20-llm-configs
last_updated: 2026-05-21
status: active
---

# 20 — LLM Configs

Per-provider API configuration and integration notes. One file per provider.

**Scope:** API credentials structure, endpoint URLs, model IDs in use, cost tier, context window, SDK configuration, and integration notes.

**Not here:** Model capability comparisons, task-to-model routing, and model selection guidance. Those belong in a separate model-map section if you create one.

## Boundary with model selection

| This directory (`20-llm-configs/`) | Model selection guidance |
|------------------------------------|--------------------------|
| API endpoint URLs | Task → model routing matrix |
| Credentials structure and key location | Model capability comparisons |
| SDK configuration and auth method | Recommended models by task type |
| Cost tier and context window facts | Provider selection guidance |
| Integration notes (rate limits, quirks) | Routing policy |

When adding a new provider:
1. Create `20-llm-configs/{provider}.md` — config, credential location, SDK notes
2. Optionally create `25-model-map/{provider}.md` — capability shortlist and routing guidance

## Files

| File | Provider |
|------|---------|
| `claude-sonnet.md` | Anthropic Claude |
| `gpt-4o.md` | OpenAI GPT-4o |
| `_template.md` | Template for new providers |
