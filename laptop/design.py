"""Modern Dark presentation, with locally bundled Geist faces."""
import base64
from html import escape
from pathlib import Path
import streamlit as st

HERE = Path(__file__).resolve().parent

@st.cache_data
def styles():
    css = (HERE / "modern_dark.css").read_text()
    for token, name in (("__GEIST__", "Geist.ttf"), ("__MONO__", "GeistMono.ttf")):
        data = base64.b64encode((HERE / "fonts" / name).read_bytes()).decode()
        css = css.replace(token, "data:font/ttf;base64," + data)
    return css.replace('format("woff2")', 'format("truetype")').replace("font-weight:100 900", "font-weight:400")

def apply():
    st.html("<style>" + styles() + "</style>")

def hero(catalog, page, track, date):
    pages = ["Study quests", "Resource library", "Four-year roadmap", "NTU timetable", "Projects", "Computing strategy"]
    page_index = pages.index(page) + 1
    st.html(f"""
    <section class="system-hero" aria-label="QuantRoadmap study desk">
      <div class="hero-copy">
        <div class="system-label">Your laptop study desk / {escape(page)}</div>
        <h1>SYSTEM ·<br>QuantRoadmap</h1>
        <p>{escape(date)} · Singapore</p>
      </div>
      <aside class="hero-object" aria-label="Study catalogue">
        <div class="object-header"><span class="object-title">Study desk</span><span class="system-label">{page_index:02} / 06</span></div>
        <div class="system-label">Track</div>
        <div class="object-track">{escape(track.replace("_", " "))}</div>
        <div class="object-rule"></div>
        <div class="system-label">Shared catalogue</div>
        <div class="object-track">{escape(catalog["version"])}</div>
        <div class="system-label" style="margin-top:.7rem">Source checks recorded {escape(catalog["verified"])}</div>
      </aside>
    </section>
    <div class="system-facts" aria-label="Catalogue contents">
      <div class="system-fact"><div class="fact-value">{len(catalog["resources"]):02}</div><div class="fact-label">Learning resources</div></div>
      <div class="system-fact"><div class="fact-value">{len(catalog["units"]):03}</div><div class="fact-label">Study sessions</div></div>
      <div class="system-fact"><div class="fact-value">{len(catalog["projects"]):02}</div><div class="fact-label">Portfolio projects</div></div>
    </div>""")
