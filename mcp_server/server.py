"""MCP server exposing governed enterprise change evidence tools."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("enterprise-change-evidence")

CHANGES = {"CHG-4821": {"service": "payment-authentication", "schema_change": True, "backward_compatible": False}}
INCIDENTS = [{"incident_id": "INC-1932", "service": "payment-authentication", "severity": "SEV-1", "summary": "Latency increased after a schema migration"}]

@mcp.tool()
def change_request(change_id: str) -> dict:
    """Retrieve the authoritative change record."""
    return CHANGES.get(change_id, {})

@mcp.tool()
def incidents(service: str) -> list[dict]:
    """Find historical incidents for a service."""
    return [x for x in INCIDENTS if x["service"] == service]

@mcp.tool()
def rollback_readiness(service: str) -> dict:
    """Retrieve rollback readiness evidence."""
    return {"service": service, "runbook_id": "RB-77", "rollback_tested": False, "last_review_days": 210}

@mcp.tool()
def monitoring_health(service: str) -> dict:
    """Retrieve current service health versus baseline."""
    return {"service": service, "error_rate_pct": 2.8, "baseline_error_rate_pct": 0.4, "p95_latency_ms": 680}

@mcp.tool()
def dependency_graph(service: str) -> dict:
    """Retrieve criticality and blast-radius evidence."""
    return {"service": service, "criticality": "tier-1", "dependencies": ["token-service", "payments-db"], "downstream": ["checkout"]}

@mcp.tool()
def security_controls(change_id: str) -> dict:
    """Retrieve security and separation-of-duties evidence."""
    return {"change_id": change_id, "security_review": "approved", "separation_of_duties": True}

if __name__ == "__main__":
    mcp.run()
