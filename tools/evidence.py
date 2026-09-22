import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def _load(name: str):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def get_change_request(change_id: str):
    return next((x for x in _load("changes.json") if x["change_id"] == change_id), None)


def search_incidents(service: str):
    return [x for x in _load("incidents.json") if x["service"] == service]


def get_service_dependencies(service: str):
    return next((x for x in _load("dependencies.json") if x["service"] == service), None)


def get_runbook(service: str):
    return next((x for x in _load("runbooks.json") if x["service"] == service), None)


def get_monitoring_health(service: str):
    return next((x for x in _load("monitoring.json") if x["service"] == service), None)


def check_security_controls(change_id: str):
    return next((x for x in _load("security.json") if x["change_id"] == change_id), None)
