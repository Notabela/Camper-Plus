"""Unit Tests for Camper+ App"""

import os
import unittest
from camperapp import app, db
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

    def tearDown(self):
        self.app_context.pop()
        self._ctx.pop()
        db.session.remove()
        db.drop_all()
        try:
            os.remove(os.path.join(basedir, 'app.db'))
        except OSError:
            pass

    # TEST IF ALL PYTHON FILES EXIST
    def test_check_init_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', '__init__.py'))
        self.assertTrue(file_exists)

    def test_check_routes_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'routes.py'))
        self.assertTrue(file_exists)

    def test_check_forms_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'forms.py'))
        self.assertTrue(file_exists)

    def test_check_login_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'login.py'))
        self.assertTrue(file_exists)

    def test_check_models_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'models.py'))
        self.assertTrue(file_exists)

    # TEST IF ALL TEMPLATE FILES EXIST
    def test_check_base_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'new_base.html'))
        self.assertTrue(file_exists)

    def test_check_parent_base_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'parent_base.html'))
        self.assertTrue(file_exists)

    def test_check_admin_manage_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'admin_manage.html'))
        self.assertTrue(file_exists)

    def test_check_admin_schedule_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'admin_schedule.html'))
        self.assertTrue(file_exists)

    def test_check_faq_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'faq.html'))
        self.assertTrue(file_exists)

    def test_check_home_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'home.html'))
        self.assertTrue(file_exists)

    def test_check_login_template_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'login.html'))
        self.assertTrue(file_exists)

    def test_check_parent_enrollments_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'parent_enrollments.html'))
        self.assertTrue(file_exists)

    def test_check_parent_register_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'parent_register.html'))
        self.assertTrue(file_exists)

    def test_check_parent_register_complete_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'parent_register_complete.html'))
        self.assertTrue(file_exists)

    def test_check_parent_schedule_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'templates', 'parent_schedule.html'))
        self.assertTrue(file_exists)

    # TEST IF ALL JAVASCRIPT FILES EXIST
    def test_check_admin_manage_js_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'js', 'admin_manage.js'))
        self.assertTrue(file_exists)

    def test_check_admin_schedule_js_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'js', 'admin_schedule.js'))
        self.assertTrue(file_exists)

    def test_check_campers_js_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'js', 'campers.js'))
        self.assertTrue(file_exists)

    def test_check_parent_schedule_js_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'js', 'parent_schedule.js'))
        self.assertTrue(file_exists)

    # TEST ALL CSS FILES EXIST
    def test_check_admin_sched_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'admin_schedule.css'))
        self.assertTrue(file_exists)

    def test_check_home_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'home.css'))
        self.assertTrue(file_exists)

    def test_check_login_signup_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'login_signup.css'))
        self.assertTrue(file_exists)

    def test_check_manage_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'manage.css'))
        self.assertTrue(file_exists)

    def test_check_parent_enrollments_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'parent_enrollments.css'))
        self.assertTrue(file_exists)

    def test_check_parent_register_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'parent_register.css'))
        self.assertTrue(file_exists)

    def test_check_parent_schedule_css_file(self):
        file_exists = os.path.exists(os.path.join(basedir, 'camperapp', 'static', 'css', 'parent_schedule.css'))
        self.assertTrue(file_exists)