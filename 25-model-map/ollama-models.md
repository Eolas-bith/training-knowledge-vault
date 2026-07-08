---
title: "Local Models — Ollama Catalogue"
type: reference
id: mmap-ollama-models
tags: [ollama, local-llm, models, hardware, model-selection]
volatility: volatile
sensitivity: public
llms: [ollama]
status: active
last_updated: 2026-07-08
---

# Local Models — Ollama Catalogue

A beginner-friendly shortlist of models to run locally with [Ollama](https://ollama.com),
organised by how much RAM you have. This is a *training* catalogue: a small, current,
opinionated set — not an exhaustive list. To connect to these, see
`20-llm-configs/ollama-local.md`. To install everything automatically, run
`97-scripts/setup-ollama.py --all`.

> **RAM is the constraint that matters.** The numbers below are for `Q4_K_M`
> quantisation (the Ollama default) — a good size/quality trade-off. A model needs
> roughly its "VRAM" figure in *free* memory to run smoothly; leave headroom for
> your OS. FP16 (unquantised) roughly doubles the requirement. If a model runs but
> is painfully slow, it is spilling to disk — drop to a smaller one.

---

## Pick by your hardware

### Minimal — under 8 GB RAM
| Role | Model | Tag | VRAM | Why |
|------|-------|-----|------|-----|
| General | Llama 3.2 3B | `llama3.2:3b` | ~2 GB | Fast, small, fine for summaries and drafting |
| Embeddings | Nomic Embed | `nomic-embed-text` | ~0.5 GB | Semantic search, Apache-2.0 |

### Standard — 8 to 16 GB RAM  *(recommended starting point)*
| Role | Model | Tag | VRAM | Why |
|------|-------|-----|------|-----|
| General | Llama 3.1 8B | `llama3.1:8b` | ~5 GB | Solid all-round reasoning and instruction-following |
| Code | Qwen 2.5 Coder 7B | `qwen2.5-coder:7b` | ~4 GB | Strong at scripts, YARA, completions |
| Embeddings | Nomic Embed | `nomic-embed-text` | ~0.5 GB | Semantic search |

### Comfortable — 16 to 32 GB RAM
| Role | Model | Tag | VRAM | Why |
|------|-------|-----|------|-----|
| General | Qwen 2.5 14B | `qwen2.5:14b` | ~9 GB | Noticeably stronger reasoning than 8B |
| Code | Qwen 2.5 Coder 7B | `qwen2.5-coder:7b` | ~4 GB | Keep the coder alongside |
| Embeddings | Nomic Embed | `nomic-embed-text` | ~0.5 GB | Semantic search |

### Roomy — 32 GB+ RAM
| Role | Model | Tag | VRAM | Why |
|------|-------|-----|------|-----|
| General | Qwen 2.5 32B | `qwen2.5:32b` | ~20 GB | Near-frontier local quality |
| Code | Qwen 2.5 Coder 14B | `qwen2.5-coder:14b` | ~9 GB | Better code reasoning |
| Embeddings | Nomic Embed | `nomic-embed-text` | ~0.5 GB | Semantic search |

Other useful pulls when you need them: `gemma3:4b` (lightweight, vision-capable),
`phi3:mini` (long context for its size), `mistral:latest` (quick lookups),
`nuextract` (structured extraction — see the quirk below).

**Everyday commands:**
```bash
ollama pull llama3.1:8b     # download a model
ollama list                 # what you have
ollama run llama3.1:8b      # chat in the terminal
ollama rm <tag>             # free the disk space
```

---

## Model API quirks

Behavioural differences that cause **silent** failures if you assume every Ollama
model uses the same calling convention.

### Template models (e.g. `nuextract`) — native template, not the chat API

**Symptom:** Your extraction pipeline runs to completion, logs look normal, but
every batch returns zero entities. No exception is thrown; `json.loads()` quietly
gets `{}`.

**Why:** `nuextract` and similar are structured-extraction *fine-tunes*, not
instruction-following chat models. Called via `/api/chat` (system + user
messages) they ignore the system prompt and answer in conversational prose, so the
JSON parse fails silently and every extracted field is dropped.

**Fix:** Call them via `/api/generate` with the model's native template, e.g.:
```
<|input|>
### Template:
{ JSON schema with empty / example values }
### Text:
{the text to extract from}
<|output|>
```
(Check the model's Ollama/HuggingFace card for its exact template — they differ.)

**General rule:** Before using `/api/chat`, ask whether a model is a task-specific
fine-tune. Signs: the name contains `extract`, `ner`, or `classifier`; its model
card shows training on fixed input templates rather than chat. Route those through
`/api/generate`; route normal chat models through `/api/chat`.

```python
def is_template_model(tag: str) -> bool:
    return any(x in tag.lower() for x in ("nuextract", "extract", "ner"))
```

---

## Notes

- **Quantisation** trades a little quality for a lot of memory. `Q4_K_M` is the
  sensible default; only reach for higher precision if you have RAM to spare and a
  measured reason.
- **Embeddings vs. generation** are different jobs — an embedding model
  (`nomic-embed-text`) turns text into vectors for search; it does not chat.
- **Fine-tuned "KB" variants** and multi-GPU server fleets are out of scope for
  this training vault — this catalogue is what one analyst can run on one laptop.
- See `25-model-map/README.md` for when to stay local vs. escalate to a cloud
  frontier model.
