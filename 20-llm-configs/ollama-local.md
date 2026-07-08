---
title: "Ollama — Local Models"
type: llm-config
id: cfg-ollama-local
volatility: volatile
sensitivity: public
provider: Ollama (local)
model_id: (varies — see 25-model-map/ollama-models.md)
api_endpoint: http://localhost:11434
strengths: [private, offline, free-to-run, no-API-key, full-control]
weaknesses: [bounded-by-your-hardware, weaker-than-frontier, no-managed-scaling]
cost_tier: free
context_window: varies by model (see catalogue)
llms: [ollama]
status: active
last_updated: 2026-07-08
---

# Ollama — Local Models

This is the **connection config** for running models on your own machine with
[Ollama](https://ollama.com). *Which* model to run and *when to prefer local over
a cloud API* live in the model map: `25-model-map/README.md` and
`25-model-map/ollama-models.md`. This file is only how you talk to the server.

> **New here?** Don't configure anything by hand. Run the bootstrap script — it
> installs Ollama, starts the server, downloads a model set sized to your RAM,
> tests it, and prints these connection details filled in for you:
> ```bash
> python3 97-scripts/setup-ollama.py --all
> ```

## Configuration

| Field | Value |
|-------|-------|
| Provider | Ollama (runs locally) |
| Endpoint | `http://localhost:11434` |
| API key | none — local models are not authenticated |
| Model ID | whatever you pulled (`ollama list` to see them) |
| Cost | free (you pay in RAM/VRAM and electricity) |
| Context window | per-model — see `25-model-map/ollama-models.md` |

## Two ways to call it

**1. Native Ollama API** — two endpoints, and the difference matters:

| Endpoint | Use for |
|----------|---------|
| `POST /api/chat` | normal chat models: send `system` + `user` messages |
| `POST /api/generate` | single-prompt calls, and **template models** (see gotcha below) |

**2. OpenAI-compatible API** — point any OpenAI SDK or agent frontend (Continue,
Cline, opencode, …) at Ollama by overriding the base URL:

```
base_url: http://localhost:11434/v1
api_key:  "ollama"        # any non-empty string; not checked locally
model:    "llama3.1:8b"   # a tag you have pulled
```

This is the easiest way to reuse tooling written for OpenAI against a local model.

## Connecting the vault

A local runner has **no auto-loaded context file** (unlike Claude Code's
`CLAUDE.md`). Load `AGENTS.md` as the **system prompt**, or point your frontend's
"rules"/"context" setting at it. Minimal bootstrap prompt:

> "Read AGENTS.md in the vault root, then follow its navigation and rules before
> doing any task."

See `AGENTS.md` → *Using this vault with any AI tool* for the per-tool table.

## Gotcha: template models are not chat models

Some task-specific models (extraction/NER fine-tunes such as `nuextract`) are
**not** instruction-following chat models. Call them via `/api/chat` and they
ignore your system prompt and answer in prose — your JSON parse then silently
returns nothing, with no error. These need `/api/generate` with their native
prompt template. The catalogue documents the full failure mode and the fix:
`25-model-map/ollama-models.md` → *Model API quirks*.

## Notes

- `ollama list` — what you have. `ollama pull <tag>` — get more. `ollama run <tag>` — chat in the terminal.
- The endpoint is local by default. To reach it from another machine you must set `OLLAMA_HOST=0.0.0.0` — only do that on a trusted network; it has no authentication.
- No credential belongs in `70-credentials/` for this provider — there is no key.
