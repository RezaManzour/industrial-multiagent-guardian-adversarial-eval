# Findings Log (running notes, informal - RESULTS.md will be the polished version)

## Finding 1: Planner allocation choice is non-deterministic across orders

The Planner Agent proposes an allocation for each order independently,
in a single LLM call per order, with no visibility into allocations
already proposed for other orders in the same run (see
`vendored/guardian/graph.py::planner_agent` - the prompt only includes
static machine info, not `proposed_allocations`).

Consequence: with capacity=1 machines and multiple orders that could
fit on more than one machine, the Planner can (non-deterministically,
depending on the LLM's per-call choice) propose the same machine for
two orders that then collide. The Guardrail correctly rejects the
second conflicting proposal - this is a **utility** loss (an order
that could have been scheduled wasn't), not a **security** failure
(no invalid allocation was ever approved).

This is a useful data point for the final report: it demonstrates the
utility/security distinction in practice, and supports the argument for
the rule-based Guardrail design (utility can degrade due to LLM
unpredictability, but the safety boundary held).

Baseline scenario (`basic_two_orders`) uses capacity=2 machines
specifically to remove this non-determinism, since its purpose is an
end-to-end sanity check, not exercising this behavior.
