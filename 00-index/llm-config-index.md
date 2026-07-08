---
title: "LLM Configs — Index"
type: index
id: idx-llm-config-index
volatility: periodic
sensitivity: public
section: 20-llm-configs
last_updated: 2026-01-15
status: active
---

# 20 — LLM Configs

Per-provider API configuration and integration notes. One file per provider.

**Scope:** API credentials structure, endpoint URLs, model IDs in use, cost tier, context window, SDK configuration, and integration notes.

**Not here:** Model capability comparisons, task-to-model routing, and model selection guidance. Those live in `25-model-map/` (which model to pick, local vs. cloud, hardware fit).

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
| `ollama-local.md` | Ollama (local) | varies | Private/offline/free — drafting, bulk, learning; no API key |
| `_template.md` | — | — | Template for new providers |

> **Model selection** (which local or cloud model to pick per task, and when to stay local vs. escalate to a frontier model) lives in `25-model-map/`. Beginners: `97-scripts/setup-ollama.py --all` sets up a local model end-to-end.

---

## Files

| File | Provider |
|------|---------|
| `claude-sonnet.md` | Anthropic Claude |
| `gpt-4o.md` | OpenAI GPT-4o |
| `_template.md` | Template for new providers |
