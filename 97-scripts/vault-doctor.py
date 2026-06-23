#!/usr/bin/env python3
"""
vault-doctor — structural integrity checker for the knowledge vault.

The vault is strong on process discipline (how humans/agents should behave) but,
without this, has no *enforced invariants*. This script is that enforcement layer:
it guarantees structure regardless of behaviour. Run it locally, in a pre-commit
hook, and in CI.

Checks (ERROR = fails the run; WARN = advisory unless --strict):
  E  frontmatter present                (except the root instruction files: README.md,
                                          AGENTS.md, CLAUDE.md, GEMINI.md)
  E  required fields present            title, id, type, status, volatility, sensitivity
  E  enum conformance                   type / status / volatility / sensitivity
  E  id globally unique                 (templates exempt)
  E  nav parity                         every NN-section dir is routed in the canonical
                                          instructions file (AGENTS.md, else CLAUDE.md)
  E  backtick paths in canonical file resolve (placeholders skipped)
  E  internal links resolve             [[wikilinks]] and (markdown.md) links
  E  sensitivity segregation            a `public` file must not link to a `private` file
  E  public-repo leakage (--public-repo) internal/private file lacking `publish: true` clearance
  W  directory overload                 a section/dir holding too large a share of files
  W  missing last_updated

Usage:
  python3 97-scripts/vault-doctor.py [--root .] [--strict] [--json]
Exit code 0 = clean (no errors; under --strict, no warnings either), 1 = problems.

Pure standard library. The frontmatter parser handles the simple
`key: value` / `key: [a, b]` subset the vault uses — it is intentionally not a
full YAML parser.
"""
import argparse, json, os, re, sys

TYPES   = {"skill","prompt","llm-config","persona","workflow","reference",
           "session","index","section-index","session-index"}
STATUS  = {"active","draft","deprecated","in-progress","complete"}
VOL     = {"stable","periodic","volatile"}
SENS    = {"public","internal","private"}
EXEMPT  = {"README.md","CLAUDE.md","AGENTS.md","GEMINI.md"}  # root instruction files / docs about the vault, not items in it
REQUIRED = ["title","id","type","status","volatility","sensitivity"]

SECTION_RE = re.compile(r"^\d{2}-")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MDLINK_RE   = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
BACKTICK_RE = re.compile(r"`([^`]+)`")

def parse_frontmatter(text):
    """Return (dict, body_offset) or (None, 0) if no frontmatter block."""
    if not text.startswith("---\n"):
        return None, 0
    end = text.find("\n---", 4)
    if end < 0:
        return None, 0
    block = text[4:end]
    fm = {}
    for line in block.split("\n"):
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            v = v.strip('"\'')
        fm[k] = v
    return fm, end + 4

def is_template(path):
    return os.path.basename(path) == "_template.md"

def collect(root):
    files = []
    for dp, dns, fns in os.walk(root):
        if "/.git" in dp or os.sep+".git" in dp:
            continue
        for fn in fns:
            if fn.endswith(".md"):
                files.append(os.path.join(dp, fn))
    return sorted(files)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--overload-share", type=float, default=0.45,
                    help="warn if one top-level section exceeds this share of all files")
    ap.add_argument("--overload-count", type=int, default=20,
                    help="warn if any single directory holds more than this many files")
    ap.add_argument("--public-repo", action="store_true",
                    help="assert this repo is published: error on any internal/private file "
                         "that lacks `publish: true` clearance (drop this flag in a private fork)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    errors, warns = [], []
    def err(p, m): errors.append((os.path.relpath(p, root), m))
    def warn(p, m): warns.append((os.path.relpath(p, root) if p else "(vault)", m))

    files = collect(root)
    meta = {}          # path -> frontmatter dict
    ids = {}           # id -> path
    name_index = {}    # basename(no ext) -> [paths]

    # ---- pass 1: parse, per-file field checks, build indexes ----
    for p in files:
        rel = os.path.relpath(p, root)
        base = os.path.basename(p)
        name_index.setdefault(base[:-3], []).append(p)
        text = open(p, encoding="utf-8").read()
        fm, _ = parse_frontmatter(text)
        # public-repo leakage gate: a non-public file tracked in a published repo is a leak
        # unless explicitly cleared (`publish: true`) — i.e. a redacted/synthetic copy. This
        # runs before the EXEMPT skip so a private README is caught too.
        if args.public_repo and fm:
            sens = fm.get("sensitivity", "")
            cleared = str(fm.get("publish", "")).strip().lower() in ("true", "yes", "1")
            if sens in ("internal", "private") and not cleared:
                err(p, f"sensitivity '{sens}' file tracked in a public repo without "
                       f"`publish: true` clearance (--public-repo)")
        if base in EXEMPT:
            continue
        if fm is None:
            err(p, "missing frontmatter block")
            continue
        meta[p] = fm
        tmpl = is_template(p)
        for field in REQUIRED:
            if field not in fm:
                err(p, f"missing required field: {field}")
            elif fm[field] == "" and not tmpl:
                err(p, f"empty required field: {field}")
        # enum checks (skip empty template placeholders)
        def check_enum(field, allowed):
            v = fm.get(field, "")
            if v == "" and tmpl:
                return
            if v and v not in allowed:
                err(p, f"{field}: '{v}' not in {sorted(allowed)}")
        check_enum("type", TYPES)
        check_enum("status", STATUS)
        check_enum("volatility", VOL)
        check_enum("sensitivity", SENS)
        if "last_updated" not in fm and "date" not in fm:
            warn(p, "missing last_updated")
        # id uniqueness
        if not tmpl:
            i = fm.get("id", "")
            if i:
                if i in ids:
                    err(p, f"duplicate id '{i}' (also {os.path.relpath(ids[i], root)})")
                else:
                    ids[i] = p

    # ---- nav parity: every NN-section dir routed in the canonical instructions file ----
    # AGENTS.md is the tool-neutral canonical file; CLAUDE.md/GEMINI.md are thin adapters
    # that point back to it. Fall back to CLAUDE.md if AGENTS.md is absent.
    nav_name = "AGENTS.md" if os.path.exists(os.path.join(root, "AGENTS.md")) else "CLAUDE.md"
    nav = os.path.join(root, nav_name)
    nav_text = open(nav, encoding="utf-8").read() if os.path.exists(nav) else ""
    sections = sorted({d for d in os.listdir(root)
                       if os.path.isdir(os.path.join(root, d)) and SECTION_RE.match(d)})
    for s in sections:
        if s not in nav_text:
            err(nav, f"section '{s}/' is not referenced in {nav_name} (unrouted)")

    # ---- backtick paths in the canonical instructions file resolve ----
    for m in BACKTICK_RE.finditer(nav_text):
        tok = m.group(1).strip()
        if not SECTION_RE.match(tok):
            continue
        if "{" in tok or "YYYY" in tok or "MM" in tok or "DD" in tok or "*" in tok:
            continue  # placeholder/glob
        target = os.path.join(root, tok.rstrip("/"))
        if not os.path.exists(target):
            err(nav, f"backtick path does not resolve: `{tok}`")

    # ---- link resolution + segregation ----
    dirs = {os.path.relpath(os.path.join(dp, d), root).replace(os.sep, "/")
            for dp, dns, _ in os.walk(root) if "/.git" not in dp for d in dns
            if ".git" not in d}
    def resolve_wikilink(tok):
        tok = tok.replace("\\", "").split("|")[0].split("#")[0].strip()
        if not tok:
            return None
        if tok.endswith("/"):                      # folder reference
            return [tok] if tok.rstrip("/") in dirs else None
        name = tok.split("/")[-1]
        if name.endswith(".md"):
            name = name[:-3]
        return name_index.get(name)

    for p in meta:
        if is_template(p):
            continue                               # templates carry placeholder links
        text = open(p, encoding="utf-8").read()
        src_sens = meta[p].get("sensitivity", "")
        for m in WIKILINK_RE.finditer(text):
            tok = m.group(1)
            targets = resolve_wikilink(tok)
            if targets is None:
                err(p, f"broken wikilink: [[{tok}]]")
            elif src_sens == "public":
                for t in targets:
                    if meta.get(t, {}).get("sensitivity") == "private":
                        err(p, f"segregation: public file links to private [[{tok}]]")
        for m in MDLINK_RE.finditer(text):
            tgt = m.group(1).split("#")[0].strip()
            if not tgt.endswith(".md") or tgt.startswith(("http://","https://")):
                continue
            cand = os.path.normpath(os.path.join(os.path.dirname(p), tgt))
            if not os.path.exists(cand):
                err(p, f"broken link: ({tgt})")

    # ---- directory overload (junk-drawer detector) ----
    content_files = [p for p in files if os.path.basename(p) not in EXEMPT]
    total = len(content_files) or 1
    top_counts = {}
    dir_counts = {}
    for p in content_files:
        rel = os.path.relpath(p, root)
        top = rel.split(os.sep)[0]
        if SECTION_RE.match(top):
            top_counts[top] = top_counts.get(top, 0) + 1
        dir_counts[os.path.dirname(p)] = dir_counts.get(os.path.dirname(p), 0) + 1
    for s, c in sorted(top_counts.items()):
        if c / total > args.overload_share:
            warn(None, f"section '{s}/' holds {c}/{total} files "
                       f"({c/total:.0%} > {args.overload_share:.0%}) — candidate for splitting by volatility")
    for d, c in sorted(dir_counts.items()):
        if c > args.overload_count:
            warn(None, f"directory '{os.path.relpath(d, root)}' holds {c} files "
                       f"(> {args.overload_count}) — consider sub-structuring")

    # ---- report ----
    if args.json:
        print(json.dumps({"errors":[{"file":f,"msg":m} for f,m in errors],
                          "warnings":[{"file":f,"msg":m} for f,m in warns]}, indent=2))
    else:
        for f, m in errors: print(f"ERROR  {f}: {m}")
        for f, m in warns:  print(f"WARN   {f}: {m}")
        print(f"\nvault-doctor: {len(files)} files, {len(errors)} error(s), {len(warns)} warning(s)")
    fail = bool(errors) or (args.strict and bool(warns))
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
