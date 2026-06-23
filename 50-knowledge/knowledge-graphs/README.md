---
title: "Knowledge Graphs — Reference Section"
type: reference
id: kb-knowledge-graphs
volatility: stable
sensitivity: public
tags: [knowledge-graph, NLP, ontology, LLM, entity-extraction, CTI, graph-analysis]
status: active
llms: [claude-sonnet, claude-opus]
last_updated: 2026-06-11
---

# Knowledge Graphs

## What this section is

This is the reference library for knowledge graph theory, methodology, and practice — built from the ground up for CTI and intelligence analysis work. It covers the conceptual foundations you need to understand *why* knowledge graphs are useful, the standards and ontologies you need to build interoperable ones, the patterns for connecting them to LLMs, and a complete worked pipeline with code.

Everything here emerged from building real extraction pipelines on intelligence data. The theory is not included for its own sake — it is here because you will hit the same design questions every practitioner hits (what model to use, when to merge entities, how to handle ambiguous relations), and having the vocabulary and the literature makes those decisions faster and more defensible.

---

## What a knowledge graph actually is

At its simplest: a directed graph where the edges are named. Instead of "node A connects to node B", you get "Lazarus Group **deploys** Cobalt Strike" or "CVE-2021-44228 **affects** Apache Log4j". The edge label — the verb — is what makes it a *knowledge* graph rather than just a network.

This matters because:
- You can query by relation type, not just by proximity
- You can reason over the graph ("what malware families are used by actors that target financial institutions?")
- You can merge graphs from different sources using shared entity identifiers
- You can attach provenance (source, confidence, date) to individual facts

The alternative most people reach for first is a co-occurrence matrix or a social graph — those tell you *that* two things are related, but not *how*. A knowledge graph preserves the how, which is where the analytical value lives.

---

## How this section is organised

**[01-foundations.md](01-foundations.md)** — Start here if you are new to the field or need to brush up on the formal underpinnings. Covers the two main graph models (RDF triples and property graphs), how KGs relate to other data representations (relational databases, vector stores), entity resolution, type hierarchies, reification for provenance, and graph centrality metrics. Also a reference table of major public KGs.

**[02-ontologies.md](02-ontologies.md)** — How to define the vocabulary and rules of your KG. Covers the standards stack (RDF, RDFS, OWL 2, SKOS) and the CTI-specific ontologies you will actually encounter: STIX 2.1 (the de facto sharing standard), UCO/CASE (forensics), and MISP taxonomies and galaxies. Includes a mapping table from locally-extracted entity types to their STIX equivalents, and design principles for building ontologies that stay maintainable.

**[03-llm-integration.md](03-llm-integration.md)** — The intersection of KGs and large language models. Six concrete patterns: GraphRAG (Microsoft's approach to RAG over large corpora using community-detected summaries), KG-augmented retrieval, LLM-assisted triple extraction, Text-to-Cypher question answering, KG as persistent agent memory, and ontology-grounded generation to reduce hallucination. Each pattern includes a worked example and an honest account of where it fails.

**[04-extraction-pipeline.md](04-extraction-pipeline.md)** — The full pipeline for extracting a typed KG from unstructured text, with annotated code. Covers text cleaning, structured entity extraction (regex for CVEs, IPs, hashes, techniques, numbered APTs), spaCy NER with a CTI-tuned noise filter, SVO triple extraction via dependency parsing, VADER sentiment scoring, entity normalisation, and graph construction.

---

## When to reach for a knowledge graph

A KG is the right tool when you need to answer questions of the form *who did what to whom*, preserve provenance on individual facts, or reason across multiple connected entities. It is not always the right tool — here is a honest comparison:

| You need to... | Reach for... |
|----------------|-------------|
| Trace a specific actor's tool usage over time | KG with typed edges and timestamps |
| Find documents similar to a known report | Vector store + embedding similarity |
| Count how often two entities appear together | Co-occurrence matrix |
| Query a well-defined schema with known fields | Relational database |
| Summarise a large corpus of threat reports | GraphRAG |
| Track competing hypotheses with confidence | ACH matrix or Bayesian network |
| Map who talks to whom in a community | Social network / sociomapping |

---

## Outputs and what to do with them

The extraction pipeline produces four files:

**`knowledge_graph.gexf`** — Load into Gephi. Use the "Force Atlas 2" layout with edge weight as the scaling factor. Node colour by type (ACTOR, MALWARE, CVE, IP etc.), node size by mention count or PageRank. The community detection in Gephi (Statistics → Modularity) will surface clusters that correspond to distinct campaigns or actor groups.

**`entities.csv`** — The node table. Sort and filter to find all entities of type ACTOR with negative sentiment, or all CVEs seen in more than two channels.

**`relations.csv`** — The edge table with verb labels. Filter to `edge_type == typed` to see only verb-labelled relations; filter to `edge_type == cooccurrence` to see weaker co-occurrence links.

**`triples.csv`** — All raw SVO triples extracted by the dependency parser, including those that were not anchored to known entities. This is the audit trail and the seed data for extending entity coverage.

---

## Key decisions when building your own KG

**Entity resolution is the hardest part.** "APT29", "Cozy Bear", "Midnight Blizzard", and "NOBELIUM" are the same actor. Your pipeline will produce four separate nodes unless you handle this. Maintain a canonical form + aliases dictionary, and run normalisation after extraction.

**Typed edges need a controlled vocabulary.** If you allow any verb as a relation label you end up with hundreds of edge types that cannot be queried consistently. Lemmatise verb labels (spaCy does this), and consider mapping common verbs to a canonical set post-extraction.

**Sentiment is a signal, not ground truth.** A threat actor with positive sentiment has probably been mentioned in a "successfully attributed" or "detected and mitigated" context, not because the analyst approves of them. Use sentiment as a triage signal, not a classification label.

**Co-occurrence is not implication.** A co-occurrence edge between a CVE and an actor means they appeared in the same message or thread, not that the actor exploits that CVE. Typed edges from SVO extraction carry actual relational claims. When interpreting the graph, distinguish the two.

---

## Dependencies for the pipeline

```
spaCy           en_core_web_sm    NER + dependency parsing
vaderSentiment  —                 Message-level sentiment scoring
networkx        —                 Graph construction + metric computation
pandas          —                 CSV export
```

All four are standard Python packages available via pip. The `en_core_web_sm` spaCy model is small (12 MB) and adequate for the entity types that matter in CTI — the structured extractors (regex, keyword lists) handle the most important IOC types and are unaffected by model choice.

Canonical script: `97-scripts/slack-intel/kg_triples.py`
