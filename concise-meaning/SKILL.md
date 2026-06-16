---
name: concise-meaning
description: Use this skill to exemplify what I am looking for when I say keep things "concise".
---

# Principle of Being Concise

One of the key principles for writing effective skills or documentation is being **concise**. This does not mean cut down on content indiscriminately to reduce word count. This means thinking carefully about where words add the most value and information, and where they are redundant or inappropriate for the particular audience.

## Examples

### Feature Documentation

Situation: I asked the agent to add a section in the documentation on how to deploy the pipeline I had built.

There was a particular part that I flagged as violating my principle of conciseness:
```markdown
Review deadlines are anchored to `start_time`, so each cycle's deadlines are pinned
to the calendar (`start_time + committee_review_hours + final_review_hours`),
independent of when the machinery actually ran — the schedule never drifts. Cycles
never overlap: if a cycle is still in review when the next is due, the next **waits**
and starts as soon as the prior finishes (its deadlines stay anchored to its
scheduled start). So `committee_review_hours + final_review_hours` may go right up to
the gap between cycle days (e.g. 24 + 24 on Tue/Thu); `config-check` only rejects a
sum that *exceeds* the gap.

Validate the numbers: `python -m persona_agent.cli config-check`
(it echoes the resolved schedule, the smallest gap, the cycle-end, the poll interval,
and whether account tracking is on).
```

Analysis: The reader is likely a user who only wants to know what config to change, what exact commands to run so that the pipeline is up and running. However, this paragraph starts to explain details that are not helpful to the user, with the risk of adding confusion. For instance the paragraph references low level implementation detail such as anchoring of the cycle to the scheduled start time rather than the actual start time. This was designed to address certain edge cases so that the pipeline is robust. But this should not be in the documentation because 1) the user does not care about these edge cases 2) it's low level detail that does not help them navigate the process of running the pipeline (the primary goal of the section). his should be entirely removed. In the same vein the line "validate the numbers" also appears redundant - it could be cut down to "To validate the config state, run `python -m persona_agent.cli config-check`". The parenthesis does not add any value (again unnecessary detail the user will simply want to gloss over).