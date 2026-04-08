# context-engineering

A small Claude Code skill collection for designing agent harnesses and writing implementation-ready execution plans.

## What's inside

This repo currently includes two skills:

- **`context-engineering/`** — distills battle-tested context engineering principles for building agent harnesses and skill suites
- **`exec-plan/`** — teaches agents how to write and maintain self-contained execution plans that can be followed from design through implementation

### `context-engineering`

This skill distills two primary sources:

- **OpenAI's Harness Engineering principles** — how to structure agents so humans steer and agents execute (maps over manuals, progressive disclosure, architecture invariants, garbage collection loops, human abstraction + agentic throughput)
- **Manus' Context Engineering principles** — production-grade lessons from a large-scale AI agent system (KV-cache optimization, filesystem as memory, attention manipulation via recitation, keeping failures in context)

### `exec-plan`

This skill focuses on writing and using an `ExecPlan`: a living, self-contained implementation spec that a coding agent or human can follow without hidden context.

It emphasizes:

- clear user-visible outcomes and validation steps
- repository-specific orientation for novices
- living sections such as `Progress`, `Decision Log`, and `Surprises & Discoveries`
- milestone-driven delivery with proof, not just code changes

## Installation

Copy either or both skill directories into your Claude Code skills folder:

```bash
cp -r context-engineering ~/.claude/skills/
cp -r exec-plan ~/.claude/skills/
```

## Usage

Invoke the skill you want in any Claude Code session:

```
/context-engineering
/exec-plan
```

Claude will load the relevant guidance and apply it while reasoning.

## When to use `context-engineering`

- Designing a new agent harness or skill suite
- Reviewing context management strategy for an existing agent system
- Deciding how to structure tools, plans, memory, and multi-agent coordination
- Debugging agent drift, repetition, or goal-forgetting behavior

## When to use `exec-plan`

- Planning a complex feature before implementation
- Writing a spec for a substantial refactor or migration
- Turning an ambiguous request into a concrete, testable execution document
- Keeping implementation progress and design decisions in one living artifact

## How they fit together

Use `context-engineering` to shape the harness, memory model, and operating principles for agentic systems.

Use `exec-plan` when the work is large enough that the agent should first produce or maintain a detailed execution plan with milestones, validation steps, and progress tracking.

## Sources

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [OpenAI Cookbook: Codex Exec Plans](https://developers.openai.com/cookbook/articles/codex_exec_plans)
