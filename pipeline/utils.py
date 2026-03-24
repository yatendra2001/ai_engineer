"""
Forge Pipeline — Core Utilities
Handles: API calls, file I/O, logging, JSON extraction, state checks
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import anthropic

from .config import MODEL, MAX_TOKENS, CONTENT_DIR


# ── Logging ───────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BLUE   = "\033[94m"


def log(msg: str, level: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    prefix = {
        "info":    f"{DIM}{timestamp}{RESET} {BLUE}→{RESET}",
        "success": f"{DIM}{timestamp}{RESET} {GREEN}✓{RESET}",
        "warn":    f"{DIM}{timestamp}{RESET} {YELLOW}⚠{RESET}",
        "error":   f"{DIM}{timestamp}{RESET} {RED}✗{RESET}",
        "step":    f"{DIM}{timestamp}{RESET} {CYAN}{BOLD}◆{RESET}",
        "dim":     f"{DIM}{timestamp}  ",
    }.get(level, "→")
    print(f"{prefix} {msg}{RESET}")


def log_step(step_id: str, name: str):
    print()
    print(f"  {CYAN}{BOLD}── Step {step_id}: {name} ──{RESET}")


def log_divider():
    print(f"  {DIM}{'─' * 50}{RESET}")


# ── Path helpers ──────────────────────────────────────────────────────────────

def module_dir(module_slug: str) -> Path:
    return CONTENT_DIR / module_slug


def lesson_dir(module_slug: str, lesson_slug: str) -> Path:
    return module_dir(module_slug) / lesson_slug


def lesson_slug(lesson_number: int, lesson_title: str) -> str:
    """Convert lesson number + title to filesystem slug."""
    clean = re.sub(r"[^a-z0-9\s]", "", lesson_title.lower())
    words = clean.split()[:6]
    return f"lesson-{lesson_number:02d}-{'-'.join(words)}"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


# ── File I/O ──────────────────────────────────────────────────────────────────

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log(f"Saved {path.relative_to(CONTENT_DIR.parent)}", "success")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: Any):
    write(path, json.dumps(data, indent=2, ensure_ascii=False))


def read_json(path: Path) -> Any:
    return json.loads(read(path))


def exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


# ── State / resume ────────────────────────────────────────────────────────────

def step_done(path: Path, force: bool = False) -> bool:
    """Return True if this step's output already exists (and force=False)."""
    if force:
        return False
    if exists(path):
        log(f"Skipping — already exists: {path.name}", "dim")
        return True
    return False


# ── JSON extraction ───────────────────────────────────────────────────────────

def extract_json(text: str) -> Any:
    """
    Extract JSON from a Claude response that may contain prose + JSON.
    Tries: raw parse → ```json block → first {...} or [...] block.
    """
    # 1. Try raw parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # 2. Try ```json ... ``` block
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. Try first { ... } or [ ... ] block
    for pattern in (r"(\{[\s\S]+\})", r"(\[[\s\S]+\])"):
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

    raise ValueError(f"Could not extract JSON from response:\n{text[:500]}...")


# ── Anthropic API ─────────────────────────────────────────────────────────────

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def call_claude(
    prompt: str,
    system: str = "",
    max_tokens: int = MAX_TOKENS,
    retries: int = 3,
    expect_json: bool = False,
) -> str:
    """
    Call Claude. Returns the text response.
    Retries on rate limits / transient errors.
    If expect_json=True, validates that the response contains parseable JSON.
    """
    client = get_client()
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                system=system if system else anthropic.NOT_GIVEN,
                messages=messages,
            )
            text = response.content[0].text

            if expect_json:
                extract_json(text)  # validate — raises if broken

            return text

        except anthropic.RateLimitError:
            wait = 2 ** attempt * 5
            log(f"Rate limited. Waiting {wait}s before retry {attempt + 1}/{retries}...", "warn")
            time.sleep(wait)

        except ValueError as e:
            if attempt < retries - 1:
                log(f"JSON parse failed (attempt {attempt + 1}). Retrying...", "warn")
                # Append a correction to the messages for next attempt
                messages.append({"role": "assistant", "content": text})
                messages.append({
                    "role": "user",
                    "content": "Your response could not be parsed as JSON. Please respond with ONLY valid JSON — no prose, no markdown fences, no explanation."
                })
            else:
                raise

        except anthropic.APIError as e:
            if attempt < retries - 1:
                wait = 2 ** attempt * 3
                log(f"API error: {e}. Retrying in {wait}s...", "warn")
                time.sleep(wait)
            else:
                raise

    raise RuntimeError(f"Failed after {retries} attempts")


def call_claude_json(prompt: str, system: str = "", max_tokens: int = MAX_TOKENS) -> Any:
    """Call Claude and return parsed JSON."""
    text = call_claude(prompt, system=system, max_tokens=max_tokens, expect_json=True)
    return extract_json(text)


# ── Prompt loading ────────────────────────────────────────────────────────────

def load_prompt(name: str) -> str:
    from .config import PROMPTS_DIR
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def fill_prompt(template: str, **kwargs) -> str:
    """Simple {key} substitution in prompt templates."""
    result = template
    for key, value in kwargs.items():
        placeholder = "{" + key + "}"
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2)
        result = result.replace(placeholder, str(value))
    return result


# ── Progress display ──────────────────────────────────────────────────────────

def print_header(title: str):
    width = 56
    print()
    print(f"  {CYAN}{'═' * width}{RESET}")
    print(f"  {CYAN}  {BOLD}{title}{RESET}")
    print(f"  {CYAN}{'═' * width}{RESET}")
    print()


def print_summary(results: dict):
    """Print a summary table of step results."""
    print()
    log_divider()
    for step, result in results.items():
        if result["status"] == "done":
            log(f"Step {step}: {result['label']} {DIM}({result.get('file', '')}){RESET}", "success")
        elif result["status"] == "skipped":
            log(f"Step {step}: {result['label']} {DIM}(already done){RESET}", "dim")
        elif result["status"] == "failed":
            log(f"Step {step}: {result['label']} — {result.get('error', 'unknown error')}", "error")
    log_divider()
    print()
