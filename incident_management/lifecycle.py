from enum import Enum


class IncidentState(str, Enum):
    DETECTED = "DETECTED"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATING = "MITIGATING"
    RECOVERING = "RECOVERING"
    RESOLVED = "RESOLVED"


TRANSITIONS = {
    IncidentState.DETECTED: {IncidentState.TRIAGED},
    IncidentState.TRIAGED: {IncidentState.INVESTIGATING},
    IncidentState.INVESTIGATING: {IncidentState.MITIGATING},
    IncidentState.MITIGATING: {IncidentState.RECOVERING},
    IncidentState.RECOVERING: {IncidentState.RESOLVED},
    IncidentState.RESOLVED: set(),
}


def transition(current: IncidentState, target: IncidentState) -> IncidentState:
    if target not in TRANSITIONS[current]:
        raise ValueError(f"Invalid incident transition: {current} -> {target}")
    return target
