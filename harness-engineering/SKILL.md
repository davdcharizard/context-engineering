---
name: harness-engineering
description: Explains most important principles of harness engineering gathered through experience. Use when building skill suites and agent harnesses that manage context and steer agents effectively.
---

## Principles

### Simplicity and autonomy

1. Simplicity trumps complexity in harness design

Complicated agent routing and harness structure tend to lead to poorer performance. Try to start simple before attempting to add additional complexity. The more complex the harness, and the more bells and whistles, the more points of failure for the agent.

Example: instead of an autoresearch loop with 8 phases where agents can move forward and back in the phases, keep the number of phases small and only allow the agent to move in one direction.

2. Empower agent adaptability

==Agents are much more adaptable and independent than you think.== Instead of explicitly spelling out each possible state or scenario and telling the agents what to do in that scenario, leave it to the agents to adapt. For instance, if the skill contains instructions for the agent to push to a branch and create a PR, instead of adding specific instructions when the `remote` is not available, leave it to the agent. In practice, the agent will adapt and know how to push if the `git remote` is not set.

Example: in the system prompt for a deep codebase subagent tasked with finding optimization opportunities for a specific target metric, instead of the instruction:

```markdown
Surface what a cursory reader misses that may be important and costly: redundant work, unnecessary data movement or serialization, sync/locking points, hidden allocations, blocking I/O, idle parallelism (cores/devices/streams), repeated recomputation.
```

A better system prompt for the harness would be:
```markdown
Surface what a cursory reader misses that may be important and costly with respect to the optimization goal.
```

This prevents the subagent from overfitting to the specific examples listed when they do not fit in the given context or goal. Agents can adapt very well and know what they should be looking for - you do not need to list it all one by one.

### Mechanical enforcement and feedback

3. Offload deterministic processes to mechanical scripts

During long runs as context degrades, agents tend to forget to execute trivial tasks. To avoid risk, always prefer to have these done via scripts than via verbose agent instruction. Offload cleanup tasks and prefer delegating non-trivial non-deterministic tasks for the agent to focus on.

Example: instead of prompting the agent to add the result into a markdown file according to a precise format, build a bash script that the agent calls to insert result into a TSV deterministically.

4. Reduce agent self-routing (e.g. If A then B statements), prefer orchestrators and informative error messages instead

Using a "conductor" bash script that reminds the agent which step to take at a particular state is much more effective then leaving the agent to figure out the next step, especially since the precise routing instructions can be forgotten in long context sessions.

Additionally, with harnesses that incorporate skills, a common failure mode is that the agent does not receive feedback that it is drifting from the skill instructions (especially when context rot sets in). Best practice is to place steering correction messages along the agent boundaries that activate when deviation occurs. When agent begins to drift, the correction message steers the agent behavior back onto the right track. The messages should not just tell the agent it did something wrong, but how to correct itself.

A common form of harmful self-routing written into harness docs is the prescriptive load: `If <condition>, read strategies/X.md`. The condition is extra prompt the agent must parse, the agent loads the file even when the current step doesn't need it, and it never learns to judge when to dig deeper. Write descriptive pointers instead (`Heuristics and edge cases for X: strategies/x.md`) and let the agent decide when to read.

This principle complements 2). It is important to enforce the routing via orchestration and informative error messages, while leaving the adaptable "soft tasks" entirely up to the agent. Knowing where this distinction lies is critical to harness performance.

5. Mechanically verify the harness itself, with corrective feedback on failure

Principle 3 offloads agent work to scripts; this extends it to harness integrity. Any contract that can be checked by a script should be — referenced file paths exist, cross-references resolve, no rule is duplicated. Contracts maintained only by prose reminders will drift, and a broken reference fails silently: the agent hits a missing file mid-run and falls back to guessing or skipping. Per principle 4, a failed check must not just flag the error but tell the agent how to correct it.

Example: a pre-run check that fails with `Pointer skills/report/SKILL.md does not exist — update the pointer or restore the file` rather than letting the agent discover the broken reference mid-run.

### Context management

6. Reduce surface area for context explosion

Context explosion can occur if the agent has unfettered access to files that it continually reads into its context window and adds to over time. Make sure to only give it as small a surface area as needed, so if any corruption happens the context does not spiral out of control, leading to further context explosion. Also prefer to do "doc-gardening" that cleans up stale or obsolete documentation and keeps files manageable to prevent redundant or out-dated info from piling up.

For example: In the autoresearch harness, agents are tasked with keeping records across different files. Reducing the number of files and making certain files read only prevents agents across long runs from corrupting them with long verbose content.

7. Place content where it is loaded — always-loaded context must pay rent

Always-loaded files (CLAUDE.md, system prompts) cost tokens every single turn and dilute the hard rules that actually matter. The decision rule: if the agent only needs a sentence after it loads skill X, the sentence belongs in skill X, not in CLAUDE.md. Keep always-loaded files to the workflow skeleton, cross-cutting contracts, and pointers; offload heuristics and examples to files loaded on demand.

8. Preserve provenance when distilling

When the harness summarizes or compresses information across files or iterations, never drop source paths or URLs. After a couple of rounds of summarization without sources, the agent can no longer distinguish recorded fact from hallucination, and that contamination is irreversible.

Example: require distilled bullets to carry their source (`Evidence: experiments/log-014.md`) so every claim stays traceable.

9. Subagent outputs go to files, not the main context.

A subagent that returns kilobytes of text pollutes the main agent's context for every subsequent turn. Have subagents write results to disk and return a one-line pointer (`Written to results/review.md`); the main agent reads it on demand. When the main agent needs to keep analyzing with tools downstream, prefer a skill or CLI over a subagent. A heavy subagent "steals" the evidence — the main agent receives only a summary and can no longer do its own read-act-analyze loop on the raw data.

10. Design for context death: any fresh agent must be able to resume from files alone

Long-running harnesses will hit compaction, crashes, or session restarts — treat this as a design constraint, not an accident. Persist progress to disk in a form that lets a brand-new agent resume in seconds: the goal, the current state, approaches already tried and failed, and the next step. The failed attempts are the part most often skipped and the most valuable — without them, every resumed session burns time re-walking the same dead ends.

Example: in the autoresearch loop, the current phase is preserved in a canonical state file that agents read, alongside instructions on how to resume that phase. The state is updated mechanically at each phase transition (per principle 3), so there is always an up-to-date checkpoint and a fresh agent resumes exactly where the last one left off.

### Instruction hygiene

11. Single Source of Truth: every rule lives in exactly one place

Duplicated rules drift. When the same hard rule, schema, or baseline is written in CLAUDE.md, a skill, and a subagent prompt, updating one copy and forgetting the others is only a matter of time — and the agent ends up holding contradictory instructions mid-run. Write each rule once in the file that owns it; everywhere else gets a one-line pointer.

Example: instead of repeating the report output schema in both CLAUDE.md and the reporting skill, define it once in the skill and have CLAUDE.md point to it (`Report format: see skills/report/SKILL.md`).

12. Write runtime instructions, not documentation

Harness files are read by the agent at runtime, so every sentence must help it complete the task. Cut version history, changelogs, design rationale ("we do X because the old approach had bug Y"), and negations ("this is not X") — they add context cost and push the agent into reasoning about the past instead of executing. Keep instructions sharp: say what to do, not why the author chose it. Rationale belongs in PR descriptions or external docs.

### Evaluation

13. Calibrate the evaluator before optimizing the agent, and keep it adversarial

If the evaluator cannot distinguish good output from bad, every harness iteration is wasted motion — verify its discrimination first (e.g. confirm it separates a known-good from a known-bad output) before touching the agent. And never let the same agent both produce and grade work: self-evaluation skews confidently positive. Use a separate evaluator explicitly tuned toward skepticism, tasked with finding problems rather than confirming success.
