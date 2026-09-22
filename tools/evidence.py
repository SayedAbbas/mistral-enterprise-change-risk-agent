import json
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / "data"
def _load(name): return json.loads((DATA / name).read_text())
def get_change_request(change_id): return next((x for x in _load("changes.json") if x["change_id"] == change_id), None)
def search_incidents(service): return [x for x in _load("incidents.json") if x["service"] == service]
def get_service_dependencies(service): return _load("dependencies.json").get(service, [])
def get_runbook(service): return _load("runbooks.json").get(service)
def get_monitoring_health(service): return _load("monitoring.json").get(service)
def get_security_controls(change_id): return _load("security.json").get(change_id)
