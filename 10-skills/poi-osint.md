---
title: "POI OSINT — Person of Interest Investigation"
type: skill
tags: [osint, poi, sherlock, infrastructure, whois, misp]
llms: [claude-sonnet]
status: active
last_updated: 2026-03-27
source_playbook: /home/user/threat-research/playbooks/poi_osint.md
---

# POI OSINT — Person of Interest Investigation

## Purpose

Open-source intelligence investigation of individuals: journalists, lawyers, judges, executives, activists, court actors. Covers identity verification, platform enumeration, professional background, infrastructure pivoting, relationship mapping, and conflict-of-interest assessment.

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Primary — drives MCP scraper server, Sherlock via SSH |

## Pre-Investigation — Analyst Must Provide

```
1. Full name (legal, including titles)
2. Known aliases / usernames
3. Role in investigation (journalist / witness / suspect / court actor / etc.)
4. Known affiliations
5. Scope boundaries: what NOT to investigate (minor children, medical, etc.)
6. Output required: MISP attrs / JSON profile / report section / IOC list
7. Classification: TLP:WHITE / GREEN / AMBER / RED
```

## MCP Tool Hierarchy

| Priority | Tool | When |
|----------|------|------|
| 1st | `mcp__scraper__fetch_page(url)` | Default — articles, profiles, registries |
| 2nd | `mcp__scraper__fetch_page(url, render=true)` | JS-gated pages |
| 3rd | `mcp__scraper__fetch_raw(url)` | Raw HTML — metadata, JSON blobs |
| 4th | `mcp__scraper__crawl_site(url, max_pages, depth)` | Multi-page sites, news archives |
| last | SSH emergency fallback | Only when MCP unavailable |

## 10-Phase Process

| Phase | Goal | Key Tools |
|-------|------|-----------|
| 1 | Identity establishment — name, titles, aliases | Professional registries, official databases |
| 2 | Username enumeration (Sherlock) | `sherlock username` |
| 3 | Social media OSINT | Twitter/X, LinkedIn, relevant platforms |
| 4 | Professional background verification | Company registries, licensing bodies, academic |
| 5 | Domain / infrastructure pivoting | WHOIS, dig, theHarvester, CRT.sh, VT, ipinfo.io |
| 6 | Media footprint | Byline pages, crawl outlet archives, podcasts |
| 7 | Relationship mapping | Entity + edge JSON, cross-reference all POIs |
| 8 | Conflict of interest assessment | Statutory and ethical frameworks relevant to jurisdiction |
| 9 | MISP integration | Add structured attrs to active event via PyMISP |
| 10 | Profile output | `osint/POI-XX_[name].json` + markdown report section |

## Sherlock False Positive Reference

**Always FALSE POSITIVE** (HTTP 200 for any username): NationStates, Rarible, Slashdot, Smule, Splice, TryHackMe, Trovo, furaffinity, LessWrong, LibraryThing, GeeksforGeeks, Hashnode, Xbox Gamertag

**HIGH reliability:** GitHub, GitLab, Academia.edu, Bluesky (verify content)

**MEDIUM:** Flickr, Blogspot (many abandoned blogs contain unrelated content — always fetch and verify)

## WHOIS Anomaly Rule

If a domain's `changed` date falls within 7 days of investigation start → flag as possible awareness of OSINT activity.

## Conflict of Interest Scoring

| Level | Meaning |
|-------|---------|
| CRITICAL | Active legal ground for recusal/complaint |
| HIGH | Strong circumstantial conflict; disclosure should have been made |
| MEDIUM | Possible conflict; needs verification |
| LOW | Structural proximity; not actionable alone |

## Output Files

| File | Location |
|------|----------|
| POI profile JSON | `osint/POI-XX_[name].json` |
| Sherlock raw | `osint/POI-XX_sherlock.txt` |
| Relationship map | `network/relationship_map.json` |
| MISP attrs | Added to active event via PyMISP |

## Linked Workflows

- [[40-workflows/narrative-influence-investigation]]
- [[10-skills/influence-ops-media]]
- [[10-skills/narrative-threat-actor]]

## Notes

- Run both POI OSINT and influence_ops_media in parallel for court/media compound cases
- Address clustering: multiple companies at same address = network indicator
- PyMISP: `add_attribute` returns dict not MISPAttribute — verify success by re-fetching event
