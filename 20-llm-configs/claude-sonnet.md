---
title: "Claude Sonnet 4.6"
type: llm-config
id: cfg-claude-sonnet
volatility: volatile
sensitivity: public
provider: Anthropic
model_id: claude-sonnet-4-6
api_endpoint: https://api.anthropic.com/v1
strengths: [tool-use, long-context, code, analysis, MCP]
weaknesses: [cost-at-scale]
cost_tier: medium
context_window: 200000
status: active
last_updated: 2026-03-27
---

# Claude Sonnet 4.6

## Configuration

| Field | Value |
|-------|-------|
| Provider | Anthropic |
| Model ID | `claude-sonnet-4-6` |
| API Endpoint | `https://api.anthropic.com/v1` |
| Context Window | 200,000 tokens |
| Cost Tier | Medium |

## Strengths

- Excellent tool-use and MCP integration (drives REMnux, filesystem MCPs directly)
- Strong code generation and analysis
- Long context — can hold full malware analysis sessions
- Best-in-class structured output (JSON, YAML)

## Weaknesses

- Cost adds up at scale for bulk processing

## Skills Using This LLM

<!-- LLM: Obsidian Dataview block below — not rendered in CLI/MCP. To find skills using this LLM: grep -rl "claude-sonnet" 10-skills/ | grep -v _template -->
```dataview
TABLE title, tags, status
FROM "10-skills"
WHERE contains(llms, "claude-sonnet")
```

## Notes

- Used as primary driver in Claude Code (CLI)
- MCP tools available: remnux, filesystem, fetch
- Default model for this workspace
- API key: `$ANTHROPIC_API_KEY` — see `70-credentials/api-keys-inventory.md`
