---
title: "GPT-4o"
type: llm-config
provider: OpenAI
model_id: gpt-4o
api_endpoint: https://api.openai.com/v1
strengths: [fast, multimodal, broad-knowledge]
weaknesses: [no-MCP, weaker-tool-use-vs-claude, shorter-context]
cost_tier: medium
context_window: 128000
status: active
last_updated: 2026-03-27
---

# GPT-4o

## Configuration

| Field | Value |
|-------|-------|
| Provider | OpenAI |
| Model ID | `gpt-4o` |
| API Endpoint | `https://api.openai.com/v1` |
| Context Window | 128,000 tokens |
| Cost Tier | Medium |

## Strengths

- Fast inference
- Multimodal (image input useful for binary visualisations)
- Broad general knowledge for attribution / TTP lookup

## Weaknesses

- No native MCP support
- Weaker structured tool-use vs Claude for complex pipelines
- Shorter context window

## Skills Using This LLM

<!-- LLM: Obsidian Dataview block below — not rendered in CLI/MCP. To find skills using this LLM: grep -rl "gpt-4o" 10-skills/ | grep -v _template -->
```dataview
TABLE title, tags, status
FROM "10-skills"
WHERE contains(llms, "gpt-4o")
```

## Notes

- API key: `$OPENAI_API_KEY` — see `70-credentials/api-keys-inventory.md`
- Can be used via OpenRouter for cost optimisation: see OpenRouter config if available
