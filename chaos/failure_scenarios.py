def evaluate_scenario(scenario, dependency_healthy):
    """Evaluate a simulated failure; never changes live infrastructure."""
    known_scenarios = {
        "database_unavailable": "database",
        "redis_unavailable": "redis",
        "worker_unavailable": "worker",
    }
    if scenario not in known_scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")

    dependency = known_scenarios[scenario]
    if dependency_healthy:
        return {
            "scenario": scenario,
            "status": "NO_FAILURE_DETECTED",
            "recommended_action": "NONE",
            "live_changes": False,
        }

    return {
        "scenario": scenario,
        "status": "SIMULATED_FAILURE",
        "recommended_action": "RAISE_INCIDENT_AND_CHECK_RUNBOOK",
        "dependency": dependency,
        "live_changes": False,
    }
