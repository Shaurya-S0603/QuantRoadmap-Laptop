"""QuantRoadmap SYSTEM laptop companion."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import streamlit as st
from laptop.model import study_units, safe_url
from laptop.design import apply as apply_design, hero

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="SYSTEM · QuantRoadmap", page_icon="⚔️", layout="wide")
apply_design()
catalog = json.loads((ROOT / "data/career_catalog.json").read_text())
resources = {r["id"]: r for r in catalog["resources"]}
with st.sidebar:
    st.header("Study desk")
    page = st.radio("Open", ["Study quests", "Resource library", "Four-year roadmap", "NTU timetable", "Projects", "Computing strategy"])
    track = st.selectbox("Track", ["engineering", "low_latency", "research_engineering", "commodities", "research"])
hero(catalog, page, track, datetime.now(ZoneInfo("Asia/Singapore")).strftime("%d %b %Y"))

def link(label, url):
    if safe_url(url):
        st.link_button(label, url)

def resource(r):
    st.write(r.get("author", ""))
    st.caption(r.get("cost", ""))
    link("Open study material ↗", r.get("url"))
    st.write(r.get("why", ""))
    st.caption(r.get("compatibility", ""))
    for section in r.get("sections", []):
        st.markdown("**" + section["title"] + "**")
        st.write(section.get("exercise", ""))

if page == "Study quests":
    st.subheader("Choose your next study session")
    st.caption("Browse sessions by track and topic. Open the source material, follow the assignment and keep evidence of your work.")
    skills = {s["id"]: s for s in catalog["skills"]}
    options = study_units(catalog, track)
    topics = list(dict.fromkeys(u["skill"] for u in options))
    topic = st.selectbox("Study topic", topics, format_func=lambda key: skills[key]["title"])
    options = [u for u in options if u["skill"] == topic]
    prerequisites = skills[topic]["prerequisites"]
    if prerequisites:
        st.caption("Recommended prerequisites: " + ", ".join(skills[key]["title"] for key in prerequisites))
    budget = st.slider("Study budget (minutes)", 15, 120, 120, 15)
    for index, u in enumerate(options):
        if index % 2 == 0:
            quest_columns = st.columns(2, gap="large")
        with quest_columns[index % 2], st.container(border=True, key="quest_" + u["id"]):
            st.html(f'<div class="quest-index">SESSION {index + 1:02} / {u["skill"].upper()}</div>')
            st.markdown("### " + u["title"])
            st.caption(f'{min(budget, u["minutes"])} min suggested · full session {u["minutes"]} min · {u["id"]}')
            if budget < u["minutes"]:
                st.caption("Partial session: continue the remaining work later.")
            st.write(u.get("instruction", ""))
            st.write(u["assignment"])
            r = resources[u["resource"]]
            link(r["title"] + " ↗", r["url"])
            section = u.get("section", 0)
            if isinstance(section, int) and 1 <= section <= len(r.get("sections", [])):
                st.write("Section: " + r["sections"][section - 1]["title"])
            st.caption("Evidence: " + u.get("evidence", "Keep a record of your independent work."))
elif page == "Resource library":
    st.subheader("All study material")
    query = st.text_input("Search titles, authors, topics or modules").casefold()
    for r in catalog["resources"]:
        if query and query not in json.dumps(r, ensure_ascii=False).casefold():
            continue
        with st.expander(r["title"]):
            resource(r)
elif page == "Four-year roadmap":
    st.subheader("2026–2030 roadmap")
    st.caption("Planning windows from the shared catalogue; university dates and eligibility remain provisional.")
    for m in catalog["milestones"]:
        with st.expander(m["semester"] + " · " + m["title"], expanded=True):
            st.caption(m["start"] + " → " + m["end"])
            st.write(m["evidence"])
            plan = m.get("studyPlan", {})
            st.write(plan.get("focus", ""))
            for b in plan.get("books", []):
                st.write(b["title"] + " · " + b.get("topics", ""))
                if b.get("resourceId") in resources:
                    link("Open " + b["title"], resources[b["resourceId"]]["url"])
            st.write(plan.get("project", ""))
elif page == "NTU timetable":
    st.subheader("Provisional NTU degree plan")
    st.warning("This is a planning aid, not an approved degree audit. Confirm prerequisites, waivers and course availability with NTU.")
    for semester in [f"Y{y} S{s}" for y in range(1, 5) for s in (1, 2)] + ["Unscheduled"]:
        rows = [m for m in catalog["modules"] if m["semester"] == semester]
        if rows:
            with st.expander(f'{semester} · {sum(m["au"] for m in rows)} AU'):
                st.dataframe([{k: m.get(k, "") for k in ("code", "title", "au", "status", "dependency")} for m in rows], hide_index=True, width="stretch")
    for gate in catalog["gates"]:
        with st.expander(gate["title"]):
            st.write(gate["issue"])
            st.write(gate["action"])
elif page == "Projects":
    st.subheader("Portfolio project briefs")
    for p in catalog["projects"]:
        with st.expander(p["title"]):
            for key in ("period", "objective", "stack", "architecture", "testing", "metrics", "github", "integration"):
                st.markdown("**" + key.title() + "**")
                st.write(p.get(key, ""))
            for m in p["milestones"]:
                st.markdown("**" + m["title"] + "**")
                st.write(m["deliverable"])
else:
    st.subheader("Laptop, campus computing and storage")
    strategy = catalog.get("computingStrategy", {})
    st.write(strategy.get("decision", ""))
    st.caption("Reviewed " + strategy.get("reviewed", ""))
    computer = strategy.get("computer", {})
    with st.container(border=True):
        st.markdown("### " + computer.get("name", "Computer"))
        st.dataframe([{"Component": k.upper(), "Specification": computer[k]}
                      for k in ("cpu", "memory", "storage", "gpu", "npu", "display") if k in computer],
                     hide_index=True, width="stretch")
        for item in computer.get("bestFor", []):
            st.markdown("- " + item)
        st.caption(computer.get("limits", ""))
    for facility in strategy.get("facilities", []):
        with st.expander(facility["title"]):
            st.write(facility.get("purpose", ""))
            for key in ("verification", "guardrails", "workflow"):
                st.markdown("**" + key.title() + "**")
                st.write(facility.get(key, ""))
            for item in facility.get("checklist", []):
                st.markdown("- " + item)
    st.markdown("### Purchase gates")
    for item in strategy.get("purchaseGates", []):
        st.markdown("- " + item)
    st.markdown("### Semester approach")
    for item in strategy.get("semesterApproach", []):
        st.markdown("**" + item["period"] + "**")
        st.write(item["approach"])
    for source in strategy.get("sources", []):
        st.caption(source)
    with st.expander("Full computing strategy record"):
        st.json(strategy, expanded=False)
st.divider()
st.caption("Shared catalogue " + catalog["version"] + " · Source checks recorded " + catalog["verified"] + " · Links open the original provider; some materials require purchase or university access.")

