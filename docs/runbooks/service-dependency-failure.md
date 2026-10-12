# Service Dependency Failure Runbook

## Purpose
Respond to suspected PostgreSQL, Redis, or worker availability failures.

## Triage
1. Check API `/health` and `/ready` separately.
2. Inspect API, worker, PostgreSQL, and Redis logs.
3. Check Kubernetes pod readiness, restart counts, and recent events.
4. Check Prometheus target health, error rate, and latency.
5. Identify the affected dependency before taking action.

## Mitigation
- Do not delete persistent volumes or databases as a first response.
- Restart or roll back only through an approved, documented procedure.
- Verify readiness and successful application requests after mitigation.

## Recovery
1. Confirm dependencies are healthy.
2. Confirm API and worker replicas are ready.
3. Verify metrics and error rates return to normal.
4. Record the timeline, root-cause hypothesis, impact, and follow-up work.

## Safety
Failure scenarios in the local test suite are simulations; they do not inject failures into live infrastructure.
