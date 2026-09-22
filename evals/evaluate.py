def release_gate(evidence: dict) -> dict:
    reasons=[]
    c=evidence["change"]
    if c.get("schema_change") and not c.get("backward_compatible"): reasons.append("non_backward_compatible_schema")
    if not evidence["rollback"].get("rollback_tested"): reasons.append("rollback_not_tested")
    m=evidence["monitoring"]
    if m["error_rate_pct"] > m["baseline_error_rate_pct"]*2: reasons.append("error_rate_above_gate")
    if any(i.get("severity")=="SEV-1" for i in evidence["incidents"]): reasons.append("sev1_history")
    return {"gate":"ESCALATE" if reasons else "PASS","reasons":reasons}
