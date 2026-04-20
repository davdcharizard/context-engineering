---
name: token-counter
description: Count Claude input tokens for a markdown file or a directory of text files using the Claude token counting API. Use to evaluate whether a SKILL.md or prompt is bloated, compare before/after refactors, or estimate context cost for a skill suite.
---

# Token Counter

Measures how many **input tokens** a file or directory would consume for a given Claude model (e.g. `claude-opus-4-7`, `claude-sonnet-4-6`). Use it to spot bloated skill markdowns, compare prompt versions, or budget context.

The skill ships a helper script `scripts/count_tokens.py` that wraps the Claude [`messages.count_tokens`](https://platform.claude.com/docs/en/build-with-claude/token-counting) endpoint. Prefer running the script over eyeballing length — token counts are deterministic per model and revealed exactly by the API.

## When to use

- Evaluating whether a `SKILL.md`, agent prompt, or plan markdown is too large
- Comparing tokens before/after refactoring a prompt or skill
- Estimating total context cost for a directory of skills, docs, or plans
- Choosing a model based on context budget (Opus vs Sonnet vs Haiku)

## Prerequisites

- `ANTHROPIC_API_KEY` exported in the environment
- `pip install anthropic`

## Usage

Run from the repo root (or pass any path):

    python token-counter/scripts/count_tokens.py <path> [--model MODEL] [--ext .md,.py] [--all]

Flags:

- `--model`  Claude model id. Default `claude-opus-4-7`. Any active model works (e.g. `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`).
- `--ext`    Comma-separated extensions for directory walks. Default `.md,.txt`.
- `--all`    Walk every common text/code/config extension instead of `--ext`.

Examples:

    # Single markdown file, default model
    python token-counter/scripts/count_tokens.py autoresearch-linter/SKILL.md

    # Whole directory, only .md files (default)
    python token-counter/scripts/count_tokens.py context-engineering/

    # Include Python sources too
    python token-counter/scripts/count_tokens.py token-counter/ --ext .md,.py

    # All common text files, against Sonnet
    python token-counter/scripts/count_tokens.py path/to/skill --model claude-sonnet-4-6 --all

Output lists per-file counts plus a `TOTAL` row:

        1,234  SKILL.md
          456  count_tokens.py
    ----------------------
        1,690  TOTAL  (2 files, model=claude-opus-4-7)

## Notes

- The API calls it an **estimate** — the real count at message-creation time may differ slightly.
- One API call per file. Token counting is free but rate-limited per minute (100 RPM on tier 1, higher on upper tiers); large directories may take a few seconds.
- Hidden directories (`.git`, `.venv`, etc.) are skipped during directory walks.
- Binary files are skipped (non-UTF-8 decode errors are logged to stderr).
