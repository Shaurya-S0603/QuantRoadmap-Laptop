# SYSTEM laptop study desk

Streamlit companion for QuantRoadmap: study quests and source links, searchable learning library, four-year plan, provisional NTU timetable, project briefs and computing strategy.

## Local Wi-Fi sync

Install Python 3.11 or newer, download/extract the repository ZIP and double-click Start_SYSTEM.cmd on Windows. Alternatively install requirements and run `python run_laptop.py`.

The updated Android SYSTEM Sync launcher provides the phone IP, certificate fingerprint and pairing token. Keep both devices on the same trusted Wi-Fi. The phone is the authoritative progress database. See [setup](LAPTOP_SETUP.txt) and [sync design](docs/lan-sync.md).

## Hosted view

Deploy streamlit_app.py on Streamlit Community Cloud. Hosted mode is a roadmap viewer; it cannot reach your private phone network. Use local mode for live study progress and completion. No phone credentials or personal backups are included in this repository.

The Android source and signing infrastructure remain in the private QuantRoadmap repository. This repository contains only the companion source and shared study catalogue.
