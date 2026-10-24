# SYSTEM study website

Open https://quantroadmap-system.streamlit.app/ in any laptop browser.
No installation, phone connection, pairing credentials or backup upload is needed.

The six views provide study sessions and source links, a searchable resource
library, the four-year quant roadmap, the provisional NTU course plan and approval
gates, portfolio project briefs, and computing strategy. The Modern Dark design
is shared by all views. Select a track and a study topic to browse every relevant
session, including later sessions; prerequisites are shown as guidance.

The site reads data/career_catalog.json. It does not receive phone records or
record personal progress. The Android app operates independently; its tasks,
quizzes, budget and progress remain on the phone.

## Optional local development

Requires Python 3.11 or later:

    python -m pip install -r requirements.txt
    python run_laptop.py

Alternatively run `python -m streamlit run streamlit_app.py`.
The optional Windows launcher Start_SYSTEM.cmd opens the same standalone site.

## Deployment and verification

Streamlit Community Cloud follows main in Shaurya-S0603/QuantRoadmap-Laptop,
entrypoint streamlit_app.py. No secrets are required. The Android repository
keeps a matching copy of the site source and the shared catalogue.

    python -m unittest discover -s tests -p test_laptop.py -v

The site is a planning reference. Confirm university prerequisites, waivers and
availability with NTU. Catalogue source dates do not imply every external link
was rechecked during this change.
