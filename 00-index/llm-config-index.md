---
title: "LLM Configs — Index"
type: index
section: 20-llm-configs
last_updated: 2026-01-15
status: active
---

# 20 — LLM Configs

Per-provider API configuration and integration notes. One file per provider.

**Scope:** API credentials structure, endpoint URLs, model IDs in use, cost tier, context window, SDK configuration, and integration notes.

**Not here:** Model capability comparisons, task-to-model routing, and model selection guidance. Those live in `25-model-map/` (if present).

---

## Boundary with model selection

| This directory (`20-llm-configs/`) | Model selection guidance |
|------------------------------------|--------------------------|
| API endpoint URLs | Task → model routing |
| Credentials structure and key location | Model capability comparisons |
| SDK configuration and auth method | Recommended models by task type |
| Cost tier and context window facts | Provider selection guidance |
| Integration notes (rate limits, quirks) | Routing policy |

---

## Available Configs

| Config | Provider | Model | Use Case |
|--------|----------|-------|----------|
| `claude-sonnet.md` | Anthropic | claude-sonnet-4-6 | Primary — orchestration, long context, tool use, MCP |
| `gpt-4o.md` | OpenAI | gpt-4o | Secondary — fast inference, multimodal, rule review |
| `_template.md` | — | — | Template for new providers |

---

## Files

| File | Provider |
|------|---------|
| `claude-sonnet.md` | Anthropic Claude |
| `gpt-4o.md` | OpenAI GPT-4o |
| `_template.md` | Template for new providers |
