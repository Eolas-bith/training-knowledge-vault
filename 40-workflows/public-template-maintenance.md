---
title: "Public Template Maintenance — Clean-Room Design Transfer"
type: workflow
id: wf-public-template-maintenance
volatility: periodic
sensitivity: public
tags: [vault, maintenance, publication, privacy, clean-room, validation]
llms: []
status: active
last_updated: 2026-09-20
---

# Public Template Maintenance — Clean-Room Design Transfer

## Purpose

Update a public knowledge-vault template from lessons learned in an operational or
private vault without publishing its content, metadata, infrastructure, history,
or identifying details. The output is a newly authored public design change, not a
sanitized copy of a private file.

## Prerequisites

- Explicit approval to change the public template
- A clean public-template working tree
- The public repository's `AGENTS.md` and `10-skills/vault-curation.md` read
- `vault-doctor.py` available
- `gitleaks` installed before enabling the repository hooks

## Inputs

| Input | Description |
|-------|-------------|
| Design observation | A short abstract statement of a reusable structural problem |
| Public invariant | The generic property the template should guarantee |
| Verification method | A deterministic check or review step proving the change |

Private files, diffs, logs, exported directory listings, and Git history are not
workflow inputs. Inspect them only in their authorized local context; do not place
them in the public worktree or send them to a public service.

## Phase 1 — Classify the candidate

**Goal:** Decide whether the lesson is design or data.

Allowed candidates:

- Folder taxonomy and routing patterns
- Generic frontmatter fields and templates
- Curation, review, rollback, and validation processes
- Trust-zone, write-scope, and publication controls
- Synthetic examples written from scratch

Excluded candidates:

- Real notes, sessions, cases, reports, prompts, or research results
- Names, handles, employers, clients, counterparties, or personal profile data
- Hosts, addresses, account state, costs, credentials, or service topology
- Private corpus sizes, measurements, performance figures, or capability claims
- Vendor-derived or licensed material that is not independently publishable
- Commit hashes, branches, messages, or history from the source repository

**Output:** A one-paragraph design requirement containing none of the excluded
material. If the requirement cannot be explained without source-specific detail,
reject it.

## Phase 2 — Write the clean-room specification

**Goal:** Replace the source observation with a public implementation contract.

Specify four things:

1. The generic failure mode
2. The invariant that prevents it
3. The public files or checks that implement the invariant
4. A synthetic test case

Do not preserve source phrasing merely because names were removed. Re-author the
explanation and examples from the public requirement.

## Phase 3 — Implement in the public repository

**Goal:** Make the smallest coherent public change.

Rules:

1. Edit only the public working tree.
2. Do not use cross-repository merge, cherry-pick, subtree, patch export, or file
   copy operations.
3. Keep one design concern per commit so it can be reverted independently.
4. Update the canonical schema, templates, navigation, documentation, and
   validator together when they describe the same invariant.
5. Prefer a validator check over prose when the rule is mechanically testable.

## Phase 4 — Validate structure and leakage

**Goal:** Prove both structural correctness and publication safety before push.

Run locally:

```bash
python3 97-scripts/vault-doctor.py --strict --public-repo
gitleaks git --pre-commit --staged --config .gitleaks.toml --redact .
```

Then inspect the complete staged diff. Look specifically for proper nouns, local
paths, hostnames, IP addresses, email addresses, identifiers, precise operational
counts, credentials, and copied prose. Automated secret scanning is necessary but
cannot recognize every form of private context.

## Phase 5 — Release and recover

**Goal:** Publish a reviewable, reversible design change.

- Use a commit message describing the public invariant, not its private origin.
- Let the pre-push hook and CI repeat the structural and secret checks.
- If a published change must be undone, use `git revert`; never rewrite shared
  history to hide it.
- Treat any discovered leak as already disclosed: revoke affected secrets and
  follow the hosting platform's history-removal procedure where appropriate.

## Quality gates

- [ ] The change can be understood without access to a private vault
- [ ] No private file, text block, example, path, or Git object was copied
- [ ] All examples are synthetic and use generic placeholders
- [ ] Schema, templates, navigation, and validation agree
- [ ] `vault-doctor.py --strict --public-repo` passes
- [ ] The staged gitleaks scan passes
- [ ] The complete staged diff received a human leak review
- [ ] The change is isolated enough to revert independently

## Linked references

- [[00-index/architecture]] — portable design and trust-zone contract
- [[10-skills/vault-curation]] — approval-gated methodology maintenance
- [[00-index/frontmatter-schema]] — classification and publication metadata
