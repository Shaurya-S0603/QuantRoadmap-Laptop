"""Read-only companion rules; never modifies an Android backup."""
import json
from urllib.parse import urlsplit


def safe_url(value):
    try:
        u = urlsplit(value)
        return value if u.scheme == "https" and u.hostname and not u.username else None
    except (ValueError, TypeError):
        return None


def read_backup(raw):
    state = json.loads(raw)
    if not isinstance(state, dict):
        raise ValueError("Choose a JSON object exported by SYSTEM.")
    # Android exports a state envelope; accept raw state as well.
    state = state.get("state", state)
    if not isinstance(state, dict) or not isinstance(state.get("career"), dict):
        raise ValueError("This file does not contain SYSTEM career progress.")
    for key in ("units", "assessments"):
        if not isinstance(state["career"].get(key, {}), dict):
            raise ValueError("Invalid career progress records.")
        if any(not isinstance(v, dict) for v in state["career"].get(key, {}).values()):
            raise ValueError("Invalid career progress entry.")
    if not isinstance(state.get("tasks", []), list):
        raise ValueError("Invalid task list.")
    return state


def passed(catalog, career, skill_id, visiting=None):
    visiting = set(visiting or ())
    if skill_id in visiting:
        return False
    visiting.add(skill_id)
    skill = next(s for s in catalog["skills"] if s["id"] == skill_id)
    record = career.get("assessments", {}).get(skill_id, {})
    score = record.get("score", 0)
    return (isinstance(score, (float, int)) and skill["passScore"] <= score <= 100
            and all(record.get(k) for k in ("independent", "explain", "debug", "evidence"))
            and record.get("criteria") == skill["assessment"]
            and all(passed(catalog, career, p, visiting) for p in skill["prerequisites"]))


def eligible(catalog, career, track):
    skills = {s["id"]: s for s in catalog["skills"]}
    records = career.get("units", {})
    def complete(uid):
        r = records.get(uid, {})
        return isinstance(r, dict) and r.get("done") and bool(r.get("evidence", "").strip())
    result = []
    for unit in catalog["units"]:
        skill = skills[unit["skill"]]
        if not ("core" in skill["tracks"] or track in skill["tracks"]):
            continue
        if complete(unit["id"]) or passed(catalog, career, skill["id"]):
            continue
        if all(passed(catalog, career, p) for p in skill["prerequisites"]) and all(
                complete(p) for p in unit["prerequisites"]):
            result.append(unit)
    return result
