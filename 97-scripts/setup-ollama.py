#!/usr/bin/env python3
"""
setup-ollama — beginner bootstrap for running this vault with a LOCAL model.

Goal: take someone from "I have this vault and a laptop" to "a local LLM is
running and I know how to point the vault at it" — on Linux, macOS, or Windows,
with no prior Ollama knowledge and no Python packages to install.

It does five things, each independently and each safe to re-run:
  1. detect     OS, CPU arch, and total RAM (RAM decides which models fit)
  2. install    Ollama if it is missing (guided — asks first, never silent)
  3. serve      make sure the Ollama server is reachable at localhost:11434
  4. pull       download a RAM-appropriate beginner model set
  5. test       run one real generation to prove the whole chain works
Then it prints exactly how to connect the vault (AGENTS.md as the system prompt).

Typical first run (does everything, asking before each change):
    python3 97-scripts/setup-ollama.py --all

Just look, change nothing (a "doctor" report + recommendation):
    python3 97-scripts/setup-ollama.py

Non-interactive (answer yes to every prompt — for scripts/CI):
    python3 97-scripts/setup-ollama.py --all --yes

Pure standard library — no pip install, matching vault-doctor.py. This script
never handles a credential: local models need no API key.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

DEFAULT_ENDPOINT = "http://localhost:11434"

# Beginner model sets by RAM tier. Everything here is pullable with `ollama pull`
# and small enough to run at Q4 quantisation on the RAM shown. Kept deliberately
# short — a beginner wants "one general + one code + embeddings", not 40 choices.
# See 25-model-map/ollama-models.md for the full catalogue and reasoning.
MODEL_TIERS = [
    # (min_ram_gb, label, [models])
    (0,  "minimal (<8 GB RAM — small, still useful)",
        ["llama3.2:3b", "nomic-embed-text"]),
    (8,  "standard (8-16 GB RAM — the recommended starting point)",
        ["llama3.1:8b", "qwen2.5-coder:7b", "nomic-embed-text"]),
    (16, "comfortable (16-32 GB RAM)",
        ["qwen2.5:14b", "qwen2.5-coder:7b", "nomic-embed-text"]),
    (32, "roomy (32 GB+ RAM)",
        ["qwen2.5:32b", "qwen2.5-coder:14b", "nomic-embed-text"]),
]

# ---------------------------------------------------------------------------
# small output helpers (no colour — works in every terminal, including Windows)
# ---------------------------------------------------------------------------
def say(msg):   print(msg)
def step(msg):  print(f"\n==> {msg}")
def ok(msg):    print(f"    [ok]   {msg}")
def warn(msg):  print(f"    [warn] {msg}")
def fail(msg):  print(f"    [FAIL] {msg}")

def confirm(question, assume_yes):
    if assume_yes:
        say(f"    {question} [auto-yes]")
        return True
    try:
        ans = input(f"    {question} [y/N] ").strip().lower()
    except EOFError:
        return False
    return ans in ("y", "yes")

# ---------------------------------------------------------------------------
# 1. detect
# ---------------------------------------------------------------------------
def detect_os():
    s = platform.system().lower()
    if s.startswith("linux"):
        return "linux"
    if s.startswith("darwin"):
        return "macos"
    if s.startswith("windows"):
        return "windows"
    return s or "unknown"

def detect_ram_gb():
    """Total physical RAM in GB, or None if it cannot be determined. Stdlib only."""
    system = detect_os()
    try:
        if system == "linux":
            with open("/proc/meminfo", encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return round(kb / 1024 / 1024, 1)
        elif system == "macos":
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()
            return round(int(out) / (1024 ** 3), 1)
        elif system == "windows":
            import ctypes  # stdlib

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return round(stat.ullTotalPhys / (1024 ** 3), 1)
    except Exception:
        return None
    return None

def recommend_tier(ram_gb):
    """Pick the richest tier whose RAM floor we meet. Unknown RAM -> 'standard'."""
    if ram_gb is None:
        return MODEL_TIERS[1]           # standard: the safe default
    chosen = MODEL_TIERS[0]
    for tier in MODEL_TIERS:
        if ram_gb >= tier[0]:
            chosen = tier
    return chosen

# ---------------------------------------------------------------------------
# 2. install
# ---------------------------------------------------------------------------
def ollama_path():
    return shutil.which("ollama")

def install_ollama(system, assume_yes):
    """Install Ollama for the detected OS. Guided: we always ask before changing
    the machine, and on macOS/Windows we prefer the user's package manager."""
    step("Ollama is not installed. Setting it up.")
    if system == "linux":
        cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        say("    Official Linux installer (may prompt for sudo):")
        say(f"        {cmd}")
        if not confirm("Run it now?", assume_yes):
            warn("Skipped. Install Ollama yourself, then re-run this script.")
            return False
        subprocess.run(cmd, shell=True, check=False)

    elif system == "macos":
        if shutil.which("brew"):
            say("    Homebrew found — installing via: brew install ollama")
            if not confirm("Run it now?", assume_yes):
                warn("Skipped. See https://ollama.com/download/mac")
                return False
            subprocess.run(["brew", "install", "ollama"], check=False)
        else:
            warn("Homebrew not found. Download the macOS app and run it once:")
            say("        https://ollama.com/download/mac")
            say("    Then re-run this script.")
            return False

    elif system == "windows":
        if shutil.which("winget"):
            say("    winget found — installing via: winget install Ollama.Ollama")
            if not confirm("Run it now?", assume_yes):
                warn("Skipped. See https://ollama.com/download/windows")
                return False
            subprocess.run(["winget", "install", "--id", "Ollama.Ollama", "-e"],
                           check=False)
        else:
            warn("winget not found. Download and run the Windows installer:")
            say("        https://ollama.com/download/windows")
            say("    Then re-run this script.")
            return False
    else:
        fail(f"Unsupported OS: {system}. See https://ollama.com/download")
        return False

    # shutil.which() caches nothing, but PATH may not include a just-installed
    # binary in this shell — report honestly rather than falsely succeed.
    if ollama_path():
        ok(f"Ollama installed: {ollama_path()}")
        return True
    warn("Installer ran, but 'ollama' is not on PATH in this shell yet.")
    warn("Open a new terminal (or add it to PATH), then re-run this script.")
    return False

# ---------------------------------------------------------------------------
# 3. serve
# ---------------------------------------------------------------------------
def server_up(endpoint):
    try:
        with urllib.request.urlopen(endpoint + "/api/tags", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False

def start_server(endpoint, assume_yes):
    if server_up(endpoint):
        ok(f"Ollama server already reachable at {endpoint}")
        return True
    if not ollama_path():
        return False
    step("Ollama server is not responding — starting it.")
    if not confirm("Start 'ollama serve' in the background?", assume_yes):
        warn("Skipped. Start it yourself with: ollama serve")
        return False
    # Detach so the server keeps running after this script exits.
    kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if os.name == "posix":
        kwargs["start_new_session"] = True
    else:
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    try:
        subprocess.Popen(["ollama", "serve"], **kwargs)
    except Exception as e:
        fail(f"Could not start server: {e}")
        return False
    for _ in range(20):                 # wait up to ~10s for it to come up
        if server_up(endpoint):
            ok(f"Server is up at {endpoint}")
            return True
        time.sleep(0.5)
    fail("Server did not come up in time. Try 'ollama serve' in its own terminal.")
    return False

# ---------------------------------------------------------------------------
# 4. pull
# ---------------------------------------------------------------------------
def installed_models(endpoint):
    try:
        with urllib.request.urlopen(endpoint + "/api/tags", timeout=5) as r:
            data = json.loads(r.read().decode())
        return {m["name"] for m in data.get("models", [])}
    except Exception:
        return set()

def pull_models(models, endpoint, assume_yes):
    have = installed_models(endpoint)
    todo = [m for m in models if m not in have and f"{m}:latest" not in have]
    if not todo:
        ok("All recommended models are already present.")
        return True
    step("Models to download: " + ", ".join(todo))
    say("    (This can be several GB and take a while on a slow connection.)")
    if not confirm("Download them now?", assume_yes):
        warn("Skipped. Pull later with: " + "  ".join(f"ollama pull {m}" for m in todo))
        return False
    all_ok = True
    for m in todo:
        say(f"    pulling {m} ...")
        rc = subprocess.run(["ollama", "pull", m]).returncode
        if rc == 0:
            ok(f"{m} ready")
        else:
            fail(f"pull failed for {m} (rc={rc})")
            all_ok = False
    return all_ok

# ---------------------------------------------------------------------------
# 5. test
# ---------------------------------------------------------------------------
def test_generate(model, endpoint):
    step(f"Testing a real generation with {model} ...")
    payload = json.dumps({
        "model": model,
        "prompt": "Reply with exactly the word: ready",
        "stream": False,
    }).encode()
    req = urllib.request.Request(endpoint + "/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode()).get("response", "").strip()
        ok(f"Model replied: {resp!r}")
        return True
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        fail(f"Generation failed: {e}")
    return False

# ---------------------------------------------------------------------------
# connection help
# ---------------------------------------------------------------------------
def print_connect_help(model, endpoint):
    step("How to use this vault with your local model")
    say(f"""
    The vault's instructions live in AGENTS.md (plain Markdown). A local runner
    has no auto-loaded context file, so you load it as the SYSTEM PROMPT.

    Quick sanity check from the terminal:
        ollama run {model}

    Native Ollama API ({endpoint}):
        POST {endpoint}/api/chat      (chat-style: system + user messages)
        POST {endpoint}/api/generate  (single-prompt; used by template models)

    OpenAI-compatible API (point Continue / Cline / opencode / any OpenAI SDK here):
        base_url: {endpoint}/v1
        api_key:  "ollama"          (any non-empty string; not checked locally)
        model:    "{model}"

    Minimal bootstrap prompt to give the model:
        "Read AGENTS.md in the vault root, then follow its navigation and rules
         before doing any task."

    More detail: 20-llm-configs/ollama-local.md  and  25-model-map/ollama-models.md
""")

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Beginner bootstrap for running the vault with a local model via Ollama.")
    ap.add_argument("--all", action="store_true",
                    help="do everything: install (if needed), serve, pull, test")
    ap.add_argument("--install", action="store_true", help="install Ollama if missing")
    ap.add_argument("--serve", action="store_true", help="start the Ollama server if down")
    ap.add_argument("--pull", action="store_true", help="download the recommended model set")
    ap.add_argument("--test", action="store_true", help="run one test generation")
    ap.add_argument("--models", default="",
                    help="comma-separated model tags to use instead of the RAM-based set")
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT,
                    help=f"Ollama endpoint (default {DEFAULT_ENDPOINT})")
    ap.add_argument("--yes", action="store_true", help="assume yes to every prompt")
    args = ap.parse_args()

    # No action flag -> "doctor" mode: report + recommend, change nothing.
    doctor_only = not any([args.all, args.install, args.serve, args.pull, args.test])
    do_install = args.all or args.install
    do_serve   = args.all or args.serve
    do_pull    = args.all or args.pull
    do_test    = args.all or args.test

    say("=" * 68)
    say(" setup-ollama — run this knowledge vault with a local model")
    say("=" * 68)

    # 1. detect
    step("Detecting your machine")
    system = detect_os()
    arch = platform.machine()
    ram = detect_ram_gb()
    ok(f"OS: {system}    CPU: {arch}    RAM: {ram if ram else '?'} GB")
    tier = recommend_tier(ram)
    models = ([m.strip() for m in args.models.split(",") if m.strip()]
              if args.models else tier[2])
    ok(f"Recommended tier: {tier[1]}")
    ok(f"Recommended models: {', '.join(models)}")
    have = ollama_path()
    (ok if have else warn)(f"Ollama: {'found at ' + have if have else 'not installed'}")

    if doctor_only:
        step("Report only — nothing was changed.")
        say("    To set everything up now, run:")
        say("        python3 97-scripts/setup-ollama.py --all")
        say("    (add --yes to skip the confirmation prompts)")
        return 0

    # 2. install
    if do_install and not ollama_path():
        if not install_ollama(system, args.yes):
            return 1
    elif do_install:
        ok("Ollama already installed — nothing to do.")

    if not ollama_path():
        fail("Ollama is not available; cannot continue. Re-run after installing.")
        return 1

    # 3. serve
    if do_serve and not start_server(args.endpoint, args.yes):
        return 1
    if (do_pull or do_test) and not server_up(args.endpoint):
        # pull can work without the HTTP server (CLI talks to it directly), but
        # test needs it. Try to bring it up.
        if not start_server(args.endpoint, args.yes):
            if do_test:
                fail("Server is down — cannot run the test.")
                return 1

    # 4. pull
    if do_pull and not pull_models(models, args.endpoint, args.yes):
        warn("Some models did not download; test may fail.")

    # 5. test
    if do_test:
        present = installed_models(args.endpoint)
        target = next((m for m in models
                       if m in present or f"{m}:latest" in present), None)
        if not target:
            warn("No recommended model is installed yet — skipping test. Run with --pull.")
        elif not test_generate(target, args.endpoint):
            return 1

    # connection help — always print on a real run
    chosen = next((m for m in models), models[0] if models else "llama3.1:8b")
    print_connect_help(chosen, args.endpoint)
    step("Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
