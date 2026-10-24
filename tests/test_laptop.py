import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from laptop.model import study_units, safe_url

C = json.loads(Path('data/career_catalog.json').read_text())


class CompanionTests(unittest.TestCase):
    def test_all_track_sessions_available_without_progress(self):
        for track in ('engineering', 'low_latency', 'research_engineering', 'commodities', 'research'):
            units = study_units(C, track)
            self.assertTrue(units)
            skills = {s['id']: s for s in C['skills']}
            self.assertEqual(units, [u for u in C['units']
                if 'core' in skills[u['skill']]['tracks'] or track in skills[u['skill']]['tracks']])
            self.assertTrue(any(u['prerequisites'] for u in units))

    def test_links(self):
        for r in C['resources']:
            self.assertTrue(safe_url(r['url']))
        self.assertIsNone(safe_url('javascript:alert(1)'))
        self.assertIsNone(safe_url('https://user:pass@example.com'))

    def test_all_pages_and_topics_without_phone(self):
        from streamlit.testing.v1 import AppTest
        with patch.dict(os.environ, {'SYSTEM_LAN_SYNC': '1'}):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'streamlit_app.py')).run()
            self.assertFalse(app.exception)
            self.assertFalse(app.get('file_uploader'))
            self.assertFalse(app.button)
            topics = next(box for box in app.selectbox if box.label == 'Study topic')
            for topic in topics.options:
                topics.select(topic).run()
                self.assertFalse(app.exception, topic)
                self.assertTrue(app.get('link_button'), topic)
            for page in app.radio[0].options:
                app.radio[0].set_value(page).run()
                self.assertFalse(app.exception, page)
                self.assertFalse(any('phone connection' in h.value.lower() for h in app.subheader))


if __name__ == '__main__':
    unittest.main()
