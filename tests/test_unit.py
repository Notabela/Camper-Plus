"""Unit Tests for Camper+ App"""

import unittest
import camperapp
from camperapp.models import db, CampEvent, CampGroup, Camper
from camperapp.forms import LoginForm
import mock
from unittest.mock import patch, DEFAULT
from datetime import datetime


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = camperapp.app.test_client()
        self.app.application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.app = self.app.application
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
            self.assertEqual(template_name, "campers.html")

    # def test_login_gets_login_template(self):
    #     """Test that the login route exists"""
    #     with patch.multiple("camperapp.routes", render_template=DEFAULT) as \
    #             mock_functions:
    #         camperapp.routes.login()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "login.html")

    @mock.patch('camperapp.models.datetime')
    def test_CampEvent_convert_ISO_py_datetime(self, mock_datetime):
        ISO_datetime = "2017-10-10T12:25:27"
        self.assertTrue(camperapp.models.datetime is mock_datetime)
        CampEvent.convert_iso_datetime_to_py_datetime(ISO_datetime)
        mock_datetime.strptime.assert_called_once_with(ISO_datetime, '%Y-%m-%dT%H:%M:%S')

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

    def test_CampEvent_convert_calevent_to_campevent(self):
        full_cal_event = {
            'title': 'basketball',
            'start': '2017-10-10T12:00:05',
            'end': '2017-10-10T13:00:00',
            'group_id': '1'
        }

        campevent = CampEvent.convert_calevent_to_campevent(full_cal_event)
        self.assertEqual(campevent.title, full_cal_event['title'])
        self.assertTrue(campevent.start is not None)
        self.assertTrue(campevent.end is not None)
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
