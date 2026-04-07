---
name: context-engineering
description: Explains most important principles of context engineering gathered through experience. Use when building skill suites and agent harnesses that manage context and steer agents effectively.
---

# Context Engineering Principles

## OpenAI Harness Engineering Principles

This is based on principles from OpenAI's Harness Engineering blog post to build systems where **humans steer, agents execute**.

### Principle 1: Give Agents a Map, Not a Manual

> "Give the agent a map, not a dense instructions manual."

**Key Ideas:**
- Use a specific markdown file as a table of contents that points to where structured knowledge resides (e.g. `docs/` directory), not as a monolithic instruction dump
- A short entry point is injected into context as a **map** that tells the agent where to look next

**Plans as First-Class Artifacts:**
- Plans scale from small to large based on complexity
- Principle of **progressive disclosure**: agents start with a small stable entry point and are shown where to look next, rather than being given a context dump
- [Execution plans](https://developers.openai.com/cookbook/articles/codex_exec_plans): self-contained knowledge + plain language instructions, **living documents** to be revised as progress is made, must produce demonstrably working behavior
- Anchor in observable outcomes: What can the user do? What commands to run when implemented? What outputs do you see? → verifiability

### Principle 2: Capture Maximal Context

> "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."

**Key Ideas:**
- Logs, error traces, application UI etc. that are related to the agent's work should all be made directly legible to the agent - i.e. create a "full observability stack"
- Organize and expose the right information for the agent to reason over rather than overwhelming it with ad-hoc instructions, in the same way you onboard a teammate on product principles, engineering norms, team culture for better aligned output
- Knowledge across docs, chat threads, and people's heads needs to be made accessible to the agent — assume anything the agent cannot "see" does not exist. Goal is to expose all important info for the agent
- Consider re-implementing obscure packages so that agents have more visible helpers and tools to use

### Principle 3: Enforce Architecture and Taste Invariants

> "Enforce boundaries centrally, allow autonomy locally."

**Why:** Agents are most effective with clear, consistent, strict boundaries and predictable structure. Enforcing **invariants** keeps the codebase coherent.

**Key Ideas:**
- Constraints are an early pre-requisite that allows for speed without decay or architectural drift
- Be explicit about where constraints matter and where they do not
- Within boundaries you allow agents significant freedom in how solutions are expressed

**Practical Implementation:**
- Rigid architectural constraint where code must meet a forward dependency graph — no circular dependencies
  - Example dependency chain: `Types -> Config -> Repo -> Service -> Runtime -> UI`. This constraint prevents decay and architectural drift
- Enforce using **custom linters and structural tests** plus small set of **taste invariants**
  - Static enforcement of structured logging, naming conventions, file size limits, etc.
  - Custom lint error messages inject remediation instructions directly into agent context

### Principle 4: Garbage Collection for Continuous Codebase Hygiene

**Problem:** Model drift, codebase entropy, too much time spent cleaning up "AI slop."

**Solution:** Pay down technical debt in small continuous intervals using an automated refactoring loop that ensures code adheres to "golden principles."

**Practical Implementation:**
- Recurring **doc-gardening** to maintain the knowledge base — scanning for stale or obsolete docs that no longer reflect real code behaviors, and opening PRs to fix stale docs
- Mechanical rules to keep the codebase legible and consistent for future agent runs:
  - i) Prefer shared utility packages over hand-rolled helpers to keep invariants centralized
  - ii) Don't probe data YOLO style (to prevent guessing)

### Principle 5: Human Abstraction Combined with Agentic Throughput

> "In a system where agent throughput far exceeds human attention, corrections are cheap, and waiting is expensive"

**Key Ideas:**
- In high-throughput environments, remove blockers — fast PRs, minimal waiting time (with some lower quality allowed as long as we allow it to auto-correct)
- **Human remains in loop on higher abstraction while agents code.** Humans work at the higher abstraction layer of translating user feedback into criteria, validating outcomes, and correcting agents where they struggle
  - Scaffolding >>> low-level code (low-level coding can be deferred to agent)
  - Let agents escalate to a human only when judgment is required (e.g. it cannot resolve a problem without human intervention)
- **Treat agent failures as signal of a missing meta aspect of the environment for feedback loop** — when agents fail, encode information into the harness to resolve the gap → key to self-improving feedback loop

---

## The 6 Manus Principles

This is based on context engineering principles from Manus, the AI agent company acquired by Meta for $2 billion in December 2025.

### Principle 1: Design Around KV-Cache

> "KV-cache hit rate is THE single most important metric for production AI agents."

**Statistics:**
- ~100:1 input-to-output token ratio
- Cached tokens: $0.30/MTok vs Uncached: $3/MTok
- 10x cost difference!

**Implementation:**
- Keep prompt prefixes STABLE (single-token change invalidates cache)
- NO timestamps in system prompts
- Make context APPEND-ONLY with deterministic serialization

### Principle 2: Mask, Don't Remove

Don't dynamically remove tools (breaks KV-cache). Use logit masking instead.

**Best Practice:** Use consistent action prefixes (e.g., `browser_`, `shell_`, `file_`) for easier masking.

### Principle 3: Filesystem as External Memory

> "Markdown is my 'working memory' on disk."

**The Formula:**
```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
```

**Compression Must Be Restorable:**
- Keep URLs even if web content is dropped
- Keep file paths when dropping document contents
- Never lose the pointer to full data

### Principle 4: Manipulate Attention Through Recitation

> "Creates and updates todo.md throughout tasks to push global plan into model's recent attention span."

**Problem:** After ~50 tool calls, models forget original goals ("lost in the middle" effect).

**Solution:** Re-read `task_plan.md` before each decision. Goals appear in the attention window.

```
Start of context: [Original goal - far away, forgotten]
...many tool calls...
End of context: [Recently read task_plan.md - gets ATTENTION!]
```

### Principle 5: Keep the Wrong Stuff In

> "Leave the wrong turns in the context."

**Why:**
- Failed actions with stack traces let model implicitly update beliefs
- Reduces mistake repetition
- Error recovery is "one of the clearest signals of TRUE agentic behavior"

### Principle 6: Don't Get Few-Shotted

> "Uniformity breeds fragility."

**Problem:** Repetitive action-observation pairs cause drift and hallucination.

**Solution:** Introduce controlled variation:
- Vary phrasings slightly
- Don't copy-paste patterns blindly
- Recalibrate on repetitive tasks

## The 3 Context Engineering Strategies in Manus

Based on Lance Martin's analysis of Manus architecture.

### Strategy 1: Context Reduction

**Compaction:**
```
Tool calls have TWO representations:
├── FULL: Raw tool content (stored in filesystem)
└── COMPACT: Reference/file path only

RULES:
- Apply compaction to STALE (older) tool results
- Keep RECENT results FULL (to guide next decision)
```

**Summarization:**
- Applied when compaction reaches diminishing returns
- Generated using full tool results
- Creates standardized summary objects

### Strategy 2: Context Isolation (Multi-Agent)

**Architecture:**
```
┌─────────────────────────────────┐
│         PLANNER AGENT           │
│  └─ Assigns tasks to sub-agents │
├─────────────────────────────────┤
│       KNOWLEDGE MANAGER         │
│  └─ Reviews conversations       │
│  └─ Determines filesystem store │
├─────────────────────────────────┤
│      EXECUTOR SUB-AGENTS        │
│  └─ Perform assigned tasks      │
│  └─ Have own context windows    │
└─────────────────────────────────┘
```

**Key Insight:** Manus originally used `todo.md` for task planning but found ~33% of actions were spent updating it. Shifted to dedicated planner agent calling executor sub-agents.

### Strategy 3: Context Offloading

**Tool Design:**
- Use <20 atomic functions total
- Store full results in filesystem, not context
- Use `glob` and `grep` for searching
- Progressive disclosure: load information only as needed

## Manus Design Choices

### Critical Constraints

- **Single-Action Execution:** ONE tool call per turn. No parallel execution.
- **Plan is Required:** Agent must ALWAYS know: goal, current phase, remaining phases
- **Files are Memory:** Context = volatile. Filesystem = persistent.
- **Never Repeat Failures:** If action failed, next action MUST be different
- **Communication is a Tool:** Message types: `info` (progress), `ask` (blocking), `result` (terminal)

### Key Quotes

> "Context window = RAM (volatile, limited). Filesystem = Disk (persistent, unlimited). Anything important gets written to disk."

> "if action_failed: next_action != same_action. Track what you tried. Mutate the approach."

> "Error recovery is one of the clearest signals of TRUE agentic behavior."

> "KV-cache hit rate is the single most important metric for a production-stage AI agent."

> "Leave the wrong turns in the context."

---

## Sources:

The principles were distilled from the following sources:
* [Manus' official context engineering documentation](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
* [OpenAI's report on harness engineering](https://openai.com/index/harness-engineering/)
