"""Routes for Camper+ app."""

from datetime import datetime
from camperapp import app
from camperapp.models import db, CampEvent, CampGroup, CampEventSchema, Admin, Camper, Parent
from camperapp.forms import SignupFormAdmin, LoginForm, \
    ChildEnrollmentForm, CreateParentForm, CreateChildForm
from flask import render_template, session, redirect, url_for, jsonify, request
from wtforms import SelectField
from wtforms.validators import DataRequired


@app.route('/', methods=['GET'])
def index():
    """View displays the homepage"""
    form = LoginForm()
    return render_template("home.html", form=form)


@app.route('/faq', methods=['GET'])
def faq():
    """View displays the FAQ page"""
    return render_template("faq.html")


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    """View displays the schedule-making page"""
    groups = CampGroup.query.all()
    return render_template("admin_schedule.html", groups=groups)


@app.route('/parent/schedule', methods=['GET'])
def parent_schedule():
    """View displays the schedule of Parent's enrolled children"""
    # Mock Children - to be replaced by real Campers
    class Child:
        def __init__(self, uid, name, color):
            self.id = uid
            self.color = color
            self.name = name

    children = [Child(1, 'John Redcorn', 'green'), Child(2, 'Bobby Hill', 'brown')]
    return render_template("parent_schedule.html", children=children)


@app.route('/parent/enrollments', methods=['GET'])
def parent_enrollments():
    """View displays the enrolled children of a parent"""
    # Mock Children - to be replaced by real Campers
    class Child:
        def __init__(self, uid, name, age, grade, group, color, status):
            self.id = uid
            self.age = age
            self.grade = grade
            self.group = group
            self.group_color = color
            self.status = status
            self.name = name

    children = [Child(1, 'John Redcorn', 12, 6, 'Falcons', 'green', 'Enrolled'),
                Child(1, 'Bobby Hill', 13, 7, 'Dodgers', 'brown', 'Enrolled')]
    return render_template("parent_enrollments.html", children=children)


@app.route('/parent/register', methods=['GET', 'POST'])
def parent_register():
    """View presents a registration form for enrolling a new child"""
    form = ChildEnrollmentForm()
    camp_season = "Summer 2018"
    parent_name = "Jane Armadillo"
    return render_template("parent_register.html", form=form,
                           camp_season=camp_season, parent_name=parent_name)


@app.route('/parent/account', methods=['GET'])
def parent_account():
    """View displays the parent's account settings"""
    return "Hello World"


@app.route('/parent/forms', methods=['GET'])
def parent_forms():
    """View displays the pending forms of the parent"""
    return "Hello World"


@app.route('/campers', methods=['GET'])
def campers():
    """View displays the camper organization page"""

    # Dynamically Add the Groups to the the Child Form
    _groups = CampGroup.query.order_by(CampGroup.name).all()
    _group_choices = [(group.id, group.name) for group in _groups]
    CreateChildForm.group = SelectField(label='Group', choices=_group_choices,
                                        validators=[DataRequired("Please select a group.")])

    parent_form = CreateParentForm()
    child_form = CreateChildForm()

    # Get all Campers
    all_campers = Camper.query.order_by(Camper.last_name).all()
    all_parents = Parent.query.order_by(Parent.last_name).all()
    all_groups = CampGroup.query.order_by(CampGroup.name).all()

    return render_template('admin_manage.html', groups=all_groups, parents=all_parents,
                           campers=all_campers, parent_form=parent_form, child_form=child_form)


@app.route('/manage/parent', methods=['POST', 'PUT', 'DELETE'])
def submit_parent_management():
    """EndPoint for Adding, Editing and Deleting a Camper"""
    # a = request.get_json(force=True)
    parent_form = CreateParentForm(request.form)
    # child_form = CreateChildForm()
    # _groups = CampGroup.query.order_by(CampGroup.name).all()
    # _group_choices = [(group.id, group.name) for group in _groups]
    # child_form.group = SelectField(label='Group', choices=_group_choices)

    # Add Validation Later
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

    return redirect(url_for('campers'))


@app.route('/manage/camper', methods=['POST'])
def submit_camper_management():
    """EndPoint for Adding, Editing and Deleting a Camper"""
    # a = request.get_json(force=True)
    child_form = CreateChildForm(request.form)  # Needs Testing

    # Add Validation Later
    camper = Camper()
    camper.first_name = child_form.first_name.data
    camper.last_name = child_form.last_name.data
    camper.birth_date = datetime.strptime(child_form.birth_date._value(), "%d %B, %Y")
    camper.grade = child_form.grade.data
    camper.gender = child_form.gender.data
    camper.medical_notes = child_form.medical_notes.data
    camper.street_address = child_form.street_address.data
    camper.city = child_form.city.data
    camper.state = child_form.state.data
    camper.zip_code = child_form.zipcode.data

    camper.is_active = False
    camper.group_id = int(child_form.group.data)

    # Search for Parent and Populate field
    parent = Parent.query.filter_by(first_name=child_form.parent_first_name.data,
                                    last_name=child_form.parent_last_name.data).first()
    if not parent:
        return "<h1>Error</h1>"

    camper.parent = parent

    db.session.add(camper)
    db.session.commit()

    # group_id = db.Column(db.Integer(), db.ForeignKey('campgroup.id'))
    # parent_id = db.Column(db.Integer(), db.ForeignKey('parent.id'))

    return redirect(url_for('campers'))


@app.route('/manage/campgroup', methods=['POST'])
def submit_camper_group_management():
    """EndPoint for Adding, Editing and Deleting a Camper"""
    # a = request.get_json(force=True)
    form = request.form
    name = form["groupName"]
    color = form["color"]

    group = CampGroup(name=name, color=color)
    db.session.add(group)
    db.session.commit()

    return redirect(url_for('campers'))


@app.route('/saveEvent', methods=['POST', 'PUT', 'DELETE'])
def submit_handler():
    """EndPoint for creating, updating and deleting Calendar Events"""
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
def get_camp_events():
    """Endpoint for retrieving saved CampEvents"""
    start = request.args.get('start')  # get events on/after start
    end = request.args.get('end')  # get events before/on end
    print(start, end)

    event_schema = CampEventSchema(many=True)
    events = CampEvent.query.all()  # get all data for now

    for event in events:
        event.add_color_attr()

    result = event_schema.dump(events).data

    return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Camp Admin and Parent login endpoint
    if 'email' in session:
        return redirect(url_for('campers'))"""
    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data

            useradmin = Admin.query.filter_by(email=email).first()
            if useradmin is not None and useradmin.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('campers'))

            userparent = Parent.query.filter_by(email=email).first()
            if userparent is not None and userparent.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('parent_enrollments'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/signupAdmin', methods=['GET', 'POST'])
def signup_admin():
    """Sign up administrator"""
    form = SignupFormAdmin()

    if request.method == 'POST':
        if not form.validate():
            return render_template('signupAdmin.html', form=form)
        else:
            email = form.email.data
            user = Admin.query.filter_by(email=email).first()
            if user is not None:
                return redirect(url_for('login'))
            else:
                newuser = Admin(form.name.data, form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()

                session['email'] = newuser.email
                return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('signupAdmin.html', form=form)


@app.route('/dev_docs', methods=['GET'])
def documentation():
    """Sphinx documentation"""
    return render_template('docindex.html')


@app.route("/logout")
def logout():
    """Logout Admin or Parent"""
    session.pop('email', None)
    return redirect(url_for('index'))
