"""Integration Tests for Camper+ App"""

import unittest
from unittest import TestCase
import camperapp
from camperapp.models import db, CampEvent, CampGroup
import json
from datetime import datetime


class TestUrls(unittest.TestCase):
    def setUp(self):
        self.app = camperapp.app.test_client()
        self.app.application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.app = self.app.application
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        """Test that home can be accessed"""
        response = self.app.get("/")
        self.assertTrue(response.status_code, 200)

    def test_calendar(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/schedule")
        self.assertTrue(response.status_code, 200)

    def test_campers(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/campers")
        self.assertTrue(response.status_code, 200)
        
    def registration(self):
        """Test that the Calendar Page can be accessed"""
        response = self.app.get("/registration")
        self.assertTrue(response.status_code, 200)""""""

    def test_post_event_on_schedule_page(self):
        """Test that roups passed to the schedule page are all displayed"""
        json_data = {
            'title': 'Test Event',
            'start': '2017-8-8T12:00:00',
            'end': '2017-8-8T12:00:00',
            'group': '3'
        }

        response = self.app.post("/saveEvent", data=json.dumps(json_data),
                                 content_type='application/json')
        self.assertTrue(response.status_code, 200)

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
        self.assertTrue(response.status_code, 200)

    def test_get_calendar_events_endpoint(self):
        event = CampEvent('Basketball', datetime.now(), datetime.now())
        group = CampGroup('falcons', 'green')
        group.events.append(event)
        db.session.add(group)
        db.session.add(event)
        db.session.commit()

        response = self.app.get('/getCampEvents?start=2013-12-01&end=2014-01-12')
        self.assertTrue(response.status_code, 200)

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
        self.assertTrue(response.status_code, 200)

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
