---
name: concise-meaning
description: Use this skill to exemplify what I am looking for when I say keep things "concise".
---

# Principle of Being Concise

One of the key principles for writing effective skills or documentation is being **concise**. This does not mean cut down on content indiscriminately to reduce word count. This means thinking carefully about where words add the most value and information, and where they are redundant or inappropriate for the particular audience.

## Examples

### Feature Documentation

**Situation:** I asked the agent to add a section in the documentation on how to deploy the pipeline I had built.

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

**Analysis:** The reader is likely a user who only wants to know what config to change, what exact commands to run so that the pipeline is up and running. However, this paragraph starts to explain details that are not helpful to the user, with the risk of adding confusion. For instance the paragraph references low level implementation detail such as anchoring of the cycle to the scheduled start time rather than the actual start time. This was designed to address certain edge cases so that the pipeline is robust. But this should not be in the documentation because 1) the user does not care about these edge cases 2) it's low level detail that does not help them navigate the process of running the pipeline (the primary goal of the section). his should be entirely removed. In the same vein the line "validate the numbers" also appears redundant - it could be cut down to "To validate the config state, run `python -m persona_agent.cli config-check`". The parenthesis does not add any value (again unnecessary detail the user will simply want to gloss over).

### Safe Shutdown Instructions

**Situation:** I asked the agent to add a section in the user documentation on how to shut down the pipeline gracefuly.

This following section was written by the agent:
**Graceful shutdown (for bug fixes)**

```bash
python -m persona_agent.cli daemon logs -f    # check what it's doing
python -m persona_agent.cli daemon stop       # stop (won't auto-restart)
# ...make your fixes...
python -m persona_agent.cli daemon restart    # resumes where it left off
```

Stop any time — it's safe. A cycle either completes or leaves no trace: an
interrupted ingest/filter persists nothing, and an interrupted review-round close
stays open and retries on the next tick. The DB is never left half-finished, so
no data is lost. Use `daemon stop` rather than `kill` (a raw `kill` is
auto-restarted). On `restart`, open rounds and scheduled cycles pick up where
they left off.

**Analysis:** This section can be made more concise because a lot of it is self explanatory. The key detail is all in the three bash command lines and their comments. Hence the paragraph below does not need a long winding retelling of their exact purpose and mechanism. For instance, I would get rid of the part about what happens with an interrupted review round and data persistence, as users would expect this kind of feature for any kind of "graceful shutdown".

Here's how I would fix it:

**Graceful Shutdown:**

```bash
python -m persona_agent.cli daemon logs -f    # check what it's doing
python -m persona_agent.cli daemon stop       # stop (won't auto-restart)
# ...make your fixes...
python -m persona_agent.cli daemon restart    # resumes where it left off
```

Stop any time for debugging using these commands. The system is explicitly designed for graceful shutdown, so the DB will not be affected. On restart the pipeline will continue where it last left off and `settings.yaml` changes take effect.