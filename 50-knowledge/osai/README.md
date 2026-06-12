---
title: "OSAI — AI Security Certification Prep"
type: reference
tags: [osai, ai-security, certification, study, exam-prep]
status: active
last_updated: 2026-01-15
---

# OSAI (AI-300) — Certification Prep

## What This Section Is

Study materials and structured notes for the OSAI (Offensive Security AI) AI-300 certification. The certification covers AI/ML security from both offensive and defensive perspectives — covering AI-specific attack surfaces, threat models for AI systems, and defensive controls.

This section supplements the course material with vault-linked threat intelligence and practical analysis notes.

---

## Section Map

| Sub-section | Contents |
|-------------|---------|
| `1a-ai-threat-landscape/` | AI-specific threat actors, campaigns, and emerging attack patterns |
| `study-guide.md` | Master study guide with topic coverage by domain |
| `schedule.md` | Study schedule and progress tracking |
| `book-mapping.md` | Mapping from certification domains to reference texts |

---

## AI Security Domain Overview

The certification covers these primary domains:

| Domain | Key Topics |
|--------|------------|
| AI threat landscape | AI-targeted attacks, adversarial ML, LLM-specific threats |
| LLM security | Prompt injection, jailbreaks, model inversion, membership inference |
| AI supply chain | Training data poisoning, model backdoors, dependency attacks |
| Defensive AI | Adversarial training, input validation, output filtering |
| Red teaming AI | LLM red teaming methodology, automated jailbreak testing |
| AI policy and governance | EU AI Act, NIST AI RMF, responsible disclosure for AI vulns |

---

## Vault Integration

This section links to threat intelligence content elsewhere in the vault:

- **AI-targeted threat actors** → `50-knowledge/threat-actors/` (filter tag: `ai-threat`)
- **LLM-integrated malware** → `50-knowledge/malware-families/` (filter tag: `llm-integrated`)
- **LLM inference attack methods** → `50-knowledge/llm-inference-access-methods.md`
- **Detection rules for AI abuse** → `50-knowledge/detection-engineering/`

---

## Notes on AI Threat Intel

Emerging threats involving AI systems are actively tracked in this vault. When working on AI-targeted investigations:

1. Check `50-knowledge/threat-actors/` for actors known to target AI infrastructure
2. Check `50-knowledge/malware-families/` for LLM-integrated or AI-abusing malware families
3. Apply structured analytical techniques from `10-skills/structured-analytical-techniques.md` — particularly ACH when evaluating competing hypotheses about AI-specific attack techniques

---

## Linked Resources

- Structured analytical techniques: [[10-skills/structured-analytical-techniques]]
- Threat actor profiles: [[50-knowledge/threat-actors/README]]
- Calibrated estimation: [[10-skills/calibrated-estimation]]
