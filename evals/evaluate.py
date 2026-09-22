import json
from pathlib import Path
from agent.change_risk_agent import assess_change
ORDER={"LOW":0,"MEDIUM":1,"HIGH":2,"CRITICAL":3}
def run():
    cases=json.loads((Path(__file__).parent/"eval_dataset.json").read_text()); passed=0
    for c in cases:
        r,_,_=assess_change(c["change_id"]); refs={x["evidence_id"] for x in r.get("evidence",[])}
        ok=ORDER.get(r.get("risk_level"),-1)>=ORDER[c["expected_min_risk"]] and r.get("requires_human_approval") is c["must_require_human_approval"] and set(c["required_evidence"]).issubset(refs)
        print(c["change_id"],"PASS" if ok else "FAIL"); passed+=int(ok)
    print(f"{passed}/{len(cases)} passed")
    raise SystemExit(0 if passed==len(cases) else 1)
if __name__=="__main__": run()
