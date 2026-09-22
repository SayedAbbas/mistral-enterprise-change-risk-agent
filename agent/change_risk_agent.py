import json, os
from mistralai.client import Mistral
from agent.prompts import SYSTEM_PROMPT
from tools.evidence import get_change_request, search_incidents, get_service_dependencies, get_runbook, get_monitoring_health, get_security_controls

def collect_evidence(change_id):
    change=get_change_request(change_id)
    if not change: raise ValueError(f"Unknown change: {change_id}")
    service=change["service"]
    return {"change":change,"incidents":search_incidents(service),"dependencies":get_service_dependencies(service),"runbook":get_runbook(service),"monitoring":get_monitoring_health(service),"security":get_security_controls(change_id)}

def deterministic_guardrails(e):
    reasons=[]
    if e["change"].get("backward_compatible") is False: reasons.append("Change is not backward compatible")
    if e.get("runbook",{}).get("rollback_validated") is False: reasons.append("Rollback procedure is not validated")
    if e.get("monitoring",{}).get("error_rate_status")=="elevated": reasons.append("Current service error rate is elevated")
    if e.get("security",{}).get("required") and not e["security"].get("approved"): reasons.append("Required security approval is missing")
    return {"force_human_review":bool(reasons),"reasons":reasons}

def assess_change(change_id):
    evidence=collect_evidence(change_id); policy=deterministic_guardrails(evidence)
    client=Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    prompt=f"""Assess this production change using only the evidence below.
Evidence: {json.dumps(evidence)}
Policy: {json.dumps(policy)}
Return JSON with change_id, risk_level (LOW/MEDIUM/HIGH/CRITICAL), confidence, summary, evidence (evidence_id/source/summary), recommended_actions, requires_human_approval. If force_human_review is true, requires_human_approval must be true."""
    response=client.chat.complete(model=os.getenv("MISTRAL_MODEL","mistral-medium-3-5"),messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt}],response_format={"type":"json_object"})
    return json.loads(response.choices[0].message.content), evidence, policy
