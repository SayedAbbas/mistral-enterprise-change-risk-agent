from agent.evidence import collect
from evals.evaluate import release_gate

def test_citations_present():
    e=collect("CHG-4821")
    assert e["change"]["evidence_id"]=="CHG-4821"
    assert e["incidents"][0]["evidence_id"]=="INC-1932"

def test_low_risk_control_case_passes():
    assert release_gate(collect("CHG-4822"))["gate"]=="PASS"
