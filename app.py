import asyncio, json, os
import streamlit as st
from agent.orchestrator import investigate
from agent.evidence import collect
from evals.evaluate import release_gate

st.set_page_config(page_title="Mistral Change Risk Agent",layout="wide")
st.title("Mistral Enterprise Change Risk Agent")
st.caption("Mistral reasoning • MCP evidence tools • deterministic release gates • human approval")
change_id=st.selectbox("Change request",["CHG-4821","CHG-4822"])
st.info("CHG-4821 is the high-risk hero scenario. CHG-4822 is a lower-risk control case.")
if st.button("Investigate change",type="primary"):
    if not os.getenv("MISTRAL_API_KEY"):
        st.error("Set MISTRAL_API_KEY before running the model.")
    else:
        with st.spinner("Calling enterprise evidence tools through MCP and assessing risk..."):
            result=asyncio.run(investigate(change_id,True))
        a,b=st.columns(2)
        a.metric("Release gate",result["release_gate"]["gate"])
        b.metric("Model risk",result["assessment"].get("risk","N/A"))
        st.subheader("Evidence")
        st.json(result["evidence"])
        st.subheader("Deterministic controls")
        st.json(result["release_gate"])
        st.subheader("Mistral assessment")
        st.json(result["assessment"])
        st.warning("Final production authorization remains with the human change authority.")
