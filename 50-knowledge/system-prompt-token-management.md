---
title: "System Prompt Token Management"
type: reference
tags: [system-prompt, token-optimisation, context-window, evals, llm-ops, vault-maintenance, claude-md]
status: active
last_updated: 2026-06-19
related: [[10-skills/vault-curation]] · [[20-llm-configs/README]]
---

# System Prompt Token Management

## The core problem

A system prompt is sent on **every exchange** in a session. It is not compressible at runtime — unlike conversation history, which can be summarised or truncated, the system prompt arrives in full at the start of every turn.

This makes it the single largest fixed per-turn cost in any LLM workflow. A 3,000-token system prompt on a 100-exchange session consumes 300,000 tokens before a single user message is counted. Every token you add to a system prompt is a permanent per-turn charge for the lifetime of every session that loads it.

**Consequence:** treat system prompt length as a first-class engineering metric, not an afterthought.

---

## How to measure token count

Tokens are not characters or words. Each LLM vendor uses a tokenizer that splits text into sub-word units — the count depends on the tokenizer and the content.

### Rule of thumb estimates

These are fast approximations, not precise counts. Use them for rough sizing.

| Method | Formula | Accuracy | When to use |
|--------|---------|----------|-------------|
| Characters ÷ 4 | `len(text) // 4` | Conservative floor — tends to undercount | Quick sanity check |
| Words × 1.35 | `len(text.split()) * 1.35` | Better for prose + markdown | Typical skill/prompt files |
| Words × 1.5 | `len(text.split()) * 1.5` | Better for code-heavy content | Files with many code blocks |

For a CLAUDE.md or skill file, **words × 1.35** gives a reasonable estimate. Markdown table syntax tokenizes higher than prose, code blocks lower.

### Precise count with tiktoken

`tiktoken` is OpenAI's tokenizer library. Claude uses a different tokenizer, but both derive from the BPE (Byte Pair Encoding) family and produce similar token counts for English prose. For sizing purposes, tiktoken is accurate enough.

```bash
pip install tiktoken
```

```python
import tiktoken

enc = tiktoken.get_encoding('cl100k_base')  # cl100k is used by GPT-4/ChatGPT — similar to Claude

def count_tokens(path):
    text = open(path).read()
    tokens = enc.encode(text)
    words = len(text.split())
    chars = len(text)
    lines = text.count('\n')
    print(f"{path}")
    print(f"  {chars:,} chars | {lines:,} lines | {words:,} words | {len(tokens):,} tokens")

count_tokens('CLAUDE.md')
count_tokens('10-skills/vault-curation.md')
```

### Example: real measurements from a CTI/OSINT vault (2026-06-19)

| File | Chars | Lines | Words | Est. tokens |
|------|-------|-------|-------|-------------|
| Global CLAUDE.md (`~/.claude/`) | 4,560 | 130 | 566 | ~764–1,140 |
| Project CLAUDE.md (`eolas-vault/`) | 12,085 | 142 | 1,490 | ~2,011–3,021 |
| Training vault CLAUDE.md | 6,045 | 96 | 846 | ~1,142–1,511 |

The wide range per file (764–1,140) reflects the difference between the two estimation methods. The true count falls somewhere in between; tiktoken gives a precise number.

**Observation from these numbers:**
- The global CLAUDE.md is small and efficient (~1K tokens)
- The project CLAUDE.md is large at ~2,000–3,000 tokens — every session loading both pays ~3,000–4,000 tokens before any work starts
- For a 200K-context model, this is 1.5–2% of total context consumed as fixed overhead — acceptable but worth monitoring as the vault grows

---

## What CLAUDE.md files are

Every CLAUDE.md in a project directory is automatically loaded as a system prompt by Claude Code when that directory is the working directory. The global `~/.claude/CLAUDE.md` is loaded in addition for every session.

**This means:**
- CLAUDE.md is not documentation — it is a system prompt
- Every line added to CLAUDE.md is a permanent per-session charge
- Skill files in `10-skills/` are only loaded when explicitly read — their length costs nothing at session start

The distinction matters: a 5,000-line skill file is fine. A 500-line CLAUDE.md is worth auditing.

---

## Per-model calibration

A system prompt written for one model is not automatically optimal for another.

| Factor | What changes between models |
|--------|-----------------------------|
| **Tokenization** | Different models tokenize differently. The same 3,000-character CLAUDE.md may cost 800 tokens on one model and 1,100 on another. |
| **Context window** | Claude Haiku 4.5, Sonnet 4.6, and Opus 4.8 all have 200K context (2026). Earlier or smaller models have less. A system prompt that uses 2% of a 200K window uses 4% of a 100K window. |
| **Prompt caching threshold** | Anthropic's prompt caching requires a minimum prefix of 1,024 tokens. A system prompt below this threshold gets no caching benefit. If you trim too aggressively on a long-session workflow, you may lose caching — and pay 10× more per turn. |
| **Instruction-following fidelity** | Smaller models need more explicit instructions. A terse, expert-audience system prompt that works reliably on Opus 4.8 may produce inconsistent behavior on Haiku 4.5, requiring expansion. Fewer tokens is not always better. |

**Rule:** when changing models, re-measure token count and re-validate behavior. Do not assume portability.

---

## Evals-driven optimization

Trimming a system prompt without validation risks silently breaking behavior. The model may start ignoring a rule, selecting the wrong tool, or producing incorrectly formatted output — and you won't know until it matters.

The correct workflow:

1. **Define behavioral tests before touching anything.** What decisions does the system prompt govern? Write representative input/output pairs. Example: "given [user asks to profile a threat actor], expect [model reads poi-osint.md skill file before proceeding]."

2. **Establish a baseline.** Run the test suite against the current system prompt. Record pass rate.

3. **Trim one category at a time.** Remove redundant instructions, dead links, or prose that belongs in skill files — one section per iteration.

4. **Re-run the eval suite.** Any regression → revert that trim. No regression → keep the cut and proceed to the next.

5. **Gate on evals.** Treat the eval suite as a deploy gate. No CLAUDE.md change ships without passing it.

### Eval frameworks

**OpenAI Evals** (`github.com/openai/evals`) — open-source framework for systematic LLM evaluation. Supports:
- Model-graded evals (LLM-as-judge)
- Exact-match and fuzzy-match classifiers
- Custom eval classes for task-specific scoring
- Multi-model comparison (useful for cross-model calibration)

It was built for OpenAI models but the eval patterns apply to any model — you call whatever API you want in your custom eval class.

**Anthropic batch API** — run the same input suite against Claude in batch mode, score outputs programmatically. No separate framework needed.

**Minimal viable eval for a vault CLAUDE.md:**
- 5–10 representative task prompts covering the main skill areas the vault supports
- Expected behaviors: which skill file should be read, what format should the output follow, what rules should be applied
- Run before and after any significant trim; compare pass rates

---

## Session lifecycle management

Context windows fill from two directions simultaneously:
- System prompt consumes from the start (fixed)
- Conversation history accumulates from the other end (growing)

When they meet, the model is forced to work in a compressed or truncated context — and behavior degrades silently. The model starts hedging, forgetting prior decisions, or ignoring instructions.

**Proactive session management prevents this.**

| Signal | Action |
|--------|--------|
| Task is complete or at a clean milestone | Close the session |
| Complex multi-step task approaching 50% context usage | Complete the current sub-task, close, open fresh session with a handoff summary |
| Compression has already occurred (you see summaries replacing prior turns) | Context is already degraded — critical content may have been lost; open a fresh session |
| Model behavior changes mid-session (hedging, forgetting decisions, ignoring rules) | Context pressure is likely — close and restart |

**Handoff prompt pattern:** when opening a fresh session after a context-full close, pass a compact state summary as the first user message (not embedded in the system prompt). Keep it under 500 tokens.

```
[State handoff — continuing from prior session]
Task: [what we're doing]
Completed: [what's already done]
Last artifact: [path/file]
Next step: [specific next action]
```

---

## CLAUDE.md maintenance checklist

Run this audit on any CLAUDE.md that has grown by 500+ tokens, or when switching to a new model version.

- [ ] Measure current token count (words × 1.35 estimate, or tiktoken for precision)
- [ ] Check for dead skill table entries (files that no longer exist or have been renamed)
- [ ] Check for duplicate rules (same instruction stated in two different places)
- [ ] Check for prose that belongs in the skill file, not the system prompt
- [ ] Check for sections that are never triggered in practice
- [ ] After trimming: re-run eval suite; verify pass rate equals or exceeds baseline
- [ ] Commit with: `chore(vault): trim CLAUDE.md — N tokens removed`

---

## Key references

- `10-skills/vault-curation.md` → `## CLAUDE.md Maintenance` — trim procedure and commit convention
- OpenAI Evals: `github.com/openai/evals` — eval framework for systematic LLM behavior validation
- Anthropic prompt caching: minimum 1,024-token prefix required; cache reads cost 10% of base input; 5-minute TTL
