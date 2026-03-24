"""
Forge Pipeline — Steps 0A through 4
Each step is a pure function: takes inputs, returns output path(s).
"""

import json
from datetime import datetime
from pathlib import Path

from .config import FILES, BEAT_RULES, BEAT_TYPES
from .utils import (
    call_claude, call_claude_json,
    write, write_json, read, read_json,
    step_done, log, log_step, extract_json,
    module_dir, lesson_dir, lesson_slug, ensure_dir,
)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 0A — Module Decomposition
# Input:  module title, capstone description, lesson count, module type
# Output: content/{module_slug}/module_plan.json
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_0A = """
You are designing a hands-on AI engineering module for developers.
The learner is a confident fullstack developer with ZERO AI background.
They are smart, pragmatic, and will quit if they spend a lesson learning something they can't use immediately.

MODULE TITLE: {module_title}
CAPSTONE PROJECT: {capstone_description}
TOTAL LESSONS: {lesson_count}
MODULE TYPE: {module_type}
PREREQUISITE MODULES: {prereqs}

Decompose this module into exactly {lesson_count} lessons.

For each lesson produce a JSON object with:
- lesson_number: integer (1-based)
- title: action-oriented and specific ("Adding the Search Pipeline", NOT "Search")
- concept: the ONE core concept introduced (not a list, exactly one)
- what_gets_built: one sentence — what can the project do after this lesson that it couldn't before?
- codebase_state_before: what exists in the repo going INTO this lesson (be specific about files/functions)
- codebase_state_after: what exists AFTER this lesson (new files/functions added)
- why_here: why does this concept appear at lesson N and not earlier or later? (2-3 sentences, reasoning)
- depends_on: list of lesson_numbers that must be complete first
- primary_question: the single question this lesson answers, phrased as a developer would ask it
- lesson_type: one of CONCEPT_HEAVY | CODE_HEAVY | BALANCED
- estimated_minutes: realistic for a first-timer building it (typically 25-50)
- xp_reward: integer between 100-160 (higher for harder/longer lessons)

Hard rules — enforce all of these:
1. Lesson 1 is ALWAYS a live demo of the FINISHED capstone. The learner sees it working before writing one line.
2. Every lesson after Lesson 1 ends with something VISIBLY WORKING. No dead-end theory lessons.
3. Concepts are introduced the EXACT moment the project needs them — not before, not as future context.
4. The final lesson polishes, tests, and ships the complete capstone.
5. No lesson introduces more than ONE major concept.
6. Lesson titles must be specific enough that someone could Google the concept and find it.

Output ONLY a JSON array of lesson objects. No prose. No markdown.
""".strip()


def run_step_0a(
    module_slug: str,
    module_title: str,
    capstone_description: str,
    lesson_count: int,
    module_type: str = "EVERGREEN",
    prereqs: list[str] = None,
    force: bool = False,
) -> Path:
    log_step("0A", "Module Decomposition")

    out_path = module_dir(module_slug) / FILES["module_plan"]

    if step_done(out_path, force):
        return out_path

    log(f"Decomposing '{module_title}' into {lesson_count} lessons...")

    prompt = PROMPT_0A.format(
        module_title=module_title,
        capstone_description=capstone_description,
        lesson_count=lesson_count,
        module_type=module_type,
        prereqs=json.dumps(prereqs or []),
    )

    data = call_claude_json(prompt)

    # Validate we got the right number of lessons
    if len(data) != lesson_count:
        log(f"Warning: expected {lesson_count} lessons, got {len(data)}. Proceeding.", "warn")

    # Enrich with module metadata
    plan = {
        "module_slug": module_slug,
        "module_title": module_title,
        "module_type": module_type,
        "capstone_description": capstone_description,
        "generated_at": datetime.now().isoformat(),
        "lessons": data,
    }

    ensure_dir(module_dir(module_slug))
    write_json(out_path, plan)
    log(f"Module plan: {len(data)} lessons decomposed", "success")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# STEP 0B — Source Discovery
# Input:  lesson plan object
# Output: content/{module_slug}/{lesson_slug}/sources.json
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_0B = """
You are finding the best source material for an AI engineering lesson.

LESSON TITLE: {title}
CONCEPT TO TEACH: {concept}
PRIMARY QUESTION: {primary_question}
WHAT GETS BUILT: {what_gets_built}
MODULE TYPE: {module_type}

Search the web and find the 5 best sources for teaching this concept.

Prioritise in this order:
1. Official documentation (Anthropic, OpenAI, LangChain, HuggingFace, etc.)
2. Engineering blog posts from companies who have solved this in production
3. Seminal research papers (if the concept has one)
4. Well-regarded technical deep-dives (Lilian Weng, Simon Willison, Jay Alammar, etc.)

Avoid: SEO tutorial farms, YouTube transcripts, outdated sources
For CURRENT modules: avoid anything >18 months old
For EVERGREEN modules: age doesn't matter if the content is correct

Return a JSON object with:
{{
  "sources": [
    {{
      "rank": 1,
      "url": "https://...",
      "title": "...",
      "type": "OFFICIAL_DOCS | ENGINEERING_BLOG | PAPER | DEEP_DIVE",
      "relevance_score": 8,
      "what_it_covers": "one sentence",
      "freshness": "2024-06 or undated",
      "key_sections": ["Section name", "Another section"]
    }}
  ],
  "known_misconceptions": [
    "Misconception 1 — what people wrongly believe",
    "Misconception 2",
    "Misconception 3"
  ],
  "related_concepts": [
    "Concept people confuse this with",
    "Another one"
  ],
  "search_terms_used": ["term1", "term2"]
}}

Output ONLY the JSON object. No prose.
""".strip()


def run_step_0b(
    module_slug: str,
    lesson: dict,
    module_type: str = "EVERGREEN",
    force: bool = False,
) -> Path:
    log_step("0B", f"Source Discovery — {lesson['title']}")

    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    out_path = lesson_dir(module_slug, l_slug) / FILES["sources"]

    if step_done(out_path, force):
        return out_path

    log(f"Finding sources for: {lesson['concept']}")

    prompt = PROMPT_0B.format(
        title=lesson["title"],
        concept=lesson["concept"],
        primary_question=lesson["primary_question"],
        what_gets_built=lesson["what_gets_built"],
        module_type=module_type,
    )

    system = "You are a technical curriculum researcher. You find primary sources for teaching complex engineering concepts. Always return valid JSON."

    data = call_claude_json(prompt, system=system)

    ensure_dir(lesson_dir(module_slug, l_slug))
    write_json(out_path, data)
    log(f"Found {len(data.get('sources', []))} sources", "success")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Deep Research
# Input:  lesson plan + top sources from Step 0B
# Output: content/{module_slug}/{lesson_slug}/research.md
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_1 = """
You are researching a concept for a hands-on AI engineering lesson.

The learner is a confident fullstack developer. Zero AI background.
They are smart and pragmatic. They hate:
- Hand-waving ("essentially, the model just...")  
- Magic ("it figures out the best response")
- Assumed context ("as you know, transformers...")

CONCEPT: {concept}
PRIMARY QUESTION THIS LESSON ANSWERS: {primary_question}
WHAT THE LEARNER WILL BUILD: {what_gets_built}
CODEBASE STATE ENTERING LESSON: {codebase_state_before}
CODEBASE STATE AFTER LESSON: {codebase_state_after}

KNOWN MISCONCEPTIONS ABOUT THIS CONCEPT:
{misconceptions}

SOURCE MATERIAL FOUND:
{source_titles}

---

Write a research document with these sections:

## 1. First Principles Explanation
Explain {concept} from scratch. No jargon until it has been earned.
Start from what a fullstack dev already knows. Build up to the full picture.
Max 300 words. No bullet lists — flowing prose that builds up sequentially.

## 2. Why This Concept Exists
What specific problem does it solve? What breaks — concretely — without it?
Give one real failure case with code or a specific example.

## 3. The Mental Model
One analogy that genuinely holds up. Not a dumbed-down one.
Then explicitly state where the analogy breaks down (this is mandatory).

## 4. How It Actually Works (Implementation)
The specific pattern used in production for {what_gets_built}.
Show real code or detailed pseudocode. No hand-waving allowed here.
Include the actual function signatures and data shapes.

## 5. Common Misconceptions
Address exactly the misconceptions listed above.
For each: state the wrong belief → why it's wrong → the correct framing.

## 6. What Can Go Wrong
The 2 most common failure modes when implementing this.
What do they look like in practice? How do you fix them?

## 7. The Production Reality
How is this actually used at companies running real AI systems?
What only becomes obvious when you hit scale or production?

## 8. Connections
How does this concept connect to what came before in the module?
What does understanding this unlock in future lessons?

---
Write for a developer who will be building with this in 30 minutes.
Do not pad. Do not repeat. If something is uncertain, say so explicitly.
""".strip()


def run_step_1(
    module_slug: str,
    lesson: dict,
    module_type: str = "EVERGREEN",
    force: bool = False,
) -> Path:
    log_step("1", f"Deep Research — {lesson['concept']}")

    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    out_path = lesson_dir(module_slug, l_slug) / FILES["research"]
    sources_path = lesson_dir(module_slug, l_slug) / FILES["sources"]

    if step_done(out_path, force):
        return out_path

    # Load sources if available
    misconceptions = []
    source_titles = "No sources pre-fetched — research from your training knowledge."
    if sources_path.exists():
        sources_data = read_json(sources_path)
        misconceptions = sources_data.get("known_misconceptions", [])
        sources = sources_data.get("sources", [])[:3]
        source_titles = "\n".join(
            f"- {s['title']} ({s['type']}): {s['what_it_covers']}"
            for s in sources
        )

    log(f"Researching: {lesson['concept']}")

    prompt = PROMPT_1.format(
        concept=lesson["concept"],
        primary_question=lesson["primary_question"],
        what_gets_built=lesson["what_gets_built"],
        codebase_state_before=lesson["codebase_state_before"],
        codebase_state_after=lesson["codebase_state_after"],
        misconceptions="\n".join(f"- {m}" for m in misconceptions) or "None found.",
        source_titles=source_titles,
    )

    system = "You are a senior AI engineer and technical educator. You explain complex concepts from first principles, honestly and without padding. Write as if teaching a smart colleague."

    research = call_claude(prompt, system=system, max_tokens=4000)

    write(out_path, research)
    log(f"Research doc: {len(research.split())} words", "success")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Lesson Structuring
# Input:  lesson plan + research.md
# Output: content/{module_slug}/{lesson_slug}/lesson.mdx
#         content/{module_slug}/{lesson_slug}/diagram_specs.json
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_2 = """
You are structuring an AI engineering lesson into interactive beats.

LESSON PLAN:
{lesson_plan}

RESEARCH DOCUMENT:
{research}

QA FLAGS FROM PREVIOUS RUN (if any):
{qa_flags}

---

Structure this lesson as a JSON object with a "beats" array.
Each beat is one interactive unit the learner progresses through sequentially.

BEAT TYPES AND THEIR SCHEMAS:

DEMO: {{ "type": "DEMO", "description": "what the learner will see working by end of lesson — 1-2 sentences" }}

HOOK: {{ "type": "HOOK", "body": "why this matters RIGHT NOW, what breaks without it — max 80 words" }}

CONCEPT: {{ "type": "CONCEPT", "title": "...", "body": "plain english first — max 120 words", "key_term": "the term being introduced", "definition": "one-sentence dictionary-style definition" }}

DIAGRAM: {{ "type": "DIAGRAM", "caption": "...", "description": "PRECISE generatable description — shapes, arrows, labels, layout. Example: 'Left-to-right flow diagram. Three boxes: Raw Query → embed() arrow → Vector Index cylinder → top-k arrow → LLM box → Answer box. Monospace labels. Black on white. No decorative elements.'" }}

ANALOGY: {{ "type": "ANALOGY", "collapsed_by_default": true, "analogy": "...", "where_it_breaks": "be explicit about the limit" }}

SOCRATIC: {{ "type": "SOCRATIC", "question": "...", "think_prompt": "Take 10 seconds. Think about...", "answer": "the revealed answer", "why_this_matters": "one sentence payoff" }}

CODE_READ: {{ "type": "CODE_READ", "language": "python|typescript", "code": "...", "annotations": [{{"line_range": [1, 5], "note": "..."}}] }}

GOTCHA: {{ "type": "GOTCHA", "wrong": "what people do wrong", "right": "what to do instead", "why": "one sentence" }}

CHECKPOINT: {{ "type": "CHECKPOINT", "questions": [{{"question": "...", "options": ["A", "B", "C", "D"], "correct_index": 0, "explanation": "shown after answer"}}] }}

---

RULES (all mandatory):
1. FIRST beat MUST be DEMO
2. SECOND beat MUST be HOOK  
3. LAST beat MUST be CHECKPOINT with exactly 3 questions
4. CONCEPT beat MUST appear before any CODE_READ/CODE_WRITE that uses that concept
5. Max 120 words in any text field (CONCEPT.body, HOOK.body, ANALOGY.analogy)
6. ANALOGY always has collapsed_by_default: true
7. Minimum 1 SOCRATIC beat
8. Minimum 1 GOTCHA beat
9. Total beats: 8 to 12
10. DIAGRAM descriptions must be precise enough to generate without ambiguity — never vague like "show how X works"
11. CHECKPOINT questions test understanding, NOT memorisation of definitions
12. CODE_READ code must be real, runnable, relevant to what_gets_built

Output a JSON object:
{{
  "lesson_id": "{lesson_id}",
  "title": "{title}",
  "concept": "{concept}",
  "beats": [ ...beat objects... ],
  "diagram_specs": [ ...extracted DIAGRAM beats for SVG generation... ]
}}

Output ONLY the JSON. No prose. No markdown fences.
""".strip()


def run_step_2(
    module_slug: str,
    lesson: dict,
    qa_flags: str = "",
    force: bool = False,
) -> tuple[Path, Path]:
    log_step("2", f"Lesson Structuring — {lesson['title']}")

    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    l_dir = lesson_dir(module_slug, l_slug)
    out_path = l_dir / FILES["lesson"]
    diagram_path = l_dir / FILES["diagram_specs"]

    if step_done(out_path, force):
        return out_path, diagram_path

    research_path = l_dir / FILES["research"]
    if not research_path.exists():
        raise FileNotFoundError(f"research.md not found — run Step 1 first: {research_path}")

    research = read(research_path)

    log(f"Structuring lesson: {lesson['title']}")

    lesson_id = f"m{module_slug.split('-')[1]}-l{lesson['lesson_number']:02d}"

    prompt = PROMPT_2.format(
        lesson_plan=json.dumps(lesson, indent=2),
        research=research,
        qa_flags=qa_flags or "None.",
        lesson_id=lesson_id,
        title=lesson["title"],
        concept=lesson["concept"],
    )

    system = "You are an expert instructional designer building a premium AI engineering course. Every beat must earn its place. Output only valid JSON."

    data = call_claude_json(prompt, system=system, max_tokens=6000)

    # Validate beat structure
    beats = data.get("beats", [])
    _validate_beats(beats, lesson["title"])

    # Write lesson MDX (beats as structured JSON embedded in MDX frontmatter)
    mdx_content = _beats_to_mdx(data)
    write(out_path, mdx_content)

    # Write diagram specs separately for SVG generation pipeline
    diagram_specs = [b for b in beats if b["type"] == "DIAGRAM"]
    write_json(diagram_path, {"lesson_id": lesson_id, "diagrams": diagram_specs})

    log(f"Lesson structured: {len(beats)} beats", "success")
    return out_path, diagram_path


def _validate_beats(beats: list, title: str):
    """Warn if beat rules are violated — doesn't fail, just logs."""
    if not beats:
        log("No beats generated!", "error")
        return

    if beats[0]["type"] != "DEMO":
        log(f"Rule violation: first beat is {beats[0]['type']}, expected DEMO", "warn")
    if beats[-1]["type"] != "CHECKPOINT":
        log(f"Rule violation: last beat is {beats[-1]['type']}, expected CHECKPOINT", "warn")

    types = [b["type"] for b in beats]
    for required in ["SOCRATIC", "GOTCHA"]:
        if required not in types:
            log(f"Rule violation: no {required} beat found in '{title}'", "warn")

    if not (BEAT_RULES["min_beats"] <= len(beats) <= BEAT_RULES["max_beats"]):
        log(f"Beat count {len(beats)} outside range {BEAT_RULES['min_beats']}–{BEAT_RULES['max_beats']}", "warn")


def _beats_to_mdx(data: dict) -> str:
    """Convert structured beat JSON to an MDX file with frontmatter."""
    beats_json = json.dumps(data["beats"], indent=2, ensure_ascii=False)
    return f"""---
lesson_id: "{data.get('lesson_id', '')}"
title: "{data.get('title', '')}"
concept: "{data.get('concept', '')}"
---

{{/* This file is auto-generated by the Forge content pipeline. */}}
{{/* Edit research.md and re-run Step 2 to update. */}}

export const beats = {beats_json}
"""


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Challenge Generation
# Input:  lesson plan + lesson beats
# Output: challenge.py, test_suite.py, hints.json, solution.py, challenge_meta.json
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_3 = """
You are writing a code challenge for an AI engineering lesson.

LESSON: {title}
CONCEPT BEING PRACTICED: {concept}
CODEBASE STATE BEFORE: {codebase_state_before}
CODEBASE STATE AFTER: {codebase_state_after}
WHAT GETS BUILT: {what_gets_built}
RUNS IN BROWSER: {runs_in_browser}

The learner has just read the lesson. Now they must implement ONE function or class
that makes the next piece of the project work.

Requirements:
- Exactly ONE function or class to implement (no sprawling multi-function challenges)
- This must be the ACTUAL function from the project — not a toy exercise
- Implementable in 10-15 minutes with the lesson fresh in mind
- Starter code provides: imports, docstring, type hints, function signature, helpers
- Mock all external API calls in tests (no real HTTP requests)
- Tests: 1 happy path, 1 edge case, 1 failure case minimum

Return a JSON object with these keys:
{{
  "challenge_py": "full content of challenge.py with # YOUR CODE HERE comments",
  "test_suite_py": "full content of test_suite.py (pytest)",
  "solution_py": "full content of solution.py (reference implementation — never shown to learner)",
  "hints": {{
    "hint_1": "conceptual nudge — no code, just direction",
    "hint_2": "points to specific docs, pattern, or approach — still no code",
    "hint_3": "skeleton with blanks — partial code, NOT the full answer"
  }},
  "meta": {{
    "title": "short challenge title",
    "function_name": "the_function_name",
    "difficulty": "GUIDED | DESIGN | DEBUG | EXTEND",
    "time_estimate_minutes": 12,
    "concepts_tested": ["concept1"],
    "common_mistakes": ["mistake QA should watch for"],
    "runs_in_browser": {runs_in_browser}
  }}
}}

Challenge.py must start with this comment block:
# Forge Challenge — {title}
# Implement the function below.
# Run tests with: pytest test_suite.py -v

Output ONLY the JSON object. No prose.
""".strip()


def run_step_3(
    module_slug: str,
    lesson: dict,
    runs_in_browser: bool = False,
    force: bool = False,
) -> dict[str, Path]:
    log_step("3", f"Challenge Generation — {lesson['title']}")

    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    l_dir = lesson_dir(module_slug, l_slug)

    out_paths = {
        "challenge": l_dir / FILES["challenge"],
        "tests":     l_dir / FILES["tests"],
        "hints":     l_dir / FILES["hints"],
        "solution":  l_dir / FILES["solution"],
        "meta":      l_dir / FILES["challenge_meta"],
    }

    if step_done(out_paths["challenge"], force):
        return out_paths

    log(f"Generating challenge for: {lesson['title']}")

    prompt = PROMPT_3.format(
        title=lesson["title"],
        concept=lesson["concept"],
        codebase_state_before=lesson["codebase_state_before"],
        codebase_state_after=lesson["codebase_state_after"],
        what_gets_built=lesson["what_gets_built"],
        runs_in_browser=str(runs_in_browser).lower(),
    )

    system = "You are a senior engineer writing precise, testable code challenges for an AI engineering course. All code must be correct, runnable, and educational."

    data = call_claude_json(prompt, system=system, max_tokens=5000)

    write(out_paths["challenge"], data["challenge_py"])
    write(out_paths["tests"],     data["test_suite_py"])
    write(out_paths["solution"],  data["solution_py"])
    write_json(out_paths["hints"], data["hints"])
    write_json(out_paths["meta"],  data["meta"])

    log(f"Challenge: {data['meta']['function_name']}() — {data['meta']['difficulty']}", "success")
    return out_paths


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Auto Quality Check
# Input:  all lesson files
# Output: content/{module_slug}/{lesson_slug}/quality_report.json
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_4 = """
You are quality-checking an AI engineering lesson before human QA.

LESSON PLAN (intended design):
{lesson_plan}

LESSON BEATS (generated):
{beats}

CHALLENGE CODE:
{challenge}

TEST SUITE:
{tests}

---

Check against this rubric. For each item return PASS, FAIL, or WARN.

STRUCTURE:
- S1: First beat is DEMO
- S2: Second beat is HOOK
- S3: Last beat is CHECKPOINT with exactly 3 questions
- S4: CONCEPT beat precedes any code that uses it
- S5: At least 1 SOCRATIC beat
- S6: At least 1 GOTCHA beat
- S7: Beat count between 8 and 12
- S8: No text block exceeds 120 words

CONTENT:
- C1: Primary question from lesson plan is answered by end of lesson
- C2: what_gets_built is achievable via the challenge
- C3: No unexplained jargon (term used before it's defined)
- C4: ANALOGY beats have where_it_breaks populated
- C5: CHECKPOINT tests understanding, not memorisation
- C6: DIAGRAM descriptions are specific and generatable (not vague)

CODE:
- K1: challenge.py has a clear # YOUR CODE HERE comment
- K2: test_suite.py uses pytest and has at least 3 tests
- K3: solution.py is not referenced in challenge.py or test_suite.py
- K4: No external API calls without mocking in tests
- K5: Challenge is scoped to ONE function or class

Return a JSON object:
{{
  "overall": "PASS | FAIL | WARN",
  "checks": [
    {{ "id": "S1", "status": "PASS|FAIL|WARN", "detail": "null or specific issue" }}
  ],
  "blocking_issues": ["..."],
  "warnings": ["..."],
  "auto_fixable": ["issues that could be fixed by re-prompting without full regeneration"]
}}

Output ONLY the JSON. No prose.
""".strip()


def run_step_4(
    module_slug: str,
    lesson: dict,
    force: bool = False,
) -> Path:
    log_step("4", f"Quality Check — {lesson['title']}")

    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    l_dir = lesson_dir(module_slug, l_slug)
    out_path = l_dir / FILES["quality_report"]

    if step_done(out_path, force):
        return out_path

    # Load lesson files
    lesson_path = l_dir / FILES["lesson"]
    challenge_path = l_dir / FILES["challenge"]
    tests_path = l_dir / FILES["tests"]

    missing = [p for p in [lesson_path, challenge_path, tests_path] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing files for quality check: {[p.name for p in missing]}")

    lesson_content = read(lesson_path)
    challenge = read(challenge_path)
    tests = read(tests_path)

    # Extract beats from MDX
    import re
    beats_match = re.search(r"export const beats = (\[[\s\S]+\])", lesson_content)
    beats_str = beats_match.group(1) if beats_match else "[]"

    log(f"Running quality check on: {lesson['title']}")

    prompt = PROMPT_4.format(
        lesson_plan=json.dumps(lesson, indent=2),
        beats=beats_str,
        challenge=challenge[:3000],  # truncate if massive
        tests=tests[:2000],
    )

    system = "You are a strict curriculum QA engineer. Be thorough. Flag anything that would confuse a learner. Output only valid JSON."

    data = call_claude_json(prompt, system=system)

    write_json(out_path, data)

    # Print summary
    overall = data.get("overall", "UNKNOWN")
    blocking = data.get("blocking_issues", [])
    warnings = data.get("warnings", [])

    if overall == "PASS":
        log(f"Quality check: PASS ✓", "success")
    elif overall == "WARN":
        log(f"Quality check: WARN — {len(warnings)} warnings", "warn")
        for w in warnings:
            log(f"  ⚠ {w}", "warn")
    else:
        log(f"Quality check: FAIL — {len(blocking)} blocking issues", "error")
        for b in blocking:
            log(f"  ✗ {b}", "error")

    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# Meta.json writer — combines all step outputs into lesson metadata
# ─────────────────────────────────────────────────────────────────────────────

def write_meta(
    module_slug: str,
    lesson: dict,
    module_type: str,
    runs_in_browser: bool,
    prereq_module_slugs: list[str] = None,
) -> Path:
    l_slug = lesson_slug(lesson["lesson_number"], lesson["title"])
    l_dir = lesson_dir(module_slug, l_slug)
    out_path = l_dir / FILES["meta"]

    # Load challenge meta if it exists
    challenge_meta_path = l_dir / FILES["challenge_meta"]
    challenge_meta = read_json(challenge_meta_path) if challenge_meta_path.exists() else {}

    module_number = module_slug.split("-")[1] if "-" in module_slug else "00"
    lesson_id = f"m{module_number}-l{lesson['lesson_number']:02d}"

    meta = {
        "id": lesson_id,
        "module_slug": module_slug,
        "lesson_number": lesson["lesson_number"],
        "lesson_slug": l_slug,
        "title": lesson["title"],
        "concept": lesson["concept"],
        "primary_question": lesson["primary_question"],
        "what_gets_built": lesson["what_gets_built"],
        "xp_reward": lesson.get("xp_reward", 120),
        "estimated_minutes": lesson.get("estimated_minutes", 35),
        "lesson_type": lesson.get("lesson_type", "BALANCED"),
        "module_type": module_type,
        "last_researched": datetime.now().strftime("%Y-%m-%d"),
        "prereqs": [
            f"m{module_number}-l{n:02d}"
            for n in lesson.get("depends_on", [])
        ],
        "concepts_introduced": [lesson["concept"]],
        "challenge": {
            "function_name": challenge_meta.get("function_name", ""),
            "difficulty": challenge_meta.get("difficulty", "GUIDED"),
            "time_estimate_minutes": challenge_meta.get("time_estimate_minutes", 12),
            "runs_in_browser": runs_in_browser,
        },
        "status": "draft",
        "generated_at": datetime.now().isoformat(),
    }

    write_json(out_path, meta)
    return out_path
