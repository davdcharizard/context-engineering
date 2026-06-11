---
name: harness-engineering
description: Explains most important principles of harness engineering gathered through experience. Use when building skill suites and agent harnesses that manage context and steer agents effectively.
---

## Principles

1. Simplicity trumps complexity in harness design

Complicated agent routing and harness structure tend to lead to poorer performance. Try to start simple before attempting to add additional complexity. The more complex the harness, and the more bells and whistles, the more points of failure for the agent.

Example: instead of an autoresearch loop with 8 phases where agents can move forward and back in the phases, keep the number of phases small and only allow the agent to move in one direction.

2. Offload deterministic processes to mechanical scripts

During long runs as context degrades, agents tend to forget to execute trivial tasks. To avoid risk, always prefer to have these done via scripts than via verbose agent instruction. Offload cleanup tasks and prefer delegating non-trivial non-deterministic tasks for the agent to focus on.

Example: instead of prompting the agent to add the result into a markdown file according to a precise format, build a bash script that the agent calls to insert result into a TSV deterministically.

3. Reduce surface area for context explosion

Context explosion can occur if the agent has unfettered access to files that it continually reads into its context window and adds to over time. Make sure to only give it as small a surface area as needed, so if any corruption happens the context does not spiral out of control, leading to further context explosion. Also prefer to do "doc-gardening" that cleans up stale or obsolete documentation and keeps files manageable to prevent redundant or out-dated info from piling up.

For example: In the autoresearch harness, agents are tasked with keeping records across different files. Reducing the number of files and making certain files read only prevents agents across long runs from corrupting them with long verbose content.

4. Reduce agent self-routing (e.g. If A then B statements), prefer orchestrators and informative error messages instead

Using a "conductor" bash script that reminds the agent which step to take at a particular state is much more effective then leaving the agent to figure out the next step, especially since the precise routing instructions can be forgotten in long context sessions.

Additionally, with harnesses that incorporate skills, a common failure mode is that the agent does not receive feedback that it is drifting from the skill instructions (especially when context rot sets in). Best practice is to place steering correction messages along the agent boundaries that activate when deviation occurs. When agent begins to drift, the correction message steers the agent behavior back onto the right track. The messages should not just tell the agent it did something wrong, but how to correct itself.

This principle complements 5). It is important to enforce the routing via orchestration and informative error messages, while leaving the adaptable "soft tasks" entirely up to the agent. Knowing where this distinction lies is critical to harness performance.

5. Empower agent adaptability

==Agents are much more adaptable and independent than you think.== Instead of explicitly spelling out each possible state or scenario and telling the agents what to do in that scenario, leave it to the agents to adapt. For instance, if the skill contains instructions for the agent to push to a branch and create a PR, instead of adding specific instructions when the `remote` is not available, leave it to the agent. In practice, the agent will adapt and know how to push if the `git remote` is not set.