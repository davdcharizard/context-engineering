---
name: autoresearch-linter
description: Explains the principles and common mistakes to avoid for effective autoresearch design and implementation. Use to check whether the autoresearch skills suite adheres to the guidelines and to address any gaps if necessary.
---

Below are the important principles for designing and writing strong autoresearch skills. Most of these were codified because they were violated consistently.

## Linting Instruction

Using the principles and common mistakes below, scan through the autoresearch skill markdowns, templates, references, and READMEs. Look carefully for ANY AND ALL VIOLATIONS of the principles below and presence of common mistakes. Once the comprehensive scan has been performed and violations and mistakes identified, present them concisely to the user in a list ranked by Low, Medium, to High importance violations, and clear pointers to where they occur in the autoresearch repo. DO NOT MAKE ANY MODIFICATIONS until the user approves or decides which is worth addressing. Having the user review and confirm gaps in the repository is critical to prevent acting on false positives.

### Context management

- **Progressive disclosure.** Give the agent a map, not a dense manual. Agents should be given a small entry point and shown where to look next. This way agents can choose to retrieve more context when it is needed, rather than etting a full context dump at every stage. For example, the agent starts from some MAP.md, navigates to the relevant markdown, and loads details on demand. Again, avoid upfront context dumps in any one file.
- **Filesystem as external memory.** Detailed information (e.g. a goal or learnings markdown or a knowledge base folder) lives on disk and their content is loaded only when relevant.
- **Maintain pointers to all referenced information.** Preserve pointers when distilling or summarizing info to a markdown — never delete a source path/URL even if the content is compressed. This helps during debugging agent output to be able to verify whether the piece of information (e.g. a value or metric) was hallucinated.
- **Single source of truth.** Every fact lives in exactly one canonical reference file, and responsibility for maintaining a specific source of information (e.g. a plan or document) should be as self-contained as possible within one skill rather than spread across multiple skills. This avoids adding multiple points of failure, and avoids the issue of performance degradation when making the agent coordinate long multi-step tasks across multiple skills. When the same information is needed between multiple skills, prefer pointers to one canonical document rather than having them each maintain their separate copy of that information. When the same fact appears in two places, the files drift and staleness becomes a failure mode.

### Framework Design

- **Trust the agent — use inversion of control** Assume that the agent has good decision-making ability within a clear framework. Hence give it a general framework when possible, and let it figure out edge cases. Avoid dense IF/THEN conditional trees, enumerated defensive fallbacks, and "if X then do Y else do Z" branching. Recognize that over fitting to one specific workflow prevents the agent being able to adapt to a wide range of tasks.
- **Offload to deterministic tools for repetitive workflows and high precision tasks** - for high precision tasks that require correctness and repetitive tasks that do not require reasoning, build scripts and tools that the agent calls. For example, instead of asking the agent to monitor a log for a particular completion keyword, give it tools like `Monitor` or a script to execute which can poll the script properly. This saves reasoning tokens and avoids failure cases where an agent may fail to perform a specific action properly.

### Autoresearch skill writing style

- **Minimize informational slash-references.** Only use `/skill-name` when the agent needs to route there (actionable). Do NOT invoke skill names for context ("downstream skills `/research-brainstorm`, `/research-plan` read this"). Phrase informationally as "downstream skills" or "the goal phase". Every slash-reference potentially loads another skill into the agent's context window which pollutes context — reserve mentions only for routing to the specific skill.
- **Don't overfit design vocabulary.** Terms specific to a mental model during the design process ("research loops" vs "infra loops", "baseline experiment") should be followed but not written down literally into the autoresearch skills. The agent cares about the goal, not the designer's taxonomy.
- **One canonical explanation, light mentions elsewhere.** Cross-cutting mechanics (baseline backfill, branch lifecycle, verification ordering) get a single deep explanation in the one skill that executes them, and a one-line reference in any other skill that needs awareness. Don't repeat the full rationale across multiple files, this wastes tokens and adds unnecessary info that can become stale when the referenced skill is changed. (see "Single Source of Truth" principle)
- **Prefer agent-native tools when available** For Claude, skills must ask agents to use the Claude-native `AskUserQuestion` tool to ask the user questions as opposed to natural language instruction. This ensures agents asks the question and blocks.

### Common Mistakes

- **Synthesize, don't split.** When both user and agent contribute (goal candidates, brainstorm ideas), produce a unified output. Never label "user's idea" vs "agent's idea" — the 2-3 final candidates should draw from whatever sources made sense, presented as one set. User input is guidance INTO the process, not a parallel stream.