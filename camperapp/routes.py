"""
.. module:: camperapp.routes
   :platform: Unix, Windows
   :synopsis: Dispatch Endpoints for Camper+ web application

.. moduleauthor:: Daniel Obeng, Chris Kwok, Eric Kolbusz, Zhirayr Abrahamyam

"""
from datetime import datetime
from camperapp import app
from camperapp.models import db, CampEvent, CampGroup, CampEventSchema, Camper, \
    Parent, User, Role, get_user_name, camp_season, registration_cost, camp_address
from camperapp.forms import SignupFormAdmin, LoginForm, \
    ChildEnrollmentForm, CreateParentForm, CreateChildForm
from camperapp.login import requires_roles
from flask import render_template, session, redirect, url_for, jsonify, request, flash, g
from flask_login import login_user, current_user, login_required, logout_user
from wtforms import SelectField
from wtforms.validators import DataRequired


@app.route('/', methods=['GET'])
def index():
    """Index View

        Endpoint for Camper+ homepage page with login form.
        Users are automatically redirected to default pages
        if they are logged in/authenticated

        Returns:
            parents are redirected to parent_enrollments endpoint.
            admins are redirected to campers endpoint.
            unauthenticated users are served the rendered home.html
            template with login form.
    """
    if current_user.is_authenticated:
        if current_user.role is Role.parent:
            return redirect(url_for('parent_enrollments'))
        elif current_user.role is Role.admin:
            return redirect(url_for('campers'))

    form = LoginForm()
    return render_template("home.html", form=form)


@app.route('/faq', methods=['GET'])
def faq():
    """Camper+ FAQ Page
        Static Camper+ FAQ Page
    """
    return render_template("faq.html")


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
@requires_roles(Role.admin)
def schedule():
    """Admin Schedule View

        Endpoint for camp schedule. Contains the Full Calendar
        js calendar for rendering camp events

        Returns:
            rendered admin_schedule.html template

        .. note::
            Only authenticated admins can access this endpoint
    """
    groups = CampGroup.query.all()
    account_name = get_user_name(current_user)
    return render_template("admin_schedule.html", account_name=account_name, groups=groups)


@app.route('/parent/schedule', methods=['GET'])
@login_required
@requires_roles(Role.parent)
def parent_schedule():
    """Parent Schedule View

        Endpoint for parent camp schedule. Contains the Full Calendar
        js calendar for rendering camp events

        Returns:
            rendered parent_schedule.html template

        .. note::
            Only authenticated parents can access this endpoint
    """
    account_name = get_user_name(current_user)
    parent = Parent.query.filter_by(id=current_user.parent_id).first()
    children = parent.campers.all()
    return render_template("parent_schedule.html", account_name=account_name, children=children)


@app.route('/parent/enrollments', methods=['GET'])
@login_required
@requires_roles(Role.parent)
def parent_enrollments():
    """Parent Enrollments View

        Endpoint to show parent's enrolled campers

        Returns:
            rendered parent_enrollments.html page

        .. note::
            Only authenticated parents can access this endpoint
    """
    account_name = get_user_name(current_user)

    parent = Parent.query.filter_by(id=current_user.parent_id).first()
    children = parent.campers.all()
    return render_template("parent_enrollments.html", account_name=account_name, children=children)


@app.route('/parent/register', methods=['GET', 'POST'])
@login_required
@requires_roles(Role.parent)
def parent_register():
    """Parent Child Registration View

        Endpoint with forms for parents to register new camper.
        Valid Campers submitted are added to the Campers database table

        Returns:
            if a GET or invalid POST request is received, returns rendered
            parent_register.html template.
            if a valid POST request is received, returns rendered
            parent_register_complete.html template

        .. note::
            Only authenticated parents can access this endpoint
    """
    account_name = get_user_name(current_user)
    parent = Parent.query.filter_by(id=current_user.parent_id).first()
    form = ChildEnrollmentForm()

    if request.method == "POST":
        camper = Camper()
        camper.first_name = form.child_first_name.data
        camper.last_name = form.child_last_name.data
        camper.birth_date = datetime.strptime(form.child_birth_date._value(), "%d %B, %Y")
        camper.grade = form.child_grade.data
        camper.gender = form.child_gender.data
        camper.medical_notes = form.medical_notes.data

        camper.parent = parent

        if form.street_address.data == "":
            # No address supplied, set address to parent address
            camper.street_address = parent.street_address
            camper.city = parent.city
            camper.state = parent.state
            camper.zip_code = parent.zip_code

        else:
            camper.street_address = form.street_address.data
            camper.city = form.city.data
            camper.state = form.state.data
            camper.zip_code = form.zipcode.data

        camper.other_parent_name = form.other_parent_name.data
        if form.other_parent_birth_date._value() != '':
            camper.other_parent_birth_date = \
                datetime.strptime(form.other_parent_birth_date._value(), "%d %B, %Y")
        camper.other_parent_email = form.other_parent_email.data
        camper.other_parent_phone = form.other_parent_cell.data

        camper.is_active = False
        camper.group_id = CampGroup.query.filter_by(name='None').first().id

        db.session.add(camper)
        db.session.commit()

        return render_template('parent_register_complete.html',
                               cost=registration_cost, camp_address=camp_address)

    elif request.method == "GET":
        parent_name = parent.alt_name()
        return render_template("parent_register.html", form=form,
                               account_name=account_name, camp_season=camp_season,
                               cost=registration_cost, parent_name=parent_name)


@app.route('/campers', methods=['GET'])
@login_required
@requires_roles(Role.admin)
def campers():
    """Administrator people/groups View

        Endpoint to view campers, camp groups and parents

        Returns:
            rendered admin_manage.html template

        .. note::
            Only authenticated admins can access this endpoint
    """
    account_name = get_user_name(current_user)

    parent_form = CreateParentForm()
    child_form = CreateChildForm()

    # Get all Campers
    all_campers = Camper.query.order_by(Camper.last_name).all()
    all_parents = Parent.query.order_by(Parent.last_name).all()
    all_groups = CampGroup.query.order_by(CampGroup.name).all()

    return render_template('admin_manage.html', account_name=account_name,
                           groups=all_groups, parents=all_parents, campers=all_campers,
                           parent_form=parent_form, child_form=child_form)


@app.route('/manage/parent', methods=['POST', 'DELETE'])
@login_required
@requires_roles(Role.admin)
def submit_parent_management():
    """Parent Management Endpoint

        Endpoint for administrator to edit, add and delete
        parents

        Returns:
            on valid POST request, returns a redirect to url_for('campers')
            on valid DELETE, return json with success flag
            on invalid POST/DELETE request, return json with failure flag

        .. note::
            Only authenticated admins can access this endpoint
    """

    # a = request.get_json(force=True)

    if request.method == 'POST':
        parent_form = CreateParentForm(request.form)

        # Validation is done on Client Side
        parent = Parent()
        parent.first_name = parent_form.first_name.data
        parent.last_name = parent_form.last_name.data
        parent.birth_date = datetime.strptime(parent_form.birth_date._value(), "%d %B, %Y")
        parent.gender = parent_form.gender.data
        parent.email = parent_form.email.data
        parent.phone = parent_form.phone.data
        parent.street_address = parent_form.street_address.data
        parent.city = parent_form.city.data
        parent.state = parent_form.state.data
        parent.zip_code = parent_form.zipcode.data

        db.session.add(parent)
        db.session.commit()

        # tell template to default to parent tab
        flash("parents", category='tab_choice')
        return redirect(url_for('campers'))

    elif request.method == 'DELETE':
        try:
            parent_id = request.json['parent_id']
            parent = Parent.query.filter_by(id=parent_id).first()

            if parent.campers.all():
                return jsonify({'success': False,
                                'msg': 'Cannot Delete Parent with Enrollments'}), \
                       400, {'ContentType': 'application/json'}

            db.session.delete(parent)
            db.session.commit()
        except Exception:
            return jsonify({'success': False, 'msg': 'Exception occurred'}), \
                   500, {'ContentType': 'application/json'}

        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/manage/camper', methods=['POST', 'DELETE', 'PATCH'])
@login_required
@requires_roles(Role.admin)
def submit_camper_management():
    """Camper Management Endpoint

        Endpoint for administrator to edit, add and delete
        campers

        Returns:
            on valid POST request, returns a redirect to url_for('campers')
            on valid DELETE/PATCH, return json with success flag
            on invalid POST/DELETE request, return json with failure flag

        .. note::
            Only authenticated admins can access this endpoint
    """
    # a = request.get_json(force=True)

    if request.method == 'POST':
        child_form = CreateChildForm(request.form)

        parents = Parent.query.all()
        if not parents:
            # Return and show an error
            flash("Error: Please add a parent First", category='error')
            return redirect(url_for('campers'))

        # Make Sure groups exits
        groups = CampGroup.query.all()

        if not groups:
            # Return and show an error
            flash("Error: Please add a group First", category='error')
            return redirect(url_for('campers'))

        camper = Camper()
        camper.first_name = child_form.first_name.data
        camper.last_name = child_form.last_name.data
        camper.birth_date = datetime.strptime(child_form.birth_date._value(), "%d %B, %Y")
        camper.grade = child_form.grade.data
        camper.gender = child_form.gender.data
        camper.medical_notes = child_form.medical_notes.data

        camper.parent_id = int(child_form.parent.data)
        parent = Parent.query.filter_by(id=camper.parent_id).first()
        # parent = camper.parent

        if child_form.street_address.data == "":
            # No address supplied, set address to parent address
            camper.street_address = parent.street_address
            camper.city = parent.city
            camper.state = parent.state
            camper.zip_code = parent.zip_code

        else:
            camper.street_address = child_form.street_address.data
            camper.city = child_form.city.data
            camper.state = child_form.state.data
            camper.zip_code = child_form.zipcode.data

        camper.is_active = False
        camper.group_id = int(child_form.group.data)

        # camper.parent = parent

        db.session.add(camper)
        db.session.commit()

        # group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))
        # parent_id = db.Column(db.Integer(), db.ForeignKey('parent.id'))

        # tell template to default to parent tab
        flash("campers", category='tab_choice')
        return redirect(url_for('campers'))

    elif request.method == 'DELETE':
        try:
            camper_id = request.json['camper_id']
            camper = Camper.query.filter_by(id=camper_id).first()
            db.session.delete(camper)
            db.session.commit()
        except Exception:
            return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

    elif request.method == "PATCH":
        # Patch handles case when camper enrollment status is changed
        camper_id = request.json['camper_id']
        camper_status = request.json['status']

        camper = Camper.query.filter_by(id=camper_id).first()
        camper.is_active = camper_status

        db.session.commit()
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/manage/campgroup', methods=['POST', 'DELETE'])
@login_required
@requires_roles(Role.admin)
def submit_camp_group_management():
    """Camp Group Management Endpoint

        Endpoint for administrator to edit, add and delete
        camp groups

        Returns:
            on valid POST request, returns a redirect to url_for('campers')
            on valid DELETE, return json with success flag
            on invalid POST/DELETE request, return json with failure flag

        .. note::
            Only authenticated admins can access this endpoint
    """
    # a = request.get_json(force=True)

    if request.method == 'POST':
        form = request.form
        name = form["groupName"]
        color = form["color"]

        group = CampGroup(name=name, color=color)
        db.session.add(group)
        db.session.commit()

        # tell template to default to campgroup tab
        flash("groups", category='tab_choice')
        return redirect(url_for('campers'))

    elif request.method == 'DELETE':

        try:
            group_id = request.json['group_id']

            if group_id == 1 and CampGroup.query.filter_by(name='none', id=1).first():
                return jsonify({'success': False, 'msg': 'Error: Cannot Delete Default Group'}), \
                       400, {'ContentType': 'application/json'}

            camp_group = CampGroup.query.filter_by(id=group_id).first()
            db.session.delete(camp_group)
            db.session.commit()

        except Exception:
            return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/saveEvent', methods=['POST', 'PUT', 'DELETE'])
@login_required
@requires_roles(Role.admin)
def submit_handler():
    """Camp Event Management Endpoint

        Endpoint for administrator to create, edit and delete
        camp events on the Full Calendar Schedule

        Returns:
            on valid POST request, returns a json with success flag and color to render
            event it. This color corresponds to the event's camp group's color
            on valid PUT/DELETE request, returns a json with success flag

        .. note::
            Only authenticated admins can access this endpoint
    """
    # a = request.get_json(force=True)

    if request.method == 'POST':
        event_data = request.json

        # save event to database
        event = CampEvent.convert_calevent_to_campevent(event_data)
        db.session.add(event)
        db.session.commit()

        # query database for group color and event id
        color = event.campgroup.color
        event_id = event.id

        return jsonify({'msg': 'success', 'color': color, 'id': event_id})

    elif request.method == 'PUT':
        print("Received a PUT request of event")
        event_data = request.json

        event_id = int(event_data['id'])
        new_title = event_data['title']
        new_start = CampEvent.convert_iso_datetime_to_py_datetime(event_data['start'])
        new_end = CampEvent.convert_iso_datetime_to_py_datetime(event_data['end'])
        new_group_id = int(event_data['group_id'])

        CampEvent.query.filter_by(id=event_id).update({'title': new_title, 'start': new_start,
                                                       'end': new_end, 'group_id': new_group_id})
        db.session.commit()

        return jsonify({'msg': 'success'})

    elif request.method == 'DELETE':
        print('Received a Delete Request')
        event_data = request.json
        event_id = int(event_data['id'])

        event = CampEvent.query.filter_by(id=event_id).one()
        db.session.delete(event)
        db.session.commit()

        return jsonify({'msg': 'success'})


@app.route('/getCampEvents', methods=['GET'])
@login_required
@requires_roles(Role.admin)
def get_camp_events():
    """Get Camp Events Endpoint

        Endpoint to retrieve all camp events saved in db. Full Calendar
        calls this endpoint with a start and end argument representing
        the range of dates for which to get events for

        Returns:
            a list of all camp events in db as json

        .. note::
            Only authenticated admins can access this endpoint
    """
    start = request.args.get('start')  # get events on/after start
    end = request.args.get('end')  # get events before/on end

    event_schema = CampEventSchema(many=True)
    events = CampEvent.query.all()  # get all data for now

    for event in events:
        event.add_color_attr()

    result = event_schema.dump(events).data

    return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Endpoint

        Endpoint to login to Camper+ Application

        Returns:
            on GET request/invalid POST (failed authentication), returns rendered login.html page
            on successful POST, i.e successful authentication, returns redirect to url_for('campers')
            or url_for('parent_enrollments') if user is admin or parent respectively
    """

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form, error='Username or Password is invalid')
        else:
            email = form.email.data
            password = form.password.data
            registered_user = User.query.filter_by(email=email.lower()).first()
            if registered_user and registered_user.check_password(password):
                # log the user In
                login_user(registered_user)
                if registered_user.role is Role.parent:
                    return redirect(url_for('parent_enrollments'))
                elif registered_user.role is Role.admin:
                    return redirect(url_for('campers'))
            else:
                return render_template('login.html', form=form,
                                       error='Username or Password is invalid')

    elif request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role is Role.parent:
                return redirect(url_for('parent_enrollments'))
            elif current_user.role is Role.admin:
                return redirect(url_for('campers'))

        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """Log out Endpoint

        Logs out current user

        Returns:
            a redirect to url_for('index'), i.e Homepage
    """
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    """Set Flask Global User

        sets flask global user to current user

        .. note::
            this function is run before every request
    """
    g.user = current_user


@app.before_request
def update_forms():
    """Update Flask Forms

        Updates CreateChildForm's select Field with current groups and parents

        .. note::
            this function is run before every request to make sure recently created
            parents and groups are in the CreateChildForm
    """
    _groups = CampGroup.query.order_by(CampGroup.name).all()
    _group_choices = [(group.id, group.name.capitalize()) for group in _groups]
    CreateChildForm.group = SelectField(label='Group', choices=_group_choices,
                                        validators=[DataRequired("Please select a group.")])

    _parents = Parent.query.order_by(Parent.last_name).all()
    _parent_choices = [(parent.id, "{}, {}".format(
        parent.last_name.capitalize(), parent.first_name.capitalize())) for parent in _parents]

    CreateChildForm.parent = SelectField(label='Parent', choices=_parent_choices,
                                         validators=[DataRequired("Please select a Parent")])


@app.before_request
def create_default_group():
    """Create Default Group

        Creates a default group called 'none' for campers 'without a group'

        .. note::
            this function is run before every request to make sure a group
            exists for camper's without groups
    """
    if not CampGroup.query.filter_by(name='None').first():
        default_group = CampGroup('None', 'blue')
        db.session.add(default_group)
        db.session.commit()
