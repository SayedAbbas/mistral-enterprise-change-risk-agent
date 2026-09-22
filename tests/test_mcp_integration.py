import asyncio

from agent.orchestrator import TOOLS, collect_via_mcp


def test_mcp_discovers_tools_and_collects_hero_evidence():
    evidence = asyncio.run(collect_via_mcp("CHG-4821"))

    assert evidence["change"]["evidence_id"] == "CHG-4821"
    assert evidence["change"]["service"] == "payment-authentication"
    assert evidence["incidents"][0]["evidence_id"] == "INC-1932"
    assert evidence["dependencies"]["evidence_id"] == "CMDB-PA"
    assert evidence["rollback"]["evidence_id"] == "RB-77"
    assert evidence["monitoring"]["evidence_id"] == "OBS-4821"
    assert evidence["security"]["evidence_id"] == "SEC-4821"
    assert len(TOOLS) == 6
