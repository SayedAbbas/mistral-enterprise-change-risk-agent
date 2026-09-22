"""Synthetic enterprise evidence with stable citation IDs."""
CHANGES={
"CHG-4821":{"evidence_id":"CHG-4821","service":"payment-authentication","summary":"Upgrade authentication service v4.7 to v5.0","schema_change":True,"backward_compatible":False},
"CHG-4822":{"evidence_id":"CHG-4822","service":"customer-notifications","summary":"Deploy backward-compatible notification patch","schema_change":False,"backward_compatible":True}}
INCIDENTS=[
{"evidence_id":"INC-1932","service":"payment-authentication","severity":"SEV-1","change_related":True,"summary":"Latency increased after schema migration"},
{"evidence_id":"INC-1881","service":"customer-notifications","severity":"SEV-3","change_related":False,"summary":"Provider throttling caused delayed messages"}]
RUNBOOKS={
"payment-authentication":{"evidence_id":"RB-77","rollback_tested":False,"last_review_days":210},
"customer-notifications":{"evidence_id":"RB-91","rollback_tested":True,"last_review_days":14}}
MONITORING={
"payment-authentication":{"evidence_id":"OBS-4821","error_rate_pct":2.8,"baseline_error_rate_pct":0.4,"p95_latency_ms":680},
"customer-notifications":{"evidence_id":"OBS-4822","error_rate_pct":0.3,"baseline_error_rate_pct":0.4,"p95_latency_ms":180}}
DEPENDENCIES={
"payment-authentication":{"evidence_id":"CMDB-PA","criticality":"tier-1","dependencies":["token-service","payments-db"],"downstream":["checkout","recurring-payments"]},
"customer-notifications":{"evidence_id":"CMDB-CN","criticality":"tier-2","dependencies":["message-provider"],"downstream":[]}}
SECURITY={
"CHG-4821":{"evidence_id":"SEC-4821","security_review":"approved","separation_of_duties":True},
"CHG-4822":{"evidence_id":"SEC-4822","security_review":"approved","separation_of_duties":True}}

def collect(change_id:str)->dict:
    c=CHANGES.get(change_id)
    if not c: raise ValueError(f"Unknown change: {change_id}")
    s=c["service"]
    return {"change":c,"incidents":[x for x in INCIDENTS if x["service"]==s],"rollback":RUNBOOKS[s],"monitoring":MONITORING[s],"dependencies":DEPENDENCIES[s],"security":SECURITY[change_id]}
