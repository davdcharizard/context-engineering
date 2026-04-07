# context-engineering

A Claude Code skill that injects battle-tested context engineering principles into your conversation when building agent harnesses and skill suites.

## What's inside

The skill distills two primary sources:

- **OpenAI's Harness Engineering principles** — how to structure agents so humans steer and agents execute (maps over manuals, progressive disclosure, architecture invariants, garbage collection loops, human abstraction + agentic throughput)
- **Manus' Context Engineering principles** — production-grade lessons from a $2B AI agent system (KV-cache optimization, filesystem as memory, attention manipulation via recitation, keeping failures in context)

## Installation

Copy the skill directory into your Claude Code skills folder:

```bash
cp -r context-engineering ~/.claude/skills/
```

## Usage

Invoke it in any Claude Code session:

```
/context-engineering
```

Claude will load the principles and apply them when reasoning about your agent harness design.

## When to use it

- Designing a new agent harness or skill suite
- Reviewing context management strategy for an existing agent system
- Deciding how to structure tools, plans, memory, and multi-agent coordination
- Debugging agent drift, repetition, or goal-forgetting behavior

## Sources

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
