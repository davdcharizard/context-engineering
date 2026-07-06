# context-engineering

A small Claude Code skill collection for designing agent harnesses.

## What's inside

This repo currently includes these skills:

- **`context-engineering/`** — distills battle-tested context engineering principles for building agent harnesses and skill suites
- **`autoresearch-linter/`** — lints an autoresearch skill suite for common design violations
- **`token-counter/`** — counts Claude input tokens for a file or directory via the token counting API, to spot bloated skills or budget prompts

### `context-engineering`

This skill distills two primary sources:

- **OpenAI's Harness Engineering principles** — how to structure agents so humans steer and agents execute (maps over manuals, progressive disclosure, architecture invariants, garbage collection loops, human abstraction + agentic throughput)
- **Manus' Context Engineering principles** — production-grade lessons from a large-scale AI agent system (KV-cache optimization, filesystem as memory, attention manipulation via recitation, keeping failures in context)

## Installation

Copy any skill directory into your Claude Code skills folder:

```bash
cp -r context-engineering ~/.claude/skills/
cp -r autoresearch-linter ~/.claude/skills/
cp -r token-counter ~/.claude/skills/
```

The `token-counter` skill additionally needs `pip install anthropic` and `ANTHROPIC_API_KEY` in the environment.

## Usage

Invoke the skill you want in any Claude Code session:

```
/context-engineering
/autoresearch-linter
/token-counter
```

Claude will load the relevant guidance and apply it while reasoning.

## When to use `context-engineering`

- Designing a new agent harness or skill suite
- Reviewing context management strategy for an existing agent system
- Deciding how to structure tools, plans, memory, and multi-agent coordination
- Debugging agent drift, repetition, or goal-forgetting behavior

## Sources

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
