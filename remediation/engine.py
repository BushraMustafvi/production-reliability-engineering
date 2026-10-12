from datetime import datetime, timezone
import json
from pathlib import Path


ALLOWED_ACTIONS = {
    "restart_worker": {
        "target": "reliability-worker",
        "requires_approval": True,
    },
    "rollback_api": {
        "target": "reliability-api",
        "requires_approval": True,
    },
}


def plan_action(action, approved=False):
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Action not allowlisted: {action}")

    definition = ALLOWED_ACTIONS[action]
    if definition["requires_approval"] and not approved:
        return {
            "status": "BLOCKED",
            "reason": "EXPLICIT_APPROVAL_REQUIRED",
            "action": action,
            "target": definition["target"],
            "executed": False,
        }

    return {
        "status": "AUTHORIZED_FOR_EXECUTION",
        "action": action,
        "target": definition["target"],
        "executed": False,
    }


def write_audit_record(record, path="remediation/audit.jsonl"):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **record,
    }
    audit_path = Path(path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry
