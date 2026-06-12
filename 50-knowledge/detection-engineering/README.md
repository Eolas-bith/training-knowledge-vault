---
title: "Detection Engineering — Section Index"
type: reference
tags: [detection-engineering, SIEM, Suricata, YARA, ATT&CK, sigma]
status: active
last_updated: 2026-01-15
---

# Detection Engineering

## Purpose

Reference material for writing, tuning, and managing detection rules across SIEM, IDS/IPS, and endpoint platforms. Covers rule syntax, field path references, ATT&CK coverage mapping, suppression patterns, and quality metrics.

---

## Contents

| File | Description |
|------|-------------|
| `detection-rule-templates.md` | Templates for common detection rule types by input (process, network, auth, etc.) |
| `insightidr-query-language.md` | InsightIDR LEQL syntax reference |
| `field-reference.md` | Field paths by event type and vendor integration |
| `lolbins-process-patterns.md` | Windows LOLBin and process chain detection patterns |
| `linux-process-patterns.md` | Linux GTFOBins, reverse shell, container escape patterns |
| `windows-event-ids.md` | Windows Security Event ID reference (4624–5145, 7045) |
| `suricata-snort-syntax.md` | Suricata/Snort rule syntax — all protocol buffers, JA3 |
| `att-ck-coverage-map.md` | ATT&CK technique → rule coverage lookup |
| `data-sources-event-types.md` | Event type identifiers for vendor integrations |
| `rule-quality-metrics.md` | Rule quality metrics and tuning decision tree |
| `suppression-patterns.md` | Suppression pattern reference |

---

## Quick Reference

### Rule Writing Workflow

1. Identify the behavior (ATT&CK technique or observed TTP)
2. Select the appropriate input data source (process, network, auth, endpoint)
3. Choose the template from `detection-rule-templates.md`
4. Build the query using `field-reference.md` for your platform
5. Test against known-good and known-bad data
6. Apply quality metrics from `rule-quality-metrics.md`
7. Document the rule with: technique ID, logic, false positive risk, tuning notes

### Platform Coverage

| Platform | Rule Format | Syntax Reference |
|----------|-------------|-----------------|
| InsightIDR | LEQL (JSON) | `insightidr-query-language.md` |
| Suricata | Snort-derived | `suricata-snort-syntax.md` |
| Generic SIEM (Sigma) | YAML | [Sigma GitHub](https://github.com/SigmaHQ/sigma) |
| Endpoint (YARA) | YARA | `10-skills/yara-generation.md` |

---

## Detection Engineering Principles

**Start with behavior, not indicators.** IOC-based rules expire when infrastructure rotates. Behavioral rules targeting techniques (how malware acts) are more durable.

**Every rule needs a false-positive estimate.** Before deploying, estimate expected false positive rate in your environment. Rules without FP estimates cannot be tuned.

**Log ATT&CK coverage.** Track which techniques have coverage and which are blind spots. Gaps are as important as detections.

**Suppress precisely.** Over-broad suppressions create visibility gaps. Document every suppression with a scope condition and a review date.

**Test with adversary simulation.** Rules are only valid if tested against the behavior they claim to detect. Use atomic red team, caldera, or manual simulation.

---

## Linked Resources

- Detection skill: [[10-skills/detection-engineering]]
- IOC enrichment (for indicator-based rules): [[10-skills/threat-research-ioc]]
- ATT&CK mapping: [[50-knowledge/detection-engineering/att-ck-coverage-map]]
- MISP integration for IOC-based rules: [[10-skills/misp-ingestion]]
