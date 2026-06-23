---
title: "Ontology — Why It Matters for LLM and AI Work"
type: reference
id: kb-ontology-and-llm
volatility: stable
sensitivity: public
tags: [ontology, knowledge-representation, llm, knowledge-graph, rag, ai, reasoning]
status: active
last_updated: 2026-06-12
---

# Ontology — Why It Matters for LLM and AI Work

## What Is an Ontology?

An ontology is a formal, explicit specification of the concepts in a domain and the relationships between them. It answers three questions:

1. **What entities exist?** — The classes (e.g., `ThreatActor`, `Malware`, `Campaign`, `Victim`)
2. **How are they related?** — The properties (e.g., `uses`, `targets`, `attributed-to`, `delivers`)
3. **What constraints apply?** — The axioms (e.g., "a `Campaign` must have at least one `ThreatActor`")

An ontology is not a database schema and not a taxonomy. A taxonomy only organises things hierarchically (is-a). An ontology adds lateral relationships, constraints, and inference rules. The difference matters enormously when you use AI to reason over it.

---

## Why Ontologies Matter for LLM Work

### 1. LLMs Have No Memory of Relationships

A language model generates text by predicting the next token. It does not maintain a consistent internal model of which entities are related and how. When you ask an LLM "which threat actors use BPFDoor?", it answers from statistical associations in training data — not from a verified, grounded knowledge base. The answer can be plausible but wrong.

An ontology gives the LLM a grounded graph to query against. Retrieval-Augmented Generation (RAG) combined with a structured knowledge graph dramatically reduces hallucination on factual questions because the model is constrained to answer from verified triples.

### 2. Ontologies Enable Structured Extraction

When you ask an LLM to extract information from a document ("identify threat actors and their TTPs"), the output quality depends entirely on whether the LLM has a clear target schema. Without an ontology:

- The LLM invents its own entity types inconsistently across documents
- Merging extractions from 100 documents produces noise, not a graph
- Entity resolution is impossible ("APT28", "Fancy Bear", "Strontium" are the same actor — the LLM won't know unless the ontology tells it)

With an ontology:
- You define the allowed entity types and relation labels upfront
- Every extraction run produces triples that conform to the same schema
- Merging is possible: same entity type + same canonical name = merge candidate

**Practical rule:** Define your ontology before you run NLP extraction. Retrofitting an ontology to unstructured extractions is expensive and lossy.

### 3. Ontologies Make AI Reasoning Auditable

When an LLM answers "Actor X is likely behind Campaign Y because they share infrastructure Z", you need to verify that chain. If the evidence lives in an ontology-backed knowledge graph:

```
(CampaignY) --[uses]--> (InfrastructureZ)
(ActorX)    --[uses]--> (InfrastructureZ)
```

...then the reasoning is traceable. You can inspect the specific edges, check their sources, and challenge the inference. Without a graph, the "reasoning" is opaque token prediction that cannot be independently verified.

This matters most in threat intelligence, legal analysis, and any domain where conclusions have real-world consequences.

### 4. Ontologies Control What the LLM Knows It Doesn't Know

An LLM will confidently answer questions that fall outside its training data. An ontology-backed system can detect "no triples match this query" and respond "unknown — no evidence in the knowledge base" rather than hallucinating an answer. This closed-world assumption is essential for high-stakes analysis.

---

## Key Ontology Standards Relevant to This Vault

### STIX 2.1 (Structured Threat Information eXpression)

The de facto standard for CTI knowledge representation. Defines:
- **STIX Domain Objects (SDOs):** `threat-actor`, `malware`, `campaign`, `attack-pattern`, `indicator`, `course-of-action`, `identity`, `vulnerability`, `tool`, `report`, `intrusion-set`
- **STIX Relationship Objects (SROs):** `relationship` (generic, with `relationship_type` property), `sighting`
- **STIX Cyber Observables (SCOs):** `domain-name`, `ip-addr`, `file`, `url`, `email-addr`, `network-traffic`, `process`

STIX is the native schema of MISP. Any knowledge graph you build for CTI should be able to map to or from STIX.

### MISP Taxonomies

MISP taxonomies are controlled vocabularies (not full ontologies, but foundational). Key ones:
- `misp-galaxy` — malware families, threat actors, tools with aliases
- `tlp` — Traffic Light Protocol marking
- `admiralty-scale` — source reliability + information credibility (1A–6F)
- `kill-chain` — Lockheed Martin Cyber Kill Chain phases

Use taxonomies to normalise entity labels before building a graph. "APT28", "Fancy Bear", "Sofacy" should all resolve to the same `misp-galaxy:threat-actor="Fancy Bear"` tag.

### MITRE ATT&CK

ATT&CK is a knowledge base structured as a taxonomy of adversary techniques, but it is also an implicit ontology:
- **Tactics** → the "why" (14 categories: Reconnaissance → Impact)
- **Techniques** → the "what" (T1059, T1055…)
- **Sub-techniques** → the "how specifically"
- **Groups, Software, Campaigns** → the "who" and "with what"

When you extract TTPs from a threat report, map them to ATT&CK IDs. This lets you:
- Compare across actors and campaigns
- Measure detection coverage against a known reference frame
- Ask "which actors use this technique?" against a structured graph

### OWL / RDF (for custom ontologies)

If you build a domain-specific graph (e.g., for influence operations, forensic linguistics, or academic paper relationships), OWL (Web Ontology Language) over RDF triples is the standard. Key concepts:

| Concept | Meaning |
|---------|---------|
| `rdfs:Class` | An entity type |
| `rdfs:subClassOf` | Inheritance |
| `owl:ObjectProperty` | A relationship between two entities |
| `owl:DatatypeProperty` | A relationship between an entity and a literal value |
| `owl:equivalentClass` | Two classes mean the same thing (useful for cross-ontology alignment) |
| `owl:sameAs` | Two individuals are the same entity (entity resolution) |

For LLM pipelines, full OWL reasoning is usually overkill. Use a simplified JSON-LD or property graph representation (Neo4j, SQLite edges table) that captures the ontology's entity types and relation labels, and apply OWL concepts as design guidance rather than runtime constraints.

---

## Practical Design Principles

### Define Entity Types Before Extraction

```
Allowed entity types:
  ThreatActor, Malware, Campaign, Infrastructure,
  Vulnerability, Victim, Country, Sector, Tool, Report

Allowed relation types:
  uses, targets, attributed-to, delivers, exploits,
  operates-in, part-of, reported-in, sighted-at
```

Write this down. Give it to the LLM as a system prompt. Every extraction session must produce triples that fit this schema or flag "out of schema" for analyst review.

### Normalise Entity Labels Immediately

The most expensive graph operation is retroactive entity resolution. Build normalisation into the extraction pipeline:
- Strip whitespace and capitalise consistently
- Apply alias lists (e.g., load from `misp-galaxy`)
- Flag bare generic tokens (`APT`, `RAT`, `backdoor`) as disambiguation-required rather than treating them as entity instances

### Track Provenance on Every Triple

Every edge in your graph should carry:
- `source` — the document or session it came from
- `confidence` — DIRECTLY_OBSERVED | INFERRED | REPORTED
- `date` — when the triple was established
- `analyst` — who or what system created it

Without provenance, you cannot audit AI-generated graph expansions, and you cannot expire stale intelligence.

### Separate Schema from Instances

Your ontology (the schema — classes and properties) should live in a dedicated file or config, separate from the instance data (the actual nodes and edges). When you update the schema, you can re-validate all instances. When you add new entities, the schema does not change.

In this vault, `50-knowledge/knowledge-graphs/02-ontologies.md` documents the schema for the analyst's knowledge graphs.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| No schema before extraction | Inconsistent entity types, unmergeable extractions | Define schema first, give it to the LLM as a constraint |
| Generic tokens as entities | "APT" node with 10,000 edges to every actor | Disambiguation-required flag; never auto-merge generic tokens |
| Relation labels from free text | "was possibly linked to", "may have used" as edge labels | Enumerate allowed labels; LLM must choose from the list or return null |
| No provenance | Cannot audit reasoning, cannot expire stale intel | Provenance fields required on every triple |
| Merging by string match alone | "Cozy Bear" ≠ "CozyBear" (missed merge) or "Lemon" = "Lemon Duck" (wrong merge) | Alias normalisation + minimum string similarity threshold + analyst review for ambiguous cases |
| Ontology drift | Schema evolves informally; old triples become invalid | Version the schema; validate instances on schema change |

---

## Linked Resources

- `50-knowledge/knowledge-graphs/01-foundations.md` — graph types, formal definitions, quality dimensions
- `50-knowledge/knowledge-graphs/02-ontologies.md` — RDF/OWL/SKOS standards; STIX 2.1, UCO, MISP ontologies
- `50-knowledge/knowledge-graphs/03-llm-integration.md` — GraphRAG, KG-augmented RAG, KGQA, LLM-assisted extraction
- `50-knowledge/knowledge-graphs/04-extraction-pipeline.md` — NER + SVO pipeline; CTI corpus example
- `10-skills/vault-curation.md` — how the vault's own lesson distillation process applies ontology principles (entity types for observations, controlled vocabulary for lesson types)
