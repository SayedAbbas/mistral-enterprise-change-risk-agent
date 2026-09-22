import json
from pathlib import Path
from agent.evidence import collect
from evals.evaluate import release_gate

def run():
    cases=json.loads((Path(__file__).parent/"cases.json").read_text())
    rows=[]
    for case in cases:
        got=release_gate(collect(case["change_id"]))
        ok=got["gate"]==case["expected_gate"] and all(x in got["reasons"] for x in case["required_reasons"])
        rows.append({"change_id":case["change_id"],"expected":case["expected_gate"],"actual":got["gate"],"pass":ok})
    passed=sum(x["pass"] for x in rows)
    return {"passed":passed,"total":len(rows),"score":passed/len(rows),"results":rows}
if __name__=="__main__": print(json.dumps(run(),indent=2))
