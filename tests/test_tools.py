from agent.change_risk_agent import collect_evidence, deterministic_guardrails
from tools.evidence import get_change_request
def test_change_exists(): assert get_change_request("CHG-4821")["service"]=="payment-authentication"
def test_high_risk_policy_forces_review():
    policy=deterministic_guardrails(collect_evidence("CHG-4821"))
    assert policy["force_human_review"] is True
    assert len(policy["reasons"])>=3
