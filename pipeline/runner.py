#!/usr/bin/env python3
"""
Forge Pipeline — CLI Runner

Usage:
  # Run the full pipeline for a single lesson
  python -m pipeline run --module module-01-llm-internals --lesson 3

  # Run only specific steps
  python -m pipeline run --module module-01-llm-internals --lesson 3 --steps 0b,1,2

  # Bootstrap a new module (Step 0A only)
  python -m pipeline bootstrap --module module-01-llm-internals

  # Run the full module (all lessons, steps 0B–4)
  python -m pipeline module --module module-01-llm-internals

  # Re-run with QA flags applied
  python -m pipeline fix --module module-01-llm-internals --lesson 3

  # Auto-refine: loop Steps 2-3-4 until QA passes
  python -m pipeline refine --module module-01-llm-internals --lesson 1

  # Strict refine (only stop on full PASS, not WARN)
  python -m pipeline refine --module module-01-llm-internals --lesson 1 --require-pass

  # More attempts for stubborn lessons
  python -m pipeline refine --module module-01-llm-internals --lesson 1 --max-attempts 8

  # Force re-run even if output exists
  python -m pipeline run --module module-01-llm-internals --lesson 3 --force

  # Show status of a module
  python -m pipeline status --module module-01-llm-internals
"""

import argparse
import json
import sys
from pathlib import Path

from .config import CONTENT_DIR, STEPS, FILES
from .utils import (
    log, log_step, log_divider, print_header,
    module_dir, lesson_dir, lesson_slug,
    read_json, write_json, exists,
)
from .steps import (
    run_step_0a, run_step_0b, run_step_1,
    run_step_2, run_step_3, run_step_4,
    write_meta,
)


# ─────────────────────────────────────────────────────────────────────────────
# Module registry — add new modules here
# ─────────────────────────────────────────────────────────────────────────────

MODULES = {
    "module-01-llm-internals": {
        "title": "How LLMs Actually Work",
        "type": "EVERGREEN",
        "lesson_count": 10,
        "prereqs": [],
        "capstone": (
            "An interactive web app called the LLM Internals Playground. "
            "Panels include: live tokenizer, sampling distribution with temperature/top-p sliders, "
            "attention heatmap, embedding visualizer, hallucination risk indicator, "
            "model comparator. Built panel-by-panel across 10 lessons. "
            "Each lesson adds one working panel to the running app."
        ),
    },
    "module-02-agents": {
        "title": "AI Agents From Zero",
        "type": "CURRENT",
        "lesson_count": 12,
        "prereqs": ["module-01-llm-internals"],
        "capstone": (
            "An Autonomous Deep Research Agent. Give it any topic, get a fully cited "
            "research report with no human in the loop. Implements all 5 Anthropic agent "
            "workflow patterns: Prompt Chaining, Routing, Parallelization, "
            "Orchestrator-Workers, Evaluator-Optimizer. Ships with a full eval suite."
        ),
    },
    "module-03-evals": {
        "title": "Agent Evals: Measuring What You Build",
        "type": "CURRENT",
        "lesson_count": 10,
        "prereqs": ["module-02-agents"],
        "capstone": (
            "A Universal Agent Eval Suite — reusable evaluation harness attached to "
            "every project from this module forward. Unit, trajectory, and end-to-end "
            "test runners. LLM-as-judge. 50+ test cases. CI-ready regression runner."
        ),
    },
    "module-04-prompts": {
        "title": "Prompt Engineering That Actually Matters",
        "type": "EVERGREEN",
        "lesson_count": 10,
        "prereqs": ["module-03-evals"],
        "capstone": (
            "An Automatic Prompt Optimization Engine. Takes any underperforming prompt, "
            "generates variants using every technique covered (CoT, few-shot, structured output, "
            "chaining, meta-prompting), scores them with the Eval Suite, returns a ranked leaderboard."
        ),
    },
    "module-05-rag": {
        "title": "RAG From Scratch",
        "type": "CURRENT",
        "lesson_count": 12,
        "prereqs": ["module-04-prompts"],
        "capstone": (
            "A Personal Second Brain — RAG over your entire knowledge base. "
            "Multi-format ingestion, smart chunking, hybrid search, re-ranker, "
            "GraphRAG, agentic retrieval, RAGAS eval suite."
        ),
    },
    "module-06-tools": {
        "title": "Tools and Function Calling",
        "type": "CURRENT",
        "lesson_count": 10,
        "prereqs": ["module-05-rag"],
        "capstone": (
            "Personal AI Assistant (Mini Jarvis). Natural language interface to: "
            "web search, URL reader, file system, Gmail MCP, Calendar MCP, "
            "sandboxed Python executor, browser automation."
        ),
    },
    "module-07-local": {
        "title": "Running AI Locally",
        "type": "CURRENT",
        "lesson_count": 10,
        "prereqs": ["module-06-tools"],
        "capstone": (
            "The Private AI Workstation. Self-hosted AI server: Ollama serving multiple "
            "models on a network API, local embeddings, local vector store, local agents, "
            "benchmark dashboard."
        ),
    },
    "module-08-memory": {
        "title": "Agent Memory Systems",
        "type": "EVERGREEN",
        "lesson_count": 9,
        "prereqs": ["module-07-local"],
        "capstone": (
            "AI Life Coach with Persistent Memory. Four-layer memory: in-context compressor, "
            "episodic vector store, semantic knowledge graph, procedural workflow store. "
            "Importance scorer, memory decay, unified retrieval."
        ),
    },
    "module-09-multi-agent": {
        "title": "Multi-Agent Systems",
        "type": "CURRENT",
        "lesson_count": 10,
        "prereqs": ["module-08-memory"],
        "capstone": (
            "Autonomous Startup Intelligence Firm. Produces investor-grade 10-page research "
            "reports fully autonomously. Orchestrator + 5 specialist workers + critic + "
            "fact-checker. Compared against LangGraph and CrewAI implementations."
        ),
    },
    "module-10-vectordbs": {
        "title": "Vector Databases Deep Dive",
        "type": "CURRENT",
        "lesson_count": 10,
        "prereqs": ["module-09-multi-agent"],
        "capstone": (
            "Universal Semantic Search Engine. 200K+ documents, five parallel vector DB "
            "backends (pgvector, ChromaDB, Qdrant, Weaviate, Pinecone), live latency/recall "
            "dashboard."
        ),
    },
    "module-11-quantization": {
        "title": "Model Quantization Explained",
        "type": "EVERGREEN",
        "lesson_count": 9,
        "prereqs": ["module-10-vectordbs"],
        "capstone": (
            "Personal Model Deployment Pipeline. HuggingFace → GGUF automation, "
            "four-level quantization (INT8, INT4, GPTQ, AWQ), 5-domain benchmark suite, "
            "Ollama deployment with complexity-based routing."
        ),
    },
    "module-12-production": {
        "title": "Production AI Systems",
        "type": "EVERGREEN",
        "lesson_count": 12,
        "prereqs": ["module-11-quantization"],
        "capstone": (
            "Production AI API. Streaming, semantic cache, complexity router, "
            "Langfuse observability, eval CI pipeline, rate limiter, fallback chains, "
            "multi-tenant cost tracker, real-time ops dashboard."
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_module(module_slug: str) -> dict:
    if module_slug not in MODULES:
        log(f"Unknown module: {module_slug}", "error")
        log(f"Available: {', '.join(MODULES.keys())}", "info")
        sys.exit(1)
    return MODULES[module_slug]


def get_lesson(module_slug: str, lesson_number: int) -> dict:
    plan_path = module_dir(module_slug) / FILES["module_plan"]
    if not plan_path.exists():
        log(f"Module plan not found. Run bootstrap first: pipeline bootstrap --module {module_slug}", "error")
        sys.exit(1)
    plan = read_json(plan_path)
    lessons = plan.get("lessons", [])
    matches = [l for l in lessons if l["lesson_number"] == lesson_number]
    if not matches:
        log(f"Lesson {lesson_number} not found in module plan", "error")
        sys.exit(1)
    return matches[0]


def parse_steps(steps_str: str) -> list[str]:
    """Parse '0b,1,2,3' into ['0b', '1', '2', '3']"""
    return [s.strip() for s in steps_str.split(",")]


def lesson_runs_in_browser(lesson_number: int) -> bool:
    """Early lessons (1-3) run in browser. Later ones use local env."""
    return lesson_number <= 3


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────

def cmd_bootstrap(args):
    """Step 0A — decompose a module into lesson plans."""
    m = get_module(args.module)
    print_header(f"Bootstrap: {m['title']}")

    run_step_0a(
        module_slug=args.module,
        module_title=m["title"],
        capstone_description=m["capstone"],
        lesson_count=m["lesson_count"],
        module_type=m["type"],
        prereqs=m["prereqs"],
        force=args.force,
    )

    # Show the plan
    plan_path = module_dir(args.module) / FILES["module_plan"]
    plan = read_json(plan_path)
    print()
    log("Module plan generated:", "success")
    log_divider()
    for lesson in plan["lessons"]:
        print(f"  {lesson['lesson_number']:2d}. {lesson['title']}")
        print(f"      Concept: {lesson['concept']}")
        print(f"      Builds: {lesson['what_gets_built']}")
        print()
    log_divider()
    log("Review the plan above. If it looks right, run lessons next.", "info")
    log(f"Next: python -m pipeline run --module {args.module} --lesson 1", "info")


def cmd_run(args):
    """Run the pipeline for a specific lesson (steps 0B–4)."""
    m = get_module(args.module)
    lesson = get_lesson(args.module, args.lesson)
    steps = parse_steps(args.steps) if args.steps else ["0b", "1", "2", "3", "4"]

    print_header(f"Lesson {args.lesson}: {lesson['title']}")

    runs_in_browser = lesson_runs_in_browser(args.lesson)

    if "0b" in steps:
        run_step_0b(args.module, lesson, m["type"], force=args.force)

    if "1" in steps:
        run_step_1(args.module, lesson, m["type"], force=args.force)

    if "2" in steps:
        qa_flags = _load_qa_flags(args.module, args.lesson)
        run_step_2(args.module, lesson, qa_flags=qa_flags, force=args.force)

    if "3" in steps:
        run_step_3(args.module, lesson, runs_in_browser=runs_in_browser, force=args.force)

    if "4" in steps:
        run_step_4(args.module, lesson, force=args.force)

    # Always write/update meta
    write_meta(args.module, lesson, m["type"], runs_in_browser)

    print()
    log("Done. Review quality_report.json for any issues.", "success")
    log(f"Then: do the lesson yourself and fill in qa_log.md", "info")


def cmd_module(args):
    """Run the full pipeline for all lessons in a module (after bootstrap)."""
    m = get_module(args.module)
    plan_path = module_dir(args.module) / FILES["module_plan"]

    if not plan_path.exists():
        log("Module plan not found. Run bootstrap first.", "error")
        log(f"  python -m pipeline bootstrap --module {args.module}", "info")
        sys.exit(1)

    plan = read_json(plan_path)
    lessons = plan["lessons"]

    print_header(f"Module: {m['title']} ({len(lessons)} lessons)")

    # If --lesson-range specified, filter
    if args.lesson_range:
        start, end = (int(x) for x in args.lesson_range.split("-"))
        lessons = [l for l in lessons if start <= l["lesson_number"] <= end]
        log(f"Running lessons {start}–{end} ({len(lessons)} lessons)")

    for lesson in lessons:
        print()
        log(f"Processing lesson {lesson['lesson_number']}: {lesson['title']}", "step")
        runs_in_browser = lesson_runs_in_browser(lesson["lesson_number"])

        try:
            run_step_0b(args.module, lesson, m["type"], force=args.force)
            run_step_1(args.module, lesson, m["type"], force=args.force)
            qa_flags = _load_qa_flags(args.module, lesson["lesson_number"])
            run_step_2(args.module, lesson, qa_flags=qa_flags, force=args.force)
            run_step_3(args.module, lesson, runs_in_browser=runs_in_browser, force=args.force)
            run_step_4(args.module, lesson, force=args.force)
            write_meta(args.module, lesson, m["type"], runs_in_browser)
        except Exception as e:
            log(f"Lesson {lesson['lesson_number']} failed: {e}", "error")
            if not args.continue_on_error:
                sys.exit(1)
            log("Continuing to next lesson (--continue-on-error)", "warn")

    print()
    log(f"Module complete. Run status to review:", "success")
    log(f"  python -m pipeline status --module {args.module}", "info")


def cmd_fix(args):
    """Re-run Step 2 + 3 after QA flags have been added to qa_log.md."""
    lesson = get_lesson(args.module, args.lesson)
    m = get_module(args.module)

    qa_flags = _load_qa_flags(args.module, args.lesson)
    if not qa_flags:
        log("No QA flags found in qa_log.md. Nothing to fix.", "warn")
        log(f"Add flags to: {lesson_dir(args.module, lesson_slug(args.lesson, lesson['title'])) / FILES['qa_log']}", "info")
        return

    print_header(f"Fix: Lesson {args.lesson} — applying QA flags")
    log(f"Found QA flags:\n{qa_flags}", "info")

    runs_in_browser = lesson_runs_in_browser(args.lesson)
    run_step_2(args.module, lesson, qa_flags=qa_flags, force=True)
    run_step_3(args.module, lesson, runs_in_browser=runs_in_browser, force=True)
    run_step_4(args.module, lesson, force=True)
    write_meta(args.module, lesson, m["type"], runs_in_browser)

    log("Fix applied. Review quality_report.json and do the lesson again.", "success")


def cmd_refine(args):
    """Auto-fix loop: extract QA failures, re-run Steps 2-3-4, repeat until PASS."""
    m = get_module(args.module)
    lesson = get_lesson(args.module, args.lesson)
    runs_in_browser = lesson_runs_in_browser(args.lesson)
    l_slug = lesson_slug(args.lesson, lesson["title"])
    report_path = lesson_dir(args.module, l_slug) / FILES["quality_report"]

    print_header(f"Refine: Lesson {args.lesson} — {lesson['title']}")

    prev_failed_ids = None

    for attempt in range(1, args.max_attempts + 1):
        log(f"Attempt {attempt}/{args.max_attempts}", "step")

        flags = _extract_failures_from_report(args.module, args.lesson)

        if not flags:
            log("No quality report found — running initial Steps 2 → 3 → 4", "info")
            run_step_2(args.module, lesson, force=True)
            run_step_3(args.module, lesson, runs_in_browser=runs_in_browser, force=True)
            run_step_4(args.module, lesson, force=True)
        else:
            log(f"Injecting failures into prompts:\n{flags}", "info")
            run_step_2(args.module, lesson, qa_flags=flags, force=True)
            run_step_3(args.module, lesson, runs_in_browser=runs_in_browser, qa_flags=flags, force=True)
            run_step_4(args.module, lesson, force=True)

        write_meta(args.module, lesson, m["type"], runs_in_browser)

        report = read_json(report_path)
        overall = report.get("overall", "UNKNOWN")

        if overall == "PASS":
            log(f"PASS on attempt {attempt}. Lesson is ready.", "success")
            return

        if overall == "WARN" and not args.require_pass:
            log(f"WARN on attempt {attempt} — no blocking issues. Stopping (use --require-pass to continue).", "success")
            return

        # Stall detection: same FAIL check IDs two attempts in a row
        current_failed_ids = frozenset(
            c["id"] for c in report.get("checks", []) if c["status"] == "FAIL"
        )
        if prev_failed_ids is not None and current_failed_ids == prev_failed_ids:
            log(
                f"Same checks failing as last attempt: {', '.join(sorted(current_failed_ids))}. "
                "This is likely a structural issue — consider editing module_plan.json directly "
                "and re-running with: --steps 2,3,4 --force",
                "warn",
            )
        prev_failed_ids = current_failed_ids

        blocking = report.get("blocking_issues", [])
        log(f"Still FAIL — {len(blocking)} blocking issue(s). Looping...", "warn")

    log(f"Reached max attempts ({args.max_attempts}). Still not passing.", "error")
    log("Review quality_report.json — the remaining issues may be structural.", "info")


def cmd_status(args):
    """Show completion status for all lessons in a module."""
    m = get_module(args.module)
    plan_path = module_dir(args.module) / FILES["module_plan"]

    if not plan_path.exists():
        log("Module plan not found. Run bootstrap first.", "error")
        return

    plan = read_json(plan_path)
    lessons = plan["lessons"]

    print_header(f"Status: {m['title']}")

    total = len(lessons)
    done = 0

    for lesson in lessons:
        l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
        l_dir = lesson_dir(args.module, l_slug)

        has_research  = exists(l_dir / FILES["research"])
        has_lesson    = exists(l_dir / FILES["lesson"])
        has_challenge = exists(l_dir / FILES["challenge"])
        has_qa_report = exists(l_dir / FILES["quality_report"])
        has_qa_log    = exists(l_dir / FILES["qa_log"])

        # Read quality report status
        qa_status = "—"
        if has_qa_report:
            try:
                report = read_json(l_dir / FILES["quality_report"])
                qa_status = report.get("overall", "?")
            except Exception:
                qa_status = "err"

        # Overall status
        if has_qa_log:
            status = "✅ QA done"
            done += 1
        elif qa_status == "PASS" and has_challenge:
            status = "🟡 Needs QA"
        elif has_lesson and has_challenge:
            status = "🔵 Generated"
        elif has_research:
            status = "🔵 Researched"
        else:
            status = "⬜ Not started"

        report_indicator = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗"}.get(qa_status, "—")

        print(
            f"  {lesson['lesson_number']:2d}. "
            f"{'R' if has_research else '·'}"
            f"{'L' if has_lesson else '·'}"
            f"{'C' if has_challenge else '·'}"
            f" {report_indicator} "
            f"{status:<14} {lesson['title'][:55]}"
        )

    log_divider()
    log(f"{done}/{total} lessons fully QA'd", "info")
    print("  Legend: R=Research  L=Lesson  C=Challenge  ✓=QA pass  ⚠=warn  ✗=fail")
    print()


def cmd_list(args):
    """List all available modules."""
    print_header("Available Modules")
    for slug, m in MODULES.items():
        plan_path = module_dir(slug) / FILES["module_plan"]
        bootstrapped = "✅" if plan_path.exists() else "⬜"
        print(f"  {bootstrapped} {slug}")
        print(f"       {m['title']} ({m['lesson_count']} lessons · {m['type']})")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# QA flag loader
# ─────────────────────────────────────────────────────────────────────────────

def _load_qa_flags(module_slug: str, lesson_number: int) -> str:
    """Load QA flags from qa_log.md for this lesson."""
    plan_path = module_dir(module_slug) / FILES["module_plan"]
    if not plan_path.exists():
        return ""
    plan = read_json(plan_path)
    lessons = plan.get("lessons", [])
    match = next((l for l in lessons if l["lesson_number"] == lesson_number), None)
    if not match:
        return ""

    l_slug = lesson_slug(lesson_number, match["title"])
    qa_path = lesson_dir(module_slug, l_slug) / FILES["qa_log"]

    if not qa_path.exists():
        return ""

    content = qa_path.read_text(encoding="utf-8")
    # Extract just the Flags section
    import re
    flags_match = re.search(r"### Flags\n([\s\S]+?)(?=###|$)", content)
    if flags_match:
        return flags_match.group(1).strip()
    return content.strip()


# ─────────────────────────────────────────────────────────────────────────────
# QA report failure extractor (for refine loop)
# ─────────────────────────────────────────────────────────────────────────────

def _extract_failures_from_report(module_slug: str, lesson_number: int) -> str:
    """Extract FAIL checks, blocking issues, and auto-fixable suggestions from quality_report.json."""
    plan_path = module_dir(module_slug) / FILES["module_plan"]
    if not plan_path.exists():
        return ""
    plan = read_json(plan_path)
    lessons = plan.get("lessons", [])
    match = next((l for l in lessons if l["lesson_number"] == lesson_number), None)
    if not match:
        return ""

    l_slug = lesson_slug(lesson_number, match["title"])
    report_path = lesson_dir(module_slug, l_slug) / FILES["quality_report"]

    if not report_path.exists():
        return ""

    report = read_json(report_path)

    parts = []

    failed_checks = [c for c in report.get("checks", []) if c["status"] == "FAIL"]
    if failed_checks:
        parts.append("FAILED CHECKS:")
        for c in failed_checks:
            parts.append(f"  - [{c['id']}] {c.get('detail', 'no detail')}")

    blocking = report.get("blocking_issues", [])
    if blocking:
        parts.append("BLOCKING ISSUES:")
        for b in blocking:
            parts.append(f"  - {b}")

    fixable = report.get("auto_fixable", [])
    if fixable:
        parts.append("SUGGESTED FIXES:")
        for f in fixable:
            parts.append(f"  - {f}")

    return "\n".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Forge Content Pipeline — AI-generated lessons for AI engineering",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # bootstrap
    p_boot = subparsers.add_parser("bootstrap", help="Step 0A — decompose module into lesson plan")
    p_boot.add_argument("--module", required=True, help="Module slug (e.g. module-01-llm-internals)")
    p_boot.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # run (single lesson)
    p_run = subparsers.add_parser("run", help="Run pipeline for a single lesson (steps 0B–4)")
    p_run.add_argument("--module", required=True)
    p_run.add_argument("--lesson", required=True, type=int, help="Lesson number")
    p_run.add_argument("--steps", help="Comma-separated steps to run (e.g. 0b,1,2). Default: all.")
    p_run.add_argument("--force", action="store_true")

    # module (all lessons)
    p_mod = subparsers.add_parser("module", help="Run pipeline for all lessons in a module")
    p_mod.add_argument("--module", required=True)
    p_mod.add_argument("--lesson-range", help="e.g. 1-5 to run lessons 1 through 5 only")
    p_mod.add_argument("--force", action="store_true")
    p_mod.add_argument("--continue-on-error", action="store_true")

    # fix (apply QA flags)
    p_fix = subparsers.add_parser("fix", help="Re-run steps 2+3 after adding QA flags to qa_log.md")
    p_fix.add_argument("--module", required=True)
    p_fix.add_argument("--lesson", required=True, type=int)

    # refine (auto-fix loop)
    p_refine = subparsers.add_parser("refine", help="Auto-fix loop: re-run 2-3-4 using QA failures until PASS")
    p_refine.add_argument("--module", required=True)
    p_refine.add_argument("--lesson", required=True, type=int)
    p_refine.add_argument("--max-attempts", type=int, default=5)
    p_refine.add_argument("--require-pass", action="store_true",
                          help="Only stop on full PASS, keep looping through WARNs")

    # status
    p_status = subparsers.add_parser("status", help="Show completion status for a module")
    p_status.add_argument("--module", required=True)

    # list
    subparsers.add_parser("list", help="List all available modules")

    args = parser.parse_args()

    commands = {
        "bootstrap": cmd_bootstrap,
        "run":       cmd_run,
        "module":    cmd_module,
        "fix":       cmd_fix,
        "refine":    cmd_refine,
        "status":    cmd_status,
        "list":      cmd_list,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
