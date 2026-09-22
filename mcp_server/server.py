"""MCP server exposing governed enterprise change evidence tools."""
from mcp.server.fastmcp import FastMCP
from agent.evidence import CHANGES, INCIDENTS, RUNBOOKS, MONITORING, DEPENDENCIES, SECURITY

mcp=FastMCP("enterprise-change-evidence")

@mcp.tool()
def change_request(change_id:str)->dict:
    """Retrieve the authoritative production change record."""
    return CHANGES.get(change_id,{})

@mcp.tool()
def incidents(service:str)->list[dict]:
    """Find historical incidents for a service."""
    return [x for x in INCIDENTS if x["service"]==service]

@mcp.tool()
def rollback_readiness(service:str)->dict:
    """Retrieve rollback readiness and runbook freshness."""
    return RUNBOOKS.get(service,{})

@mcp.tool()
def monitoring_health(service:str)->dict:
    """Retrieve current service health compared with baseline."""
    return MONITORING.get(service,{})

@mcp.tool()
def dependency_graph(service:str)->dict:
    """Retrieve criticality, dependencies and blast radius."""
    return DEPENDENCIES.get(service,{})

@mcp.tool()
def security_controls(change_id:str)->dict:
    """Retrieve security approval and separation-of-duties evidence."""
    return SECURITY.get(change_id,{})

if __name__=="__main__": mcp.run()
