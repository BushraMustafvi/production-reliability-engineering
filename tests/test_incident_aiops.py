import pytest

from incident_management.lifecycle import IncidentState, transition
from aiops.correlation import correlate_events


def test_incident_lifecycle_progresses():
    state = IncidentState.DETECTED
    for target in (
        IncidentState.TRIAGED,
        IncidentState.INVESTIGATING,
        IncidentState.MITIGATING,
        IncidentState.RECOVERING,
        IncidentState.RESOLVED,
    ):
        state = transition(state, target)
    assert state == IncidentState.RESOLVED


def test_incident_rejects_skipped_state():
    with pytest.raises(ValueError):
        transition(IncidentState.DETECTED, IncidentState.RESOLVED)


def test_correlates_events_by_service():
    result = correlate_events([
        {"service": "api", "signal": "high_latency"},
        {"service": "api", "signal": "high_errors"},
        {"service": "worker", "signal": "queue_growth"},
    ])
    assert result["event_count"] == 3
    assert result["affected_services"] == ["api", "worker"]
    assert result["events_by_service"] == {"api": 2, "worker": 1}
    assert result["correlation_status"] == "OBSERVATIONAL_ONLY"
