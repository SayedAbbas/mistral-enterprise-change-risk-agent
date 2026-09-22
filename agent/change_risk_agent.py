import json, os
from mistralai import Mistral

SYSTEM = """You assess enterprise production change risk using supplied enterprise evidence. Never invent evidence. Surface rollback, incident, dependency, health and security risks. Return JSON. Final production approval always belongs to a human."""

def assess(evidence: dict) -> dict:
    client=Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response=client.chat.complete(model=os.getenv("MISTRAL_MODEL","mistral-medium-latest"),messages=[{"role":"system","content":SYSTEM},{"role":"user","content":json.dumps(evidence)}],response_format={"type":"json_object"},temperature=0)
    result=json.loads(response.choices[0].message.content)
    result["requires_human_approval"]=True
    return result
