---
title: "Academic Writing Pipeline"
type: skill
tags: [writing, academic, latex, bibtex, pandoc, imrad, peer-review, agentic]
llms: [claude-sonnet, claude-opus]
status: active
last_updated: 2026-04-03
---

# Academic Writing Pipeline

## Purpose

Agentic pipeline for drafting, structuring, and compiling peer-reviewed academic papers, conference submissions, and journal articles. Covers the full workflow from raw research notes to a compiled, citation-complete PDF. Enforces citation fidelity — agents never invent references.

## Compatible LLMs

| LLM | Notes |
|-----|-------|
| claude-sonnet | Primary — file editing, outline generation, section drafting |
| claude-opus | Use for abstract, introduction, discussion, and final editorial review |

---

## Paper Structures Supported

| Type | Structure | Typical Venues |
|------|-----------|---------------|
| Empirical research paper | IMRaD (Intro, Methods, Results, Discussion) | IEEE S&P, USENIX, CCS, NDSS |
| Position / vision paper | Problem → Argument → Implications | Workshops, HotSec-style venues |
| Survey / SLR | Protocol → Taxonomy → Gaps | ACM CSUR, IEEE COMST |
| Extended abstract | Mini-IMRaD (500–1000 words) | Poster sessions, doctoral symposia |

---

## Required Inputs

- `input/notes.md` — research notes, findings, experimental results, key claims
- `input/figures/` — data plots, diagrams, screenshots (PNG/PDF)
- `input/refs.bib` — BibTeX library from Zotero or manual curation
- Target venue and its LaTeX template (e.g., `ieeeconf.cls`, `acmart.cls`, `llncs.cls`)
- Word / page limit

**Citation rule (non-negotiable):** Agents write `\cite{placeholder}` with a bracketed descriptor — e.g., `\cite{[CITE: lateral-movement-survey-2024]}`. A dedicated citation-resolution pass matches descriptors to real entries in `refs.bib`. Papers are never submitted with unresolved cite placeholders.

---

## Agent Architecture

```
Orchestrator
├── 1. Scope & Constraint Agent    — venue requirements, template, word limit, deadline
├── 2. Literature Synthesis Agent  — reads refs.bib + notes, builds related-work map
├── 3. Outline Agent               — produces section-by-section outline with word budgets
├── 4. Section Writer Agents (×N)
│   ├── abstract-writer            — last drafted, first read — do this after body
│   ├── introduction-writer        — motivation, gap, contributions, roadmap
│   ├── related-work-writer        — uses literature synthesis output
│   ├── methodology-writer
│   ├── results-writer             — data-driven, figures referenced
│   ├── discussion-writer          — interpretation, limitations, implications
│   └── conclusion-writer
├── 5. Citation Resolution Agent   — matches [CITE: descriptors] to refs.bib entries
├── 6. Figure & Caption Agent      — checks figure refs, writes captions, checks label consistency
├── 7. Coherence Reviewer          — global pass: argument thread, term consistency, flow
├── 8. Venue Compliance Agent      — checks length limits, required sections, formatting rules
└── 9. LaTeX Compiler              — pdflatex/bibtex compile loop, error recovery
```

---

## Tool Chain

| Phase | Tools / Commands |
|-------|-----------------|
| Reference management | Zotero → BibTeX export → `refs.bib` |
| LaTeX compilation | `pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex` |
| Word-count check | `texcount -inc -total paper.tex` |
| Grammar / style | `vale` with academic style guide, or `languagetool` |
| Diff for revisions | `latexdiff old.tex new.tex > diff.tex && pdflatex diff.tex` |
| Markdown → LaTeX fallback | `pandoc notes.md -o notes.tex` |
| Figure generation | Python matplotlib / R ggplot2 → PDF figures |

---

## Standard File Layout

```
./papers/{venue-year-slug}/
├── paper.tex                   # main LaTeX file
├── refs.bib                    # BibTeX library (Zotero export)
├── figures/                    # PDF/PNG figures
├── sections/                   # one .tex per section (input'd by paper.tex)
│   ├── abstract.tex
│   ├── intro.tex
│   ├── related.tex
│   ├── methodology.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── conclusion.tex
├── templates/                  # venue .cls/.sty files
├── drafts/                     # versioned intermediate drafts
│   └── outline.md
├── review/
│   ├── coherence-notes.md
│   └── compliance-check.md
└── output/
    ├── paper.pdf
    └── paper-diff.pdf          # revision diff vs previous version
```

---

## Prompt Template

**Invocation pattern:**

```
Read 85-writing/academic-writing.md, then draft a full [venue-format] paper from
input/notes.md. Target venue: [venue name]. Word limit: [N] words.
BibTeX library is at input/refs.bib. Use only references present in refs.bib.
Write [CITE: descriptor] for any reference not yet confirmed — do not invent citekeys.
```

---

## Writing Style Guidelines

- **Voice:** Third person, passive for methods (standard in most CS venues), active acceptable in intro/discussion.
- **Tense:** Present for facts/claims ("this paper shows"), past for your experimental actions ("we measured").
- **Contributions list:** Always explicit in introduction — numbered, concrete, falsifiable.
- **Limitations:** Must appear in discussion or a dedicated section. Reviewers penalise omission heavily.
- **Figures:** Every figure must be referenced in text before it appears. Caption must be self-contained.

---

## Reviewer Response Workflow

When revising after peer review:

1. Parse reviewer comments into `review/comments.md` with tags `[MAJOR]` / `[MINOR]` / `[NITPICK]`
2. Draft a response matrix: each comment → planned action → section modified
3. Use `latexdiff` to produce a marked-up PDF showing changes
4. Run the coherence reviewer on the full revised draft before resubmission

---

## Notes & Lessons Learned

- **Abstract last:** Draft the abstract after the body is stable. It should describe what you *did*, not what you *intend to do*.
- **Contribution inflation:** Agents tend to over-claim in the introduction. The coherence reviewer should specifically audit whether each stated contribution is actually demonstrated in the paper.
- **BibTeX hygiene:** Export from Zotero with BetterBibTeX for consistent cite keys. Standardise key format: `AuthorYYYY` or `AuthorYYYYword`. Fix accented characters before they reach LaTeX.
- **Venue-specific formatting:** Never assume a template is correct — download fresh from the venue CFP. Class files differ across years.
- **Rebuttal / revision:** `latexdiff` is invaluable. Always version your `.tex` files with git so diffs are reliable.
