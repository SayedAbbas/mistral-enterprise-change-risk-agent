import json, os
from mistralai import Mistral

SYSTEM="""You are an enterprise production-change risk analyst.
Use only supplied evidence. Never invent facts or evidence IDs.
Every material finding must reference evidence_id values from the input.
Return JSON with: risk (LOW|MEDIUM|HIGH|CRITICAL), summary, findings,
mitigations, confidence. Each finding must contain finding, evidence_ids.
The model is advisory. Final production approval always belongs to a human."""

def assess(evidence:dict)->dict:
    client=Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response=client.chat.complete(
        model=os.getenv("MISTRAL_MODEL","mistral-medium-latest"),
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":json.dumps(evidence)}],
        response_format={"type":"json_object"},temperature=0)
    result=json.loads(response.choices[0].message.content)
    valid_ids=set()
    def walk(x):
        if isinstance(x,dict):
            if x.get("evidence_id"): valid_ids.add(x["evidence_id"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(evidence)
    cited={i for finding in result.get("findings",[]) for i in finding.get("evidence_ids",[])}
    result["citation_validation"]={"valid":cited.issubset(valid_ids),"known_evidence_ids":sorted(valid_ids),"cited_evidence_ids":sorted(cited)}
    result["requires_human_approval"]=True
    return result
