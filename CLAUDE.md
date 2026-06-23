# Training Knowledge Vault — Claude Code adapter

This vault keeps its instructions in **`AGENTS.md`** (the tool-neutral canonical file) so the same content works across Codex, Claude Code, Antigravity, Gemini CLI, and local models. The line below imports it inline at session start — do not duplicate vault rules here.

@AGENTS.md

---

## Claude Code-specific notes

- A global `~/.claude/CLAUDE.md` (if present) loads in addition to this file. Vault rules live in `AGENTS.md`; keep host/operator-wide preferences in the global file, not here.
- Edit `AGENTS.md` for any change to vault instructions, then run `97-scripts/vault-doctor.py`. This adapter should stay a thin pointer.
