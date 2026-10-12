import json
import pytest

from remediation.engine import plan_action, write_audit_record


def test_remediation_requires_approval():
    result = plan_action("restart_worker")
    assert result["status"] == "BLOCKED"
    assert result["executed"] is not True


def test_allowlisted_action_never_executes_implicitly():
    result = plan_action("rollback_api", approved=True)
    assert result["status"] == "AUTHORIZED_FOR_EXECUTION"
    assert result["executed"] is False


def test_unknown_action_is_rejected():
    with pytest.raises(ValueError):
        plan_action("delete_database", approved=True)


def test_audit_record_is_written(tmp_path):
    path = tmp_path / "audit.jsonl"
    write_audit_record({"action": "restart_worker", "status": "BLOCKED"}, path)
    entry = json.loads(path.read_text().strip())
    assert entry["action"] == "restart_worker"
    assert "timestamp" in entry
