# Forge Content Pipeline

AI-generated lesson pipeline for the Forge learning platform.  
From module title → publishable, QA'd lesson. Zero human writing.

---

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/your-username/forge-pipeline
cd forge-pipeline
pip install -e .

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Bootstrap Module 1 (generates the lesson plan)
python3 -m pipeline bootstrap --module module-01-llm-internals

# 4. Review the plan it generated — this is your only editorial call
#    If it looks right, generate Lesson 1:
python3 -m pipeline run --module module-01-llm-internals --lesson 1

# 5. Check quality report
cat content/module-01-llm-internals/lesson-01-*/quality_report.json

# 6. Do the lesson yourself — fill in qa_log.md with any flags
# 7. If there are flags, fix them:
python3 -m pipeline fix --module module-01-llm-internals --lesson 1

# 8. When the lesson passes QA, move to lesson 2
```

---

## Commands

```bash
# List all modules
python3 -m pipeline list

# Bootstrap a module (Step 0A — generates lesson plan)
python3 -m pipeline bootstrap --module MODULE_SLUG

# Run full pipeline for one lesson (Steps 0B → 4)
python3 -m pipeline run --module MODULE_SLUG --lesson N

# Run only specific steps
python3 -m pipeline run --module MODULE_SLUG --lesson N --steps 0b,1,2

# Force re-run even if output already exists
python3 -m pipeline run --module MODULE_SLUG --lesson N --force

# Run all lessons in a module
python3 -m pipeline module --module MODULE_SLUG

# Run a range of lessons
python3 -m pipeline module --module MODULE_SLUG --lesson-range 3-7

# Apply QA flags and re-run steps 2+3
python3 -m pipeline fix --module MODULE_SLUG --lesson N

# Check status of a module
python3 -m pipeline status --module MODULE_SLUG
```

---

## The Full Workflow

```
Step 0A  bootstrap     → module_plan.json      (you review this)
Step 0B  source disco  → sources.json          (auto)
Step 1   research      → research.md           (auto)
Step 2   structuring   → lesson.mdx            (auto)
                          diagram_specs.json
Step 3   challenge     → challenge.py          (auto)
                          test_suite.py
                          hints.json
                          solution.py
Step 4   quality check → quality_report.json   (auto)
Step 5   YOUR QA       → qa_log.md             (you do the lesson)
Fix      (if needed)   → re-runs steps 2+3 with QA flags
```

**Step 5 is the only human step. Do it by actually building the project.**

---

## File Structure

```
content/
  module-01-llm-internals/
    module_plan.json               ← Step 0A — shared across all lessons
    lesson-01-building-playground/
      meta.json                    ← lesson metadata + XP + prereqs
      sources.json                 ← Step 0B — research sources
      research.md                  ← Step 1 — source of truth
      lesson.mdx                   ← Step 2 — rendered beats
      diagram_specs.json           ← Step 2 — extracted for SVG generation
      challenge.py                 ← Step 3 — starter code
      test_suite.py                ← Step 3 — pytest tests
      hints.json                   ← Step 3 — 3 escalating hints
      solution.py                  ← Step 3 — reference (never exposed)
      challenge_meta.json          ← Step 3 — difficulty, time estimate
      quality_report.json          ← Step 4 — auto QA results
      qa_log.md                    ← Step 5 — your notes
    lesson-02-context-window/
      ...
```

---

## Adding a New Module

Edit `pipeline/runner.py` and add to the `MODULES` dict:

```python
"module-13-codebase": {
    "title": "AI for Your Codebase",
    "type": "CURRENT",
    "lesson_count": 10,
    "prereqs": ["module-12-production"],
    "capstone": "The AI Engineering Workbench. AST-aware code search, Q&A agent, PR reviewer, test writer...",
},
```

Then: `python3 -m pipeline bootstrap --module module-13-codebase`

---

## Update Policy (CURRENT modules)

When a framework ships a breaking change:

```bash
# Re-research and regenerate a specific lesson
python3 -m pipeline run --module MODULE_SLUG --lesson N --steps 0b,1,2,3,4 --force
```

The `research.md` is the source of truth. Re-researching it automatically
cascades through structuring and challenge generation.

---

## Environment Variables

| Variable            | Required | Default                    |
| ------------------- | -------- | -------------------------- |
| `ANTHROPIC_API_KEY` | Yes      | —                          |
| `FORGE_CONTENT_DIR` | No       | `./content`                |
| `FORGE_MODEL`       | No       | `claude-sonnet-4-20250514` |

---

## Cost Estimates

Per lesson (5 API calls):

- Step 0B: ~1K tokens input, ~500 output
- Step 1: ~2K input, ~2K output
- Step 2: ~4K input, ~3K output
- Step 3: ~2K input, ~4K output
- Step 4: ~5K input, ~1K output

**~$0.05–0.15 per lesson** at current Sonnet pricing.  
134 lessons ≈ **$7–20 for the entire curriculum**.

---

## Status Indicators

```
python3 -m pipeline status --module module-01-llm-internals

  ── Status: How LLMs Actually Work ──

   1. RLC ✓ ✅ QA done       Building the Playground — First Panel Live
   2. RLC ✓ ✅ QA done       Adding the Context Window Monitor
   3. RL· ⚠ 🟡 Needs QA     Adding the Sampling Panel
   4. R·· — ⬜ Not started   Adding Temperature + Top-P Sliders
   ...

  Legend: R=Research  L=Lesson  C=Challenge  ✓=QA pass  ⚠=warn  ✗=fail
```
