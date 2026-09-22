"""MCP-first orchestration for the demo agent.

The production boundary is MCP. For a zero-infrastructure demo/test path,
the same evidence contract can be collected in-process with --local.
"""
import asyncio, json, os, sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.evidence import collect
from evals.evaluate import release_gate

TOOLS=("change_request","incidents","dependency_graph","rollback_readiness","monitoring_health","security_controls")

async def collect_via_mcp(change_id:str)->dict:
    server=StdioServerParameters(command=sys.executable,args=["-m","mcp_server.server"])
    async with AsyncExitStack() as stack:
        read,write=await stack.enter_async_context(stdio_client(server))
        session=await stack.enter_async_context(ClientSession(read,write))
        await session.initialize()

        discovered=await session.list_tools()
        available={tool.name for tool in discovered.tools}
        missing=set(TOOLS)-available
        if missing:
            raise RuntimeError(f"MCP server missing required tools: {sorted(missing)}")

        async def call(name,args):
            if name not in available:
                raise RuntimeError(f"MCP tool not discovered: {name}")
            result=await session.call_tool(name,args)
            if result.isError:
                raise RuntimeError(f"MCP tool {name} failed")
            return result.structuredContent

        change=await call("change_request",{"change_id":change_id})
        if not change:
            raise ValueError(f"Unknown change: {change_id}")
        service=change["service"]
        return {
          "change":change,
          "incidents":await call("incidents",{"service":service}),
          "dependencies":await call("dependency_graph",{"service":service}),
          "rollback":await call("rollback_readiness",{"service":service}),
          "monitoring":await call("monitoring_health",{"service":service}),
          "security":await call("security_controls",{"change_id":change_id})}

async def investigate(change_id:str,use_mcp:bool=True)->dict:
    # Import the model client only when model reasoning is requested.
    from agent.change_risk_agent import assess

    evidence=await collect_via_mcp(change_id) if use_mcp else collect(change_id)
    gate=release_gate(evidence)
    assessment=assess(evidence)
    return {"change_id":change_id,"evidence":evidence,"release_gate":gate,"assessment":assessment}

if __name__=="__main__":
    change=sys.argv[1] if len(sys.argv)>1 else "CHG-4821"
    use_mcp="--local" not in sys.argv
    print(json.dumps(asyncio.run(investigate(change,use_mcp)),indent=2))
