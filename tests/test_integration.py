"""Integration Tests for Camper+ App"""

import unittest
import camperapp
from camperapp.models import db, CampEvent, CampGroup
import json
from datetime import datetime

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass',
                                             last_name="test")

    """def test_auth_view_redirect(self):
        response = self.client.post('/auth/',
                                    {'username': 'sam123', 'password': 'abc123'})
        self.assertEqual(response.status_code, 302)

    def test_auth_view_invalid_user(self):
        Test if invalid User
        response = self.client.post('/auth/', {'username': 'sam123', 'password': 'abc123'},
                                    follow=True)
        message = list(response.context['messages'])
        self.assertEqual("The account you entered is invalid, please try again!",
                         str(message[0]))

    def test_auth_view_valid_user(self):
        est if it is a valid user
        response = self.client.post('/auth/', {'username':'testuser', 'password':'testpass'},
                                    follow=True)
        self.assertRedirects(response, '/')
        message = list(response.context['messages'])
        self.assertEqual("Hi test, you have successfully logged in.", str(message[0]))

class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser', password='pass', email="test@123.com")

    def test_register_redirect(self):
        Test if it redirects Login
        response = self.client.post("/registration-submission/",
                                    {'username' : 'test',
                                     'password': 'test',
                                     'email' : 'test123@123.com'})
        self.assertEqual(response.status_code, 302)

    def test_duplicate_user(self):
        est if username is alreayd taken
        response = self.client.post("/registration-submission/", {'username': 'testuser'})
        self.assertEqual(response.context['message'],
                         "Try again, the username testuser is already taken.")

    def test_duplicate_email(self):
        test if a email already exists
        response = self.client.post("/registration-submission/", {'email': 'test@123.com'})
        self.assertEqual(response.context['message'],
                         "Try again, there is already an account with that email test@123.com.")

    def test_register_auto_login(self):
        Test for Auto Login
        self.client.post("/registration-submission/",
                         {'username' : 'test',
                          'password': 'test',
                          'email' : 'test123@123.com'},
                         follow=True)
        self.assertIn('_auth_user_id', self.client.session)

     def test_user_added_to_db(self):
        self.client.post("/registration-submission/", {'username' : 'test', 'password' : 'test'})
        try:
            User.objects.get(username="test")
        except ObjectDoesNotExist:
            self.fail('Retrieving brand new registered user from database failed.' \
                      'ObjectDoesNotExist exception raised.')

class LogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_logout(self): 
        Test to see if you can log out
        response = self.client.get('/logout/', follow=True)
        self.assertRedirects(response, '/')
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'You have successfully logged out.')
        self.assertNotIn('_auth_user_id', self.client.session)"""

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
