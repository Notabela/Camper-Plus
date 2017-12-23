"""Unit Tests for Camper+ App"""

import os
import mock
from unittest.mock import patch, DEFAULT, Mock
from datetime import datetime
import unittest
import camperapp.routes
from camperapp import app, db
from camperapp.models import CampEvent, CampGroup, Camper, Admin, User, Role, Parent
from flask_login import login_user
from werkzeug.exceptions import Unauthorized
import pytest
from config import basedir


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['LOGIN_DISABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        app.login_manager.init_app(app)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self._ctx = app.test_request_context()
        self._ctx.push()

        db.drop_all()
        db.create_all()
        db.session.commit()
        self.assertEqual(app.debug, False)

        # Create admin
        self.admin = User('test_a@mail.com', 'testing', Role.admin)
        db.session.add(self.admin)

        # Create Parent
        self.parent = Parent()
        self.parent.first_name = 'first_test'
        self.parent.last_name = 'last_test'
        self.parent.gender = 'f'
        self.parent.email = 'test@mail.com'
        self.parent.street_address = 'test'
        self.parent.city = 'T'
        self.parent.state = 'B'

        db.session.add(self.parent)
        db.session.commit()

        # Create parent login
        self.parent_user = User('test_p@mail.com', 'testing', Role.parent)
        self.parent_user.parent_id = self.parent.id
        db.session.add(self.parent_user)
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()
        self._ctx.pop()
        db.session.remove()
        db.drop_all()
        try:
            os.remove(os.path.join(basedir, 'app.db'))
        except OSError:
            pass

    def test_index_gets_calls_render_template_without_login(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.index()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_index_gets_home_template_without_login(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.index()
            render_template = mock_funcs['render_template']
            call_args = render_template.call_args
            template_name = call_args[0][0]
            self.assertEqual(template_name, "home.html")

    def test_index_gets_calls_redirect_with_login_admin(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        login_user(self.admin)
        with patch.multiple('camperapp.routes', redirect=DEFAULT, url_for=DEFAULT) \
                as mock_funcs:
            camperapp.routes.index()
            redirect = mock_funcs['redirect']
            url_for = mock_funcs['url_for']
            self.assertTrue(redirect.called)
            self.assertTrue(url_for.called)

    def test_index_calls_right_url_with_login_admin(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        login_user(self.admin)
        with patch.multiple('camperapp.routes', redirect=DEFAULT, url_for=DEFAULT) as \
                mock_funcs:
            camperapp.routes.index()
            url_for = mock_funcs['url_for']
            call_args = url_for.call_args
            redirect_url = call_args[0][0]
            self.assertEqual(redirect_url, 'campers')

    def test_index_gets_calls_redirect_with_login_parent(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        login_user(self.parent_user)
        with patch.multiple('camperapp.routes', redirect=DEFAULT, url_for=DEFAULT) \
                as mock_funcs:
            camperapp.routes.index()
            redirect = mock_funcs['redirect']
            url_for = mock_funcs['url_for']
            self.assertTrue(redirect.called)
            self.assertTrue(url_for.called)

    def test_index_calls_right_url_with_login_parent(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        login_user(self.parent_user)
        with patch.multiple('camperapp.routes', redirect=DEFAULT, url_for=DEFAULT) as \
                mock_funcs:
            camperapp.routes.index()
            url_for = mock_funcs['url_for']
            call_args = url_for.call_args
            redirect_url = call_args[0][0]
            self.assertEqual(redirect_url, 'parent_enrollments')

    def test_schedule_calls_render_template(self):
        """Test that the Schedule endpoint calls render_template"""
        login_user(self.admin)
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.schedule()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_schedule_gets_schedule_template(self):
        """Test that the Schedule endpoint calls the schedule Page"""
        login_user(self.admin)
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
        login_user(self.admin)
        with patch.multiple('camperapp.routes', render_template=DEFAULT) as \
                mock_funcs:
            camperapp.routes.campers()
            render_template = mock_funcs['render_template']
            self.assertTrue(render_template.called)

    def test_campers_gets_campers_template(self):
        login_user(self.admin)
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

    def test_admin_creation(self):
        email = 'jay@yahoo.com'
        password = 'zzzzxxxx'

        admin = User(email, password, Role.admin)
        db.session.add(admin)
        db.session.commit()

        queried_admin = User.query.filter_by(email=email).one()
        self.assertTrue(queried_admin is not None)

    def test_parent_user_creation(self):
        email = 'jay@yahoo.com'
        password = 'zzzzxxxx'

        parent = User(email, password, Role.parent)
        db.session.add(parent)
        db.session.commit()

        queried_parent = User.query.filter_by(email=email).one()
        self.assertTrue(queried_parent is not None)

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

    @patch.object(camperapp.login, 'current_user')
    def test_requires_roles_for_login_allows_specified_roles(self, mock_user):
        wrapper = camperapp.login.requires_roles(Role.admin)
        sample_func = Mock(return_value='Pass')
        protected_func = wrapper(sample_func)

        mock_user.role = Role.admin
        return_value = protected_func()
        self.assertTrue(return_value, sample_func.return_value)

    @patch.object(camperapp.login, 'current_user')
    def test_requires_roles_for_login_blocks_unspecified_roles(self, mock_user):
        wrapper = camperapp.login.requires_roles(Role.admin)
        sample_func = Mock(return_value='Pass')
        protected_func = wrapper(sample_func)

        mock_user.role = Role.parent

        with pytest.raises(Unauthorized):
            protected_func()

    def test_load_user_with_login_manager(self):
        user = User('test@test.com', 'pass', Role.parent)
        db.session.add(user)
        db.session.commit()

        loaded_user = camperapp.login.load_user(user.id)
        self.assertEqual(loaded_user, user)

    def test_get_user_name_admin(self):
        user = User('test@test.com', 'pass', Role.admin)
        db.session.add(user)
        db.session.commit()

        user_name = camperapp.models.get_user_name(user)
        self.assertEqual(user_name, 'test')

    def test_get_user_name_admin_bad_email(self):
        user = User('test.com', 'pass', Role.admin)
        db.session.add(user)
        db.session.commit()

        user_name = camperapp.models.get_user_name(user)
        self.assertEqual(user_name, 'test.com')

    def test_get_user_name_parent_bad_input(self):
        parent = Parent()
        db.session.add(parent)
        db.session.commit()

        user = User('test@test.com', 'pass', Role.parent)
        user.parent_id = parent.id
        db.session.add(user)
        db.session.commit()

        user_name = camperapp.models.get_user_name(user)
        self.assertEqual(user_name, 'Parent')

    def test_parent_name(self):
        parent = Parent()
        parent.first_name = 'Jane'
        parent.last_name = 'Test'
        db.session.add(parent)
        db.session.commit()

        self.assertEqual(parent.name(), 'Test, Jane')

    def test_parent_alt_name(self):
        parent = Parent()
        parent.first_name = 'Jane'
        parent.last_name = 'Test'
        db.session.add(parent)
        db.session.commit()

        self.assertEqual(parent.alt_name(), 'Jane Test')

    def test_camper_name(self):
        camper = Camper()
        camper.first_name = 'Jack'
        camper.last_name = 'Test'
        db.session.add(camper)
        db.session.commit()

        self.assertEqual(camper.name(), 'Test, Jack')

    def test_camper_alt_name(self):
        camper = Camper()
        camper.first_name = 'Jack'
        camper.last_name = 'Test'
        db.session.add(camper)
        db.session.commit()

        self.assertEqual(camper.alt_name(), 'Jack Test')

    def test_camper_age(self):
        my_date = '1 April, 2010'
        parsed_date = datetime.strptime(my_date, "%d %B, %Y")
        age = datetime.today().year - parsed_date.year

        camper = Camper()
        camper.first_name = 'Jack'
        camper.last_name = 'Test'
        camper.birth_date = camper.birth_date = datetime.strptime(my_date, "%d %B, %Y")
        db.session.add(camper)
        db.session.commit()

        self.assertEqual(camper.age(), age)
