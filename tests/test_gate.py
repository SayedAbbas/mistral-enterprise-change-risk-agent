from evals.evaluate import release_gate

def test_high_risk_change_escalates():
    evidence={"change":{"schema_change":True,"backward_compatible":False},"rollback":{"rollback_tested":False},"monitoring":{"error_rate_pct":2.8,"baseline_error_rate_pct":0.4},"incidents":[{"severity":"SEV-1"}]}
    assert release_gate(evidence)["gate"]=="ESCALATE"
