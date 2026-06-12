---
title: "YARA Rule Generation"
type: skill
tags: [yara, detection, signature, malware]
llms: [claude-sonnet, gpt-4o]
status: active
last_updated: 2026-03-27
---

# YARA Rule Generation

## Purpose

Generate high-fidelity YARA rules from static analysis outputs. Produces family-level and variant-level rules.

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Primary |
| gpt-4o | Good for rule review / FP assessment |

## Required Context / Inputs

- Strings output (`static/{hash}/strings.txt`)
- Section analysis
- Import table
- Capa output

## Execution Prompt

**Variables:** `{STRINGS_FILE}`, `{SECTIONS}`, `{FAMILY}`, `{HASH8}`

```
Generate YARA rules from the following static analysis data:

Strings: {STRINGS_FILE}
Section analysis: {SECTIONS}
Family: {FAMILY}
Sample hash prefix: {HASH8}

Requirements:
1. family_{FAMILY}.yar — patterns present in ALL samples; minimum 3 conditions, 2+ byte patterns
2. variant_{HASH8}.yar — patterns unique to this variant
3. No generic patterns (MZ headers, common API names)
4. Each condition must have an inline comment explaining why it was chosen
5. Include ATT&CK technique references in metadata
6. Write string values as raw strings to avoid Unicode issues

Validate logic before outputting — every declared string must appear in condition.
```

**Expected output:** Two YARA rule files per sample set saved to `signatures/yara/`. Validate with `yara -r rule.yar samples/` before marking complete.

## Rule Standards

- `family_{name}.yar` — patterns common to ALL samples
- `variant_{hash8}.yar` — patterns specific to each variant
- Minimum 3 conditions, 2+ byte patterns
- Each condition must include an explanatory comment
- ATT&CK technique references in metadata

## Common Pitfalls

- Write rules as Python raw strings (`r'...'`) to avoid em-dash/Unicode corruption
- Every declared string (`$x`) MUST appear in the condition
- No generic patterns (MZ headers, common API names)
- Validate: `yara -r rule.yar samples/` before marking complete

## Linked Workflows

- [[40-workflows/new-sample-triage]]
