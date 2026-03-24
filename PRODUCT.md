# Forge

### The AI Engineering Learning Path

---

## What Is This

Forge is a self-paced learning platform that takes a fullstack developer to a production AI engineer — through hands-on projects, not lectures.

Every concept is introduced the moment a real project needs it. Every lesson ends with something working. Every project ships with tests that measure whether it actually works.

The platform is being built by someone learning AI engineering while building it. The curriculum teaches you to build the platform. The platform teaches you the curriculum. It feeds itself.

---

## The Problem

Most AI learning fails in one of three ways:

**Too abstract.** You learn what embeddings are but never build anything with them. The knowledge evaporates in two weeks.

**Too shallow.** You finish a tutorial that holds your hand through a demo. When you try to build something real, you're lost.

**No feedback loop.** You don't know if you're actually getting better. There are no tests, no evals, no measure of progress beyond "I watched the video."

The existing options:

| Option               | Problem                                                       |
| -------------------- | ------------------------------------------------------------- |
| YouTube tutorials    | Passive. No challenge. Forgotten immediately.                 |
| Udemy / Coursera     | Mostly outdated. Certificate means nothing. No real projects. |
| Boot.dev             | Great model, not AI-focused                                   |
| Official docs        | No structure, no path, no projects                            |
| Just building things | No guidance, high frustration, no curriculum                  |

There is no platform that takes a working developer — someone who can already ship software — and turns them into someone who can build and deploy real AI systems. Forge is that.

---

## Who This Is For

**One person:** A confident fullstack developer who has zero AI background and wants to become an AI engineer.

They can already build web apps, write APIs, work with databases. They are not a beginner to software. They are a beginner to AI. They want to fix that systematically, not by watching videos, but by building real things.

They are allergic to:

- Hand-waving ("the model just figures it out")
- Toy examples that don't translate to production
- Courses that teach tools instead of principles
- Certificates that nobody cares about

They want:

- To understand AI from first principles
- To ship real projects they can show people
- To know when they're making progress
- To not waste time on things that will be outdated in six months

---

## The Core Bet

**Project-first learning is faster and stickier than concept-first learning.**

The standard approach: teach the concept, then show an example, then maybe a small exercise.

Forge's approach: show the finished project running first. Then build it layer by layer. Concepts are introduced at the exact moment the project needs them — not as future context, not as prerequisites, but as the answer to a problem the learner is currently experiencing.

The result: every concept you learn is immediately load-bearing. You can't forget it because you just wired it into something that works.

---

## What Gets Built

Forge is a single linear path — 13 modules, one project per module, 134 lessons total.

You don't pick electives. You don't jump around. The order is the curriculum. Every module builds on the last.

### The 13 Projects

| #   | Module                        | Project                                                                                                                |
| --- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | How LLMs Actually Work        | LLM Internals Playground — interactive app: live tokenizer, attention heatmap, sampling distribution, model comparator |
| 2   | AI Agents From Zero           | Autonomous Deep Research Agent — give it a topic, get a fully cited research report                                    |
| 3   | Agent Evals                   | Universal Eval Suite — reusable test harness attached to every project from here forward                               |
| 4   | Prompt Engineering            | Automatic Prompt Optimization Engine — takes a broken prompt, generates variants, scores them, returns a leaderboard   |
| 5   | RAG From Scratch              | Personal Second Brain — RAG over your entire knowledge base with hybrid search and agentic retrieval                   |
| 6   | Tools & Function Calling      | Mini Jarvis — one agent that controls web search, Gmail, Calendar, file system, browser via natural language           |
| 7   | Running AI Locally            | Private AI Workstation — fully self-hosted AI server, zero cloud, multiple models, benchmark dashboard                 |
| 8   | Agent Memory Systems          | AI Life Coach — agent with four-layer persistent memory: episodic, semantic, procedural, in-context                    |
| 9   | Multi-Agent Systems           | Startup Intelligence Firm — multi-agent system that produces investor-grade 10-page company research reports           |
| 10  | Vector Databases              | Universal Semantic Search Engine — 200K+ documents across five vector DB backends with live comparison dashboard       |
| 11  | Model Quantization            | Model Deployment Pipeline — HuggingFace model in, optimised Ollama endpoint out, automated                             |
| 12  | Production AI Systems         | Production AI API — streaming, semantic cache, model router, observability, eval CI, multi-tenancy                     |
| 13  | AI for Your Codebase _(Paid)_ | AI Engineering Workbench — AST-aware code search, PR reviewer, test writer, refactoring agent for your actual repo     |

Every project after Module 3 ships with a working eval suite. Module 13 requires every prior capstone — it is the proof you completed the curriculum.

---

## How the Platform Works

### Lesson Structure

Every lesson is a sequence of 8–12 **beats**. A beat is one interactive unit — you move through them sequentially. There is no scrolling through a wall of text.

| Beat Type    | What It Does                                                                                 |
| ------------ | -------------------------------------------------------------------------------------------- |
| `DEMO`       | Always first. You see the finished thing before writing a line.                              |
| `HOOK`       | Why this concept matters right now. What breaks without it.                                  |
| `CONCEPT`    | One idea explained from first principles. Max 120 words.                                     |
| `DIAGRAM`    | An inline SVG. The thing drawn, not described.                                               |
| `SOCRATIC`   | A question appears. You think. You click to reveal. No grade — just forced recall.           |
| `CODE_READ`  | Annotated code in the right pane. You read it, annotations explain each part.                |
| `GOTCHA`     | A warning card. The exact mistake most people make here and how to avoid it.                 |
| `ANALOGY`    | One analogy, always collapsed by default. Includes where it breaks down.                     |
| `CHECKPOINT` | Three questions. Must pass to unlock the next lesson. Tests understanding, not memorisation. |

Every lesson has a code challenge. You implement one real function from the project — not a toy exercise, the actual function. Tests run automatically. You must pass to continue.

### The Split Pane

The UI is two panes. Left: the lesson narrative — beats in sequence. Right: code, always present, updates as you progress. The design is deliberately minimal — monospace code, generous whitespace, no decorative elements. The XP and badges are elsewhere. Inside a lesson, it is just you and the material.

### Gamification

Progress is tracked and made visible — not to manufacture fake motivation but because knowing where you are on a long path matters.

**XP** is earned by completing lessons, passing challenges, and shipping capstones. It fills a level bar. Levels have real titles that map to real skills: _Agent Apprentice_ at Level 5, _RAG Builder_ at Level 8, _Production Engineer_ at Level 15. You cannot buy them.

**Streaks** track daily activity. One lesson or challenge per day keeps the streak alive. Streak freezes can be earned (not bought) by maintaining a 30-day streak.

**Achievements** are permanent badges earned by doing specific things: building your first agent loop, shipping a capstone with a passing eval suite, running a full agent with zero cloud API calls. They cannot be purchased.

**Capstone Showcase** — every finished capstone can be submitted publicly. Community reactions. GitHub link. A `SHIPPED` tag on your profile. These are portfolio pieces, not homework.

---

## How the Content Is Generated

This is the part that makes Forge different to build and maintain.

### The Problem With Writing 134 Lessons By Hand

Writing high-quality technical lessons takes time. More importantly — the person building this platform is learning AI engineering while building it. They cannot write authoritative lessons on topics they haven't mastered yet.

The solution: **AI generates the content. The builder QAs it by doing it.**

### The Pipeline

Every lesson is produced by a six-step AI pipeline. Zero human writing. The only human input is a module title and a capstone description.

```
MODULE TITLE + CAPSTONE DESCRIPTION
        │
        ▼
STEP 0A — Module Decomposition
Claude reasons about the capstone like a senior engineer:
"What's the minimal working version? What do you add next?
What do you need to understand before you can add it?"
Output: module_plan.json — the lesson-by-lesson breakdown

        │
        ▼
STEP 0B — Source Discovery  (per lesson)
Claude searches for the best primary sources for this concept:
official docs, engineering blogs, seminal papers.
Output: sources.json — ranked, curated reading list

        │
        ▼
STEP 1 — Deep Research  (per lesson)
Claude reads the sources and writes a dense research document:
first principles explanation, mental model, implementation pattern,
common misconceptions, failure modes, production reality.
Output: research.md — the source of truth for this lesson

        │
        ▼
STEP 2 — Lesson Structuring  (per lesson)
Claude converts the research into a structured beat sequence.
Rules are enforced: DEMO first, CONCEPT before CODE_READ,
max 120 words per text beat, at least one SOCRATIC, one GOTCHA.
Output: lesson.mdx — the renderable lesson

        │
        ▼
STEP 3 — Challenge Generation  (per lesson)
Claude writes the code challenge: starter code with clear
TODO markers, pytest test suite (happy path + edge case + failure),
three escalating hints, and a reference solution never shown to the learner.
Output: challenge.py, test_suite.py, hints.json, solution.py

        │
        ▼
STEP 4 — Auto Quality Check  (per lesson)
Claude checks the lesson against a strict rubric:
structure rules, content rules, code correctness rules.
Produces a quality report with PASS / WARN / FAIL per check.
Output: quality_report.json

        │
        ▼
REFINE (if FAIL)
The pipeline reads the failing checks, injects them back
into Steps 2+3 as explicit instructions, reruns automatically.
Loops until quality check passes. No human involvement.

        │
        ▼
STEP 5 — YOU (QA by doing)
The only human step. You do the lesson as a learner would.
You do the code challenge with no help.
Where you get stuck = the lesson is unclear. Fix it.
Where you breeze through = the challenge is too easy. Fix it.
Output: qa_log.md — your notes, fed back into a targeted fix run
```

### Why This Works

The builder's lack of prior knowledge is not a liability — it is the qualification. The best QA for a beginner-to-engineer curriculum is someone with zero priors who has to do every lesson themselves before it ships. Every bug they hit in the challenge, every concept they had to re-read — that is signal no automated check can produce.

The pipeline generates. The builder learns. The output is a lesson that has been built by AI and validated by a human who just learned the material for the first time.

### The Numbers

| Step               | Who Does It | Time Per Lesson          |
| ------------------ | ----------- | ------------------------ |
| 0A (module plan)   | Claude      | ~45 sec, once per module |
| 0B (sources)       | Claude      | ~30 sec                  |
| 1 (research)       | Claude      | ~45 sec                  |
| 2 (structuring)    | Claude      | ~60 sec                  |
| 3 (challenge)      | Claude      | ~45 sec                  |
| 4 (quality check)  | Claude      | ~30 sec                  |
| Refine (if needed) | Claude      | ~2 min per loop          |
| 5 (QA)             | You         | ~45–60 min               |

**Cost:** ~$0.10 per lesson in API credits. ~$15 for the entire curriculum.  
**Time:** ~1 hour of human time per lesson. ~130 hours total = the time it takes to become an AI engineer.

The 130 hours of QA is the learning. That is the point.

### Content Updates

Modules are tagged `EVERGREEN` (foundational, doesn't change) or `CURRENT` (framework layer, changes fast). For `CURRENT` modules, the pipeline re-runs from Step 1 whenever a framework ships a breaking change. The `research.md` is the source of truth — updating it cascades automatically through structuring and challenge generation.

---

## Technical Architecture

### The Platform

```
Frontend
  Next.js 16 (App Router)
  Tailwind CSS
  Framer Motion (beat transitions)
  Monaco Editor (in-browser code challenges)

Backend
  PostgreSQL — users, progress, XP, achievements
  Redis — streaks, leaderboard cache, sessions
  E2B — sandboxed Python execution (in-browser challenges, early modules)

AI Features (built using the curriculum itself)
  Hint generation — LLM explains challenge errors contextually
  Community Q&A — RAG over all lesson content
  Progress summaries — personalised weekly recap

Auth        Clerk
Payments    Stripe (Module 13 unlock)
Observability  Langfuse (AI calls) + PostHog (product analytics)
Hosting     Railway or Fly.io
```

### The Content Pipeline

```
Python CLI — runs locally, outputs to /content directory
Anthropic SDK — all generation uses claude-sonnet-4
File format — MDX (lesson beats) + JSON (meta, challenges, reports)
```

The content directory is the source of truth for the platform. The renderer reads from it. The pipeline writes to it. They are decoupled.

### The Meta Layer

Every module in the curriculum corresponds to a feature in the platform:

| Curriculum Module       | Platform Feature Built With It                             |
| ----------------------- | ---------------------------------------------------------- |
| Module 1: LLM Internals | Hint system — LLM explains challenge errors                |
| Module 2: Agents        | Auto-generate lesson quizzes from transcripts              |
| Module 3: Evals         | Automated content quality checks                           |
| Module 4: Prompts       | Optimise hint prompts using the engine you built           |
| Module 5: RAG           | Community Q&A bot — RAG over all lesson content            |
| Module 6: Tools + MCP   | GitHub integration for capstone submissions                |
| Module 7: Local AI      | Self-hosted model option for hint generation               |
| Module 8: Memory        | Personalised recap — remembers what you struggled with     |
| Module 9: Multi-Agent   | Auto-generate new module outlines                          |
| Module 10: Vector DBs   | Semantic search across the full curriculum                 |
| Module 11: Quantization | Run hint LLM on your own hardware                          |
| Module 12: Production   | The full platform backend — auth, caching, observability   |
| Module 13: AI Codebase  | AI assistant that answers questions about Forge's own code |

The platform is built using the skills the curriculum teaches. In the end, the most advanced feature of the platform — an AI assistant that understands the Forge codebase — is the final project of the curriculum itself.

---

## Business Model

### Pricing

| Tier | Price                     | What You Get                                |
| ---- | ------------------------- | ------------------------------------------- |
| Free | $0                        | Modules 1–12, all 124 lessons, all projects |
| Paid | $49 one-time or $15/month | Module 13 — AI for Your Codebase            |

The free curriculum is not a demo. It is the product. Giving away 12 modules creates trust, completion, and an audience that is warm for Module 13.

### Monetisation Timeline

| Phase        | Timeframe   | Source                            | Monthly Revenue |
| ------------ | ----------- | --------------------------------- | --------------- |
| Build        | Month 1–3   | None                              | $0              |
| AdSense      | Month 3–6   | 1K subs, 4K hours                 | $200–500        |
| Sponsorships | Month 6–12  | AI tool companies at 5K–10K users | $3K–8K          |
| Module 13    | Month 10–18 | Paid module                       | $5K–15K         |
| Full-time    | Month 12–18 | All combined                      | $10K–15K+       |

### Why This Niche Monetises Fast

AI tool companies spend heavily on developer education sponsorships: Anthropic, E2B, Qdrant, Weaviate, Pinecone, LangChain. Developer audience CPM is 3–5× higher than general content. Course format converts better than entertainment. Module 13 has a built-in warm audience who just spent 130 hours on the free path.

---

## Principles This Platform Will Never Violate

| Anti-pattern                        | Why it's excluded                                             |
| ----------------------------------- | ------------------------------------------------------------- |
| Certificates you can pay for        | Credentials should mean something                             |
| Skipping prerequisites              | The order is the curriculum. Every module builds on the last. |
| Passive lessons with no challenge   | Every lesson has a code challenge. Always.                    |
| Opt-out leaderboards                | Competition is opt-in only                                    |
| More than one weekly email          | One digest. That's it.                                        |
| Infinite course catalog             | One path. Done well. Not fifty half-finished tracks.          |
| XP for anything other than learning | You cannot grind your way to a high level.                    |

---

## Where Things Stand

The pipeline is built and running. Module 1 is being generated and QA'd.

**Done:**

- Platform documentation (product spec, gamification system, curriculum map)
- Content pipeline spec (all prompts, beat schema, file structure)
- Pipeline CLI — `bootstrap`, `run`, `refine`, `fix`, `module`, `status`
- All 12 modules registered with capstone descriptions
- First lesson generated, quality-checked, refine loop tested

**Next:**

- QA Module 1 Lesson 1 (do it, fill qa_log.md)
- Complete Module 1 generation (lessons 2–10)
- Design lesson renderer (the frontend beat-by-beat UI)
- Build the progress tracker (the core product loop)

---

_134 lessons. 13 projects. One path._  
_Built by someone learning it. For someone starting it._
