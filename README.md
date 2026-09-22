# Mistral Enterprise Change Risk Agent

An evidence-grounded agent that investigates production changes before deployment using **Mistral + MCP**, deterministic release gates, and human approval.

> The model recommends. Deterministic controls enforce safety gates. A human change authority makes the final production decision.

## Hero scenario

**CHG-4821** upgrades a tier-1 payment-authentication service. Before approval, the agent gathers evidence through MCP tools: the authoritative change record, related incidents, dependency blast radius, rollback readiness, live monitoring health, and security controls.

The synthetic scenario intentionally contains correlated risk signals: a non-backward-compatible schema change, an untested rollback, elevated error rate, and related SEV-1 history.

## Architecture

```text
Change Manager
     |
     v
Mistral Change Risk Agent
     |
     +---- MCP Client / Tool Boundary -------------------+
     |                                                   |
     v                                                   v
Enterprise Change Evidence MCP Server             Mistral reasoning
  | change_request                                     |
  | incidents                                          |
  | dependency_graph                                   |
  | rollback_readiness                                 |
  | monitoring_health                                  |
  | security_controls                                  |
  +----------------------+-----------------------------+
                         |
                         v
                Evidence-grounded assessment
                         |
              Deterministic release gate
                         |
                         v
                  Human approval
```

## Why MCP?

MCP separates enterprise integrations from the reasoning layer. The agent does not need hard-coded access logic for each operational system. In a production implementation, the synthetic MCP tools can be replaced with governed adapters for change management, incident management, observability, source control, CMDB/service catalogs, and security systems.

This creates a reusable boundary for tool discovery, typed inputs, authorization, auditing, and future agent portability.

## MCP tools

| Tool | Purpose |
|---|---|
| `change_request` | Authoritative change details |
| `incidents` | Historical incident evidence |
| `dependency_graph` | Criticality and blast radius |
| `rollback_readiness` | Runbook and rollback readiness |
| `monitoring_health` | Current health vs baseline |
| `security_controls` | Security approval and separation of duties |

## Safety architecture

The LLM is **not** the release gate. `evals/evaluate.py` applies deterministic escalation rules independently of the model. High-risk evidence therefore cannot be silently overridden by persuasive model output.

All production approval remains human-in-the-loop.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Mistral API key to `.env`.

Start the MCP server:

```bash
python -m mcp_server.server
```

Run tests:

```bash
pytest
```

## Repository structure

```text
agent/        Mistral reasoning, evidence and MCP orchestration
mcp_server/   MCP enterprise evidence server
evals/        deterministic release gates and repeatable cases
tests/        safety, citation and control-case tests
.github/      CI test workflow
app.py        Streamlit investigation UI
```

## What is implemented

- Mistral reasoning with JSON output and evidence-ID citation validation
- MCP server with six governed enterprise evidence tools
- MCP client orchestration that discovers/calls the evidence boundary
- Two synthetic scenarios: a high-risk hero case and a lower-risk control
- Model-independent deterministic release gate
- Repeatable evaluation cases and pytest safety tests
- Streamlit investigation UI
- GitHub Actions CI
- Human-in-the-loop production authorization

## Quick demo

```bash
cp .env.example .env
# add MISTRAL_API_KEY
make install
make test
make eval
make demo
```

For a CLI investigation through MCP:

```bash
python -m agent.orchestrator CHG-4821
```

Expected deterministic outcome for the hero scenario: `ESCALATE`. The control case `CHG-4822` should `PASS`.

## Evaluation dimensions

The included deterministic suite validates known release-gate outcomes. The agent layer additionally validates that model-produced evidence citations refer only to evidence IDs actually returned by the enterprise tools. This creates a base for extending the suite with tool-selection accuracy, grounding, escalation accuracy, latency and regression gates.

## Disclaimer

Synthetic data only. This repository is a reference architecture and not a production change-management or deployment authorization system.
