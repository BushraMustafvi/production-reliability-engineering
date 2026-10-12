import pytest
from chaos.failure_scenarios import evaluate_scenario


@pytest.mark.parametrize(
    "scenario",
    ["database_unavailable", "redis_unavailable", "worker_unavailable"],
)
def test_failure_scenario_is_safe(scenario):
    result = evaluate_scenario(scenario, dependency_healthy=False)
    assert result["status"] == "SIMULATED_FAILURE"
    assert result["live_changes"] is False
    assert result["recommended_action"] == "RAISE_INCIDENT_AND_CHECK_RUNBOOK"


def test_healthy_dependency_does_not_raise_failure():
    result = evaluate_scenario("redis_unavailable", dependency_healthy=True)
    assert result["status"] == "NO_FAILURE_DETECTED"
    assert result["recommended_action"] == "NONE"


def test_unknown_scenario_rejected():
    with pytest.raises(ValueError):
        evaluate_scenario("delete_cluster", dependency_healthy=False)
