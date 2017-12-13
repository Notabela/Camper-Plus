"""Integration Tests for Camper+ App"""

import os
from datetime import datetime
import unittest
from camperapp import app, db
from camperapp.models import CampEvent, CampGroup, Camper, Admin
# from config import basedir
import json
from bs4 import BeautifulSoup


class TestUrls(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('.', 'app.db')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        db.session.commit()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        self.app_context.pop()
        db.session.remove()
        db.drop_all()
        try:
            os.remove(os.path.join('.', 'app.db'))
            # os.remove(os.path.join(basedir, 'app.db'))
        except OSError:
            pass

    def test_home(self):
        """Test that home can be accessed"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_calendar(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/schedule")
        self.assertEqual(response.status_code, 200)

    def test_campers(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/campers")
        self.assertEqual(response.status_code, 200)

    def registration(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/registration")
        self.assertEqual(response.status_code, 200)

    def test_parent_schedule(self):
        """Test that the parent Schedule can be accessed"""
        response = self.app.get("/parent/schedule")
        self.assertEqual(response.status_code, 200)

    def test_parent_enrollment(self):
        """Test that the parent Schedule can be accessed"""
        response = self.app.get("/parent/enrollments")
        self.assertEqual(response.status_code, 200)

    def test_parent_register_student(self):
        """Test that the parent Schedule can be accessed"""
        response = self.app.get("/parent/register")
        self.assertEqual(response.status_code, 200)

    def test_post_event_on_schedule_page(self):
        """Test that groups passed to the schedule page are all displayed"""
        camp_group = CampGroup('falcons', 'yellow')
        db.session.add(camp_group)
        db.session.commit()

        json_data = {
            'title': 'Test Event',
            'start': '2017-8-8T12:00:00',
            'end': '2017-8-8T12:00:00',
            'group_id': '1'
        }

        response = self.app.post("/saveEvent", data=json.dumps(json_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_event_on_calendar_endpoint(self):
        """Tests whether put event endpoint is working fine"""
        camp_group = CampGroup('falcons', 'yellow')

        start = datetime.now()
        end = datetime.now()
        camp_event = CampEvent("basketball", start, end)
        camp_group.events.append(camp_event)
        db.session.add(camp_group)
        db.session.add(camp_event)
        db.session.commit()

        new_title = 'soccer'
        json_data = {
            'id': CampEvent.query.filter_by(title="basketball").first().id,
            'title': new_title,
            'start':  CampEvent.convert_py_datetime_to_iso_datetime(start),
            'end': CampEvent.convert_py_datetime_to_iso_datetime(end),
            'group_id': CampEvent.query.filter_by(title="basketball").first().group_id
        }

        response = self.app.put("/saveEvent", data=json.dumps(json_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_calendar_events_endpoint(self):
        event = CampEvent('Basketball', datetime.now(), datetime.now())
        group = CampGroup('falcons', 'green')
        group.events.append(event)
        db.session.add(group)
        db.session.add(event)
        db.session.commit()

        response = self.app.get('/getCampEvents?start=2013-12-01&end=2014-01-12')
        self.assertEqual(response.status_code, 200)

    def test_delete_event_on_calendar_endpoint(self):
        """Tests whether event posted on calendar is saved into db"""
        camp_group = CampGroup('falcons', 'yellow')

        start = datetime.now()
        end = datetime.now()
        camp_event = CampEvent("basketball", start, end)
        camp_group.events.append(camp_event)
        db.session.add(camp_group)
        db.session.add(camp_event)
        db.session.commit()

        json_data = {
            'id': CampEvent.query.filter_by(title="basketball").first().id,
            'title': 'basketball',
            'start':  CampEvent.convert_py_datetime_to_iso_datetime(start),
            'end': CampEvent.convert_py_datetime_to_iso_datetime(end),
            'group_id': CampEvent.query.filter_by(title="basketball").first().group_id
        }

        response = self.app.delete("/saveEvent", data=json.dumps(json_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_event_on_calendar_db(self):
        """Tests whether event posted on calendar is saved into db"""
        camp_group = CampGroup('falcons', 'yellow')
        db.session.add(camp_group)
        db.session.commit()

        json_data = {
            'title': 'Test Event',
            'start': '2017-8-8T12:00:00',
            'end': '2017-8-8T12:00:00',
            'group_id': '1'
        }

        self.app.post("/saveEvent", data=json.dumps(json_data), content_type='application/json')
        events = CampEvent.query.all()
        self.assertEqual(len(events), 1)

    def test_put_event_on_calendar_db(self):
        """Tests whether event posted on calendar is saved into db"""
        camp_group = CampGroup('falcons', 'yellow')

        start = datetime.now()
        end = datetime.now()
        camp_event = CampEvent("basketball", start, end)
        camp_group.events.append(camp_event)
        db.session.add(camp_group)
        db.session.add(camp_event)
        db.session.commit()

        new_title = 'soccer'
        json_data = {
            'id': CampEvent.query.filter_by(title="basketball").first().id,
            'title': new_title,
            'start':  CampEvent.convert_py_datetime_to_iso_datetime(start),
            'end': CampEvent.convert_py_datetime_to_iso_datetime(end),
            'group_id': CampEvent.query.filter_by(title="basketball").first().group_id
        }

        self.app.put("/saveEvent", data=json.dumps(json_data), content_type='application/json')
        event = CampEvent.query.first()
        self.assertEqual(event.title, new_title)

    def test_delete_event_on_calendar_db(self):
        """Tests whether event posted on calendar is saved into db"""
        camp_group = CampGroup('falcons', 'yellow')

        start = datetime.now()
        end = datetime.now()
        camp_event = CampEvent("basketball", start, end)
        camp_group.events.append(camp_event)
        db.session.add(camp_group)
        db.session.add(camp_event)
        db.session.commit()

        json_data = {
            'id': CampEvent.query.filter_by(title="basketball").first().id,
            'title': 'basketball',
            'start':  CampEvent.convert_py_datetime_to_iso_datetime(start),
            'end': CampEvent.convert_py_datetime_to_iso_datetime(end),
            'group_id': CampEvent.query.filter_by(title="basketball").first().group_id
        }

        self.app.delete("/saveEvent", data=json.dumps(json_data), content_type='application/json')
        events = CampEvent.query.all()
        self.assertEqual(len(events), 0)

    def test_get_calendar_events_gets_data(self):
        event = CampEvent('Basketball', datetime.now(), datetime.now())
        group = CampGroup('falcons', 'green')
        group.events.append(event)
        db.session.add(group)
        db.session.add(event)
        db.session.commit()

        response = self.app.get('/getCampEvents?start=2014-12-01&end=2020-01-12')
        self.assertTrue(response.data is not None)

    def test_campers_add_camper_page_shows_groups(self):
        group_name = 'falcons'
        group = CampGroup(group_name, 'green')
        db.session.add(group)
        db.session.commit()
        response = self.app.get('/campers')
        soup = BeautifulSoup(response.data, 'html.parser')
        groups_field = soup.find("select", {"id": "group"})
        option_tag = groups_field.find('option')
        self.assertTrue(option_tag)
        self.assertEqual(option_tag.text, group_name)
