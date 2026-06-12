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

### Vault Methodology

- [[10-skills/vault-curation]] — four-phase lessons system: capture → aggregate → review → apply; skill files only touched in Phase 4 with explicit analyst approval
- [[10-skills/_template]] — template for adding a new skill

**Reference:**
- [[00-index/lessons-log]] — central lessons inbox; all open and applied lessons
- [[00-index/vault-curation-log]] — state tracker: last run, sessions processed, commit hashes
- [[30-prompts/vault-distillation-prompt]] — prompt that drives the Phase 2 aggregation run

---

### Analytical Techniques & Intelligence Structuring

- *(Add your SAT / ACH / structured analysis skill here — see `10-skills/_template.md`)*

**Reference knowledge:**
- [[50-knowledge/ontology-and-llm]] — why ontologies matter for LLM and AI work; entity types, relation schemas, STIX 2.1, MITRE ATT&CK, provenance

---

### Knowledge Graphs

- [[50-knowledge/knowledge-graphs/README|Knowledge Graphs]] — theory, ontologies, LLM integration, NLP extraction pipeline

---

### Threat Intelligence

- *(Add IOC enrichment, MISP ingestion, threat actor profiling skills here)*

**Reference knowledge:**
- [[50-knowledge/threat-actors/_template]] — threat actor profile template (identity, victimology, MO, ATT&CK, IOCs)
- [[50-knowledge/malware-families/_template]] — malware family profile template

---

### OSINT & Influence Operations

- *(Add POI OSINT, influence ops, forensic linguistics skills here)*

---

### Detection Engineering

- *(Add your SIEM rule writing, ATT&CK coverage mapping, suppression design skills here)*

---

### Writing & Reporting

- *(Add infosec report writing, academic writing, thesis writing skills here)*

---

### Script Library

- [[97-scripts/README]] — how scripts are structured, how they map to skills and workflows, deployment pattern

---

## How to Add a Skill

1. Copy `10-skills/_template.md` to `10-skills/your-skill-name.md`
2. Fill in the frontmatter (`title`, `tags`, `llms`, `status`, `last_updated`)
3. Write the **Purpose**, **Required Context / Inputs**, **Tool Chain** or **Procedure**, **Output Format**, and **Notes** sections
4. If the skill uses a script: add a `## Scripts` section with a table row linking to `97-scripts/`
5. If the skill uses a prompt: link to `30-prompts/`
6. Add an entry to this index under the appropriate domain
7. Commit skill file and index update together
