# Skills Index

<!-- LLM: Obsidian Dataview block below — not rendered in CLI/MCP contexts. The static index in ## By Domain is the LLM-readable version. -->
```dataview
TABLE llms, tags, status, last_updated
FROM "10-skills"
WHERE type = "skill"
SORT status ASC, title ASC
```

---

## By Domain

### Detection Engineering
- [[10-skills/detection-engineering]] — SIEM rule lifecycle: query language, suppression design, ATT&CK mapping, priority assignment, quality metrics

**Reference knowledge:**
- [[50-knowledge/detection-engineering/index|Detection Engineering Index]] — entry point and navigation
- [[50-knowledge/detection-engineering/detection-rule-templates|Detection Rule Templates]] — rule proposal guide: templates by input type (technique, process, cmd-line, Event ID, IP/domain/hash, registry, vendor alert, auth, cloud)
- [[50-knowledge/detection-engineering/insightidr-query-language|SIEM Query Language]] — JSON operator reference
- [[50-knowledge/detection-engineering/field-reference|Field Reference]] — field paths by event type and vendor integration
- [[50-knowledge/detection-engineering/lolbins-process-patterns|Windows LOLBins & Process Patterns]] — LOLBin abuse patterns, parent→child chains, suspicious paths, renamed binary detection
- [[50-knowledge/detection-engineering/linux-process-patterns|Linux Process Patterns]] — GTFOBins, web server process tree abuse, reverse shells, credential access, persistence, container escape
- [[50-knowledge/detection-engineering/windows-event-ids|Windows Event IDs]] — Security Event ID reference: 4624–5145, 7045, 1102
- [[50-knowledge/detection-engineering/suricata-snort-syntax|Suricata/Snort Syntax]] — complete rule syntax, all protocol buffers (HTTP/TLS/DNS/SMB/SSH/JA3), flowbits, threshold
- [[50-knowledge/detection-engineering/att-ck-coverage-map|ATT&CK Coverage Map]] — technique coverage with rule counts
- [[50-knowledge/detection-engineering/data-sources-event-types|Data Sources & Event Types]] — event type identifiers for integrations
- [[50-knowledge/detection-engineering/rule-quality-metrics|Rule Quality Metrics]] — matchRate, suppressionRate, falsePositives thresholds and tuning decision tree
- [[50-knowledge/detection-engineering/suppression-patterns|Suppression Patterns]] — suppression strategy patterns with annotated examples

**Script:** `97-scripts/detection-engineering/analyze-rules.py` — CLI tool to filter/search/export rules by technique, tactic, priority, event type, quality

---

### Malware Analysis
- [[10-skills/malware-analysis]] — ELF/Linux automated pipeline (REMnux, malcat, capa, floss)
- [[10-skills/windows-pe-reversing]] — Windows PE manual reversing (IDA, FLARE-VM, anti-analysis bypass)
- [[10-skills/yara-generation]]

**Reference knowledge:**
- [[50-knowledge/re-fundamentals]] — x86/x64 assembly, registers, calling conventions, debugging
- [[50-knowledge/windows-api-malware]] — Win32 API patterns: File/Registry/Process/Network/anti-analysis

### Threat Intelligence & IOC Enrichment
- [[50-knowledge/threat-actors/_template]] — threat actor profile template (identity, victimology, MO, ATT&CK, IOCs)
- [[10-skills/threat-intel]]
- [[10-skills/threat-research-ioc]]
- [[10-skills/misp-ingestion]]
- [[10-skills/cti-misp-pipeline]]
- [[10-skills/twitter-x-cti-pipeline]]
- [[10-skills/ta-attribution-map]] — probabilistic TA attribution from knowledge graph

**Reference knowledge:**
- [[50-knowledge/mitre-atlas/README|MITRE ATLAS]] — adversarial ML attack taxonomy for AI/ML systems

### Web Intelligence & Scraping
- [[10-skills/webcrawler-mcp]] — static + JS scraping, BFS crawl, offline snapshots, HAR, via MCP

### Dark Web OSINT
- [[50-knowledge/tools/robin-darkweb-osint]] — AI-powered dark web OSINT tool; Tor search across multiple .onion engines, LLM synthesis

### OSINT & Narrative / Influence Research
- [[10-skills/poi-osint]]
- [[10-skills/influence-ops-media]]
- [[10-skills/narrative-threat-actor]]
- [[10-skills/forensic-linguistics]] — authorship attribution, AI detection, stylometry
- [[50-knowledge/ai-detection-tools]] — AI-generated text detection methods, limitations
- [[10-skills/disarm-framework]] — DISARM Red/Blue; disinformation TTP taxonomy; counter-narrative mapping
- [[10-skills/narrative-framing-analysis]] — Entman framing theory, van Dijk CDA, BEND framework

### Knowledge Graphs
- [[50-knowledge/knowledge-graphs/README|Knowledge Graphs]] — theory, ontologies, LLM integration, NLP extraction pipeline
- [[50-knowledge/knowledge-graphs/01-foundations]] — graph types, formal definitions, KG vs other data models
- [[50-knowledge/knowledge-graphs/02-ontologies]] — RDF/OWL/SKOS standards; STIX 2.1, UCO, MISP ontologies
- [[50-knowledge/knowledge-graphs/03-llm-integration]] — GraphRAG, KG-augmented RAG, KGQA, LLM-assisted extraction
- [[50-knowledge/knowledge-graphs/04-extraction-pipeline]] — NER + SVO + sentiment pipeline with full code

**Script:** `97-scripts/slack-intel/kg_triples.py` — production implementation of the extraction pipeline

### Analytical Techniques & Intelligence Structuring
- [[10-skills/structured-analytical-techniques]] — SATs (ACH, KAC, Red Team), Diamond Model, Cyber Kill Chain, MITRE ATT&CK
- [[10-skills/premortem-analysis]] — prospective hindsight; failure-assumption technique
- [[10-skills/behavioral-criminal-profiling]] — FBI BAU methodology; MICE/RASCLS motivation analysis
- [[50-knowledge/behavioral-analysis/README|Behavioral Analysis Methods]] — 7 traditions: CIB, psycholinguistic, forensic behavioral, structured threat assessment, behavioral economics, psychographic profiling, social/group behavioral
- [[10-skills/humint-source-evaluation]] — NATO admiralty codes; source reliability and information credibility
- [[10-skills/indications-warning-analysis]] — I&W methodology; indications lists; warning watch levels
- [[10-skills/calibrated-estimation]] — Sherman Kent WEP; ODNI probability language; superforecasting techniques
- [[10-skills/social-network-analysis]] — manual/qualitative network mapping; centrality measures; influence op network analysis

### Threat Modeling
- [[10-skills/threat-modeling]] — STRIDE/STRIDE-LM, DREAD, PASTA, VAST, OCTAVE, LINDDUN

### Quantitative Risk & Governance
- [[10-skills/quantitative-risk-management]] — FAIR, Beta-PERT, Monte Carlo, FMEA, NIST RMF, ISO 27005

### Red Team / Phishing Operations
- [[10-skills/phishing-red-team]] — AiTM phishing with Evilginx + GoPhish

### AI Red Teaming
- [[50-knowledge/osai/README]] — OSAI cert prep: prompt injection, RAG corpus poisoning, embedding inversion, MCP exploitation, A2A protocol attacks, AI infra CVEs, supply chain, MITRE ATLAS, OWASP LLM Top 10

### Digital Privacy & Security
- [[80-privacy-security/skills/analyst-opsec]]
- [[80-privacy-security/skills/privacy-audit]]
- [[80-privacy-security/skills/threat-modeling-skill]]

### Digital Risk & Brand Protection

**Reference knowledge:**
- [[50-knowledge/takedown-remediation-matrix]] — platform-by-platform takedown matrix: supported scenarios, minimum evidence required, prerequisites; covers 35+ platforms

### Analyst Profile

- [[81-profile/README]] — what the profile section contains and when to load it

### Ethics & Applied Frameworks

- [[10-skills/ethical-analysis-frameworks]] — principalism, deontology, consequentialism, virtue ethics, Just War Theory, DURC

### Vault Maintenance

- [[10-skills/vault-curation]] — four-phase lessons system: capture → aggregate → review → apply
- [[00-index/lessons-log]] — central lessons inbox; all open and applied lessons
- [[00-index/vault-curation-log]] — state tracker: last run date, last session processed, commit hashes
- [[10-skills/vault-health]] — automated health check: broken wikilinks, missing frontmatter, orphaned entities

### Script Library

Canonical copies of orchestration scripts. Vault is source of truth; runtime hosts are deployments.

- [[97-scripts/README]] — index, vault-to-runtime mapping, deployment pattern

### Agentic Writing
- [[85-writing/infosec-report-writing]] — threat reports, advisories, security blogs
- [[85-writing/academic-writing]] — peer-reviewed papers, conference submissions, surveys

**Writing Prompts**
- [[30-prompts/infosec-report-orchestrator]] — trigger: threat report / advisory / blog
- [[30-prompts/vault-distillation-prompt]] — trigger: vault curation run
