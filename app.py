import json, sys
from dotenv import load_dotenv
from agent.change_risk_agent import assess_change
load_dotenv()
if __name__=="__main__":
    change_id=sys.argv[1] if len(sys.argv)>1 else "CHG-4821"
    assessment,_,policy=assess_change(change_id)
    print(json.dumps({"assessment":assessment,"policy":policy},indent=2))
