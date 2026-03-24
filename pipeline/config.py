"""
Forge Pipeline — Configuration
"""

import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "content"
PROMPTS_DIR = Path(__file__).parent / "prompts"

# ── Model ─────────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8192

# ── Step output filenames ──────────────────────────────────────────────────────

FILES = {
    "module_plan":      "module_plan.json",
    "sources":          "sources.json",
    "research":         "research.md",
    "lesson":           "lesson.mdx",
    "challenge":        "challenge.py",
    "tests":            "test_suite.py",
    "hints":            "hints.json",
    "solution":         "solution.py",
    "challenge_meta":   "challenge_meta.json",
    "quality_report":   "quality_report.json",
    "qa_log":           "qa_log.md",
    "diagram_specs":    "diagram_specs.json",
    "meta":             "meta.json",
}

# ── Step names (for CLI + logging) ────────────────────────────────────────────

STEPS = {
    "0a": "Module Decomposition",
    "0b": "Source Discovery",
    "1":  "Deep Research",
    "2":  "Lesson Structuring",
    "3":  "Challenge Generation",
    "4":  "Auto Quality Check",
}

# ── Beat types (for validation) ───────────────────────────────────────────────

BEAT_TYPES = [
    "DEMO", "HOOK", "CONCEPT", "DIAGRAM",
    "ANALOGY", "SOCRATIC", "CODE_READ",
    "CODE_WRITE", "GOTCHA", "CHECKPOINT",
]

BEAT_RULES = {
    "first_beat_must_be": "DEMO",
    "last_beat_must_be": "CHECKPOINT",
    "min_beats": 8,
    "max_beats": 12,
    "required_at_least_one": ["SOCRATIC", "GOTCHA"],
    "max_words_in_text_beat": 120,
}
