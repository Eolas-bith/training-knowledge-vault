---
title: "Model Map — Which Model to Use"
type: index
id: mmap-readme
tags: [model-map, routing, local-llm, ollama, model-selection]
volatility: volatile
sensitivity: public
status: active
last_updated: 2026-07-08
---

# 25 — Model Map

**Which model to run, and when.** This section is model *selection* guidance. It
is deliberately separate from `20-llm-configs/`, which holds *connection* details
(endpoints, keys, SDK config). The boundary:

| `20-llm-configs/` (how to connect) | `25-model-map/` (which to pick) — this section |
|------------------------------------|------------------------------------------------|
| Endpoint URLs, API keys, SDK setup | Task → model routing |
| Per-provider config facts | Capability comparisons, hardware fit |
| One file per provider | Recommendations by task and by machine |

New provider setup lives in `20-llm-configs/`; put its shortlist and routing here.

---

## Files

| File | What it covers |
|------|----------------|
| `ollama-models.md` | Local model catalogue (Ollama) by hardware tier, roles, and API quirks |

Cloud models (Claude, GPT-4o) are configured in `20-llm-configs/`; their
selection guidance is folded into the routing table below rather than given their
own file in this training vault.

---

## Local or cloud? — pick the smallest thing that does the job

| Situation | Prefer |
|-----------|--------|
| Sensitive / private data that must not leave the machine | **Local** (Ollama) |
| Offline, air-gapped, or no API budget | **Local** |
| Bulk/repetitive calls where per-token cost would add up | **Local** (if quality holds) |
| Learning, prototyping, drafting | **Local** — free and fast enough |
| Hardest reasoning, long context, heavy tool-use / MCP | **Cloud frontier** (Claude) |
| Multimodal or broad world-knowledge one-offs | **Cloud** (Claude / GPT-4o) |
| You need a result you can *stake a report on* | **Cloud frontier**, or local + human verify |

A useful default: **draft and iterate locally, escalate the final or the hardest
step to a frontier model.** Local models are capable but bounded by your hardware
— treat their output as a strong first pass, not ground truth.

---

## Task → model routing (starting point)

Generic guidance — tune it to what you actually have installed. Local tags assume
Ollama; see `ollama-models.md` for hardware requirements.

| Task | Good local choice | Cloud escalation |
|------|-------------------|------------------|
| Summarise / draft / rewrite | `llama3.1:8b` | Claude Sonnet |
| Code / scripts / YARA rules | `qwen2.5-coder:7b` | Claude Sonnet |
| Structured extraction (JSON/NER) | `nuextract` (template API!) or `qwen2.5:14b` | Claude Sonnet |
| Embeddings / semantic search | `nomic-embed-text` | (usually stays local) |
| Fast lookups / classification | `llama3.2:3b` | GPT-4o |
| Long-context analysis, tool-use, MCP | — (hardware-bound) | **Claude Sonnet** |
| Final report you will publish | local draft → verify | **Claude Sonnet** |

---

## See also

- `20-llm-configs/ollama-local.md` — how to connect to a local model
- `20-llm-configs/claude-sonnet.md`, `20-llm-configs/gpt-4o.md` — cloud configs
- `97-scripts/setup-ollama.py` — one-command local setup for beginners
