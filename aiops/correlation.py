from collections import Counter


def correlate_events(events):
    """Summarize related telemetry events without claiming causal proof."""
    counts = Counter(
        str(event.get("service", "unknown"))
        for event in events
    )
    return {
        "event_count": len(events),
        "affected_services": sorted(counts),
        "events_by_service": dict(sorted(counts.items())),
        "correlation_status": "OBSERVATIONAL_ONLY",
    }
