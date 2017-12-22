"""Unit Tests for Camper+ App"""

import os
import mock
from unittest.mock import patch, DEFAULT
from datetime import datetime
import unittest
import camperapp.routes
from camperapp import app, db
from camperapp.models import CampEvent, CampGroup, Camper, Admin, User
from config import basedir


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        app.login_manager.init_app(app)
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
            os.remove(os.path.join(basedir, 'app.db'))
        except OSError:
            pass

    def test_schedule_calls_render_template(self):
        """Test that the Schedule endpoint calls render_template"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.schedule()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_schedule_gets_schedule_template(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.schedule()
            render_template = mock_funcs['render_template']
            call_args = render_template.call_args
            template_name = call_args[0][0]
            self.assertEqual(template_name, "admin_schedule.html")

    def test_faq_calls_faq_template(self):
        """Test that the Schedule endpoint calls render_template"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.faq()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_faq_gets_faq_template(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.faq()
            render_template = mock_funcs['render_template']
            call_args = render_template.call_args
            template_name = call_args[0][0]
            self.assertEqual(template_name, "faq.html")

    def test_campers_gets_calls_render_template(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.campers()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_campers_gets_campers_template(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.campers()
            render_template = mock_funcs['render_template']
            call_args = render_template.call_args
            template_name = call_args[0][0]
            self.assertEqual(template_name, "admin_manage.html")

    def test_get_login_calls_render_template(self):
        """"Test that the login route exists"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT, session=DEFAULT, request=DEFAULT) \
                as mock_functions:
            mock_functions['request'].method = 'GET'
            camperapp.routes.login()
            render_template = mock_functions["render_template"]
            self.assertTrue(render_template.called)

    def test_login_gets_login_template(self):
        """"Test that the login route exists"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT, session=DEFAULT, request=DEFAULT) \
                as mock_functions:
            mock_functions['request'].method = 'GET'
            camperapp.routes.login()
            render_template = mock_functions["render_template"]
            self.assertTrue(render_template.called)
            call_args = render_template.call_args
            file_name = call_args[0][0]
            self.assertEqual(file_name, "login.html")

    @mock.patch('camperapp.models.datetime')
    def test_CampEvent_convert_ISO_py_datetime(self, mock_datetime):
        iso_datetime = "2017-10-10T12:25:27"
        self.assertTrue(camperapp.models.datetime is mock_datetime)
        CampEvent.convert_iso_datetime_to_py_datetime(iso_datetime)
        mock_datetime.strptime.assert_called_once_with(iso_datetime, '%Y-%m-%dT%H:%M:%S')

    @patch.object(CampEvent, 'convert_iso_datetime_to_py_datetime')
    def test_CampEvent_convert_calevent_to_campevent_args(self, mock_parser):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        CampEvent.convert_calevent_to_campevent(full_cal_event)
        mock_parser.assert_any_call(full_cal_event['start'])
        mock_parser.assert_any_call(full_cal_event['end'])

    def test_CampEvent_convert_calevent_to_campevent_title(self):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        campevent = CampEvent.convert_calevent_to_campevent(full_cal_event)
        self.assertEqual(campevent.title, full_cal_event['title'])

    def test_CampEvent_convert_calevent_to_campevent_start_time(self):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        campevent = CampEvent.convert_calevent_to_campevent(full_cal_event)

        self.assertEqual(campevent.start.strftime('%Y-%m-%dT%H:%M:%S'), full_cal_event['start'])

    def test_CampEvent_convert_calevent_to_campevent_end(self):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        campevent = CampEvent.convert_calevent_to_campevent(full_cal_event)
        self.assertEqual(campevent.end.strftime('%Y-%m-%dT%H:%M:%S'), full_cal_event['end'])

    def test_CampEvent_convert_calevent_to_campevent_group_id(self):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        campevent = CampEvent.convert_calevent_to_campevent(full_cal_event)
        self.assertEqual(campevent.group_id, int(full_cal_event['group_id']))

    def test_camper_save(self):
        first_name = 'daniel'
        last_name = 'obeng'
        camper = Camper()
        camper.first_name = first_name
        camper.last_name = last_name
        db.session.add(camper)
        db.session.commit()

        queried_camper = Camper.query.filter_by(first_name=first_name).one()
        self.assertTrue(queried_camper is not None)

    def test_admin_signup(self):
        name = 'jay'
        email = 'jay@yahoo.com'
        pwdhash = 'zzzzxxxx'

        admin = Admin(name, email, pwdhash)
        db.session.add(admin)
        db.session.commit()

        queried_admin = Admin.query.filter_by(name=name).one()
        self.assertTrue(queried_admin is not None)

    def test_campevent_save(self):
        title = "basketball"
        start = datetime.now()
        end = datetime.now()
        camp_event = CampEvent(title, start, end)
        db.session.add(camp_event)
        db.session.commit()

        queried_camp_event = CampEvent.query.filter_by(title=title).one()
        self.assertTrue(queried_camp_event is not None)

    def test_campevent_add_no_color(self):
        group_name = 'falcons'
        group_color = 'yellow'
        event_title = "basketball"
        event_start = datetime.now()
        event_end = datetime.now()

        camp_event = CampEvent(event_title, event_start, event_end)
        camp_group = CampGroup(group_name, group_color)
        db.session.add(camp_event)
        db.session.add(camp_group)
        db.session.commit()

        # no group yet, should fail
        camp_event.add_color_attr()
        self.assertTrue(camp_event.color is None)

    def test_campevent_add_color(self):
        group_name = 'falcons'
        group_color = 'yellow'
        event_title = "basketball"
        event_start = datetime.now()
        event_end = datetime.now()

        camp_event = CampEvent(event_title, event_start, event_end)
        camp_group = CampGroup(group_name, group_color)
        db.session.add(camp_event)
        db.session.add(camp_group)
        db.session.commit()

        camp_group.events.append(camp_event)
        db.session.commit()

        camp_event.add_color_attr()
        self.assertTrue(hasattr(camp_event, 'color'))

    def test_campgroup_save(self):
        name = 'falcons'
        color = 'yellow'

        camp_group = CampGroup(name, color)
        db.session.add(camp_group)
        db.session.commit()

        queried_camp_group = CampGroup.query.filter_by(name=name).one()
        self.assertTrue(queried_camp_group is not None)

    def test_campgroup_relationship(self):
        group_name = 'falcons'
        group_color = 'yellow'
        camper_first_name = 'daniel'
        camper_last_name = 'obeng'
        camper_age = 12

        camp_group = CampGroup(group_name, group_color)
        camper = Camper()
        camper.first_name = camper_first_name
        camper.last_name = camper_last_name
        camper.age = camper_age
        camp_group.campers.append(camper)
        db.session.add(camp_group)
        db.session.add(camper)
        db.session.commit()

        queried_camp_group = Camper.query.filter_by(first_name=camper_first_name).one()\
            .campgroup
        self.assertEqual(queried_camp_group, camp_group)

    def test_campevent_relationship(self):
        group_name = 'falcons'
        group_color = 'yellow'
        event_title = "basketball"
        event_start = datetime.now()
        event_end = datetime.now()

        camp_event = CampEvent(event_title, event_start, event_end)
        camp_group = CampGroup(group_name, group_color)
        camp_group.events.append(camp_event)
        db.session.add(camp_event)
        db.session.add(camp_group)
        db.session.commit()

        queried_camp_group = CampEvent.query.filter_by(title=event_title).one().campgroup
        self.assertEqual(queried_camp_group, camp_group)
