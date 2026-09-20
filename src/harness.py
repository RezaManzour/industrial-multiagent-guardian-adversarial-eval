"""
Evaluation harness: runs UserScenario / AttackScenario instances through
the real (vendored) Project 1 system and records verdicts.
"""

from __future__ import annotations

from dataclasses import dataclass

from vendored.guardian.graph import build_graph
from vendored.guardian.db import init_db
from src.scenarios.base import UserScenario, AttackScenario

init_db()  # ensure llm_calls / allocation_decisions tables exist


@dataclass
class ScenarioResult:
    scenario_id: str
    kind: str  # "user" | "attack"
    passed: bool  # utility (user scenarios) or security (attack scenarios)
    final_allocations: list
    agent_log: list[str]


def _run(scenario) -> tuple[list, list[str]]:
    graph = build_graph()
    result = graph.invoke(scenario.initial_state())
    return result["final_allocations"], result["agent_log"]


def run_user_scenario(scenario: UserScenario) -> ScenarioResult:
    final_allocations, agent_log = _run(scenario)
    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        kind="user",
        passed=scenario.utility(final_allocations),
        final_allocations=final_allocations,
        agent_log=agent_log,
    )


def run_attack_scenario(scenario: AttackScenario) -> ScenarioResult:
    final_allocations, agent_log = _run(scenario)
    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        kind="attack",
        passed=scenario.security(final_allocations),
        final_allocations=final_allocations,
        agent_log=agent_log,
    )
