"""Routes for Camper+ app."""

from camperapp import app
from camperapp.models import db, CampEvent, CampGroup, CampEventSchema, Admin

from flask import render_template, session, redirect, url_for
from flask import jsonify
from flask import request
from camperapp.forms import SignupFormAdmin, LoginForm, ChildEnrollmentForm, CreateParentForm, CreateChildForm



@app.route('/', methods=['GET'])
def index():
    """View displays the homepage"""
    form = LoginForm()
    return render_template("home.html", form=form)


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

    children = [Child(1, 'John Redcorn', 12, 6, 'Falcons','green','Enrolled'), Child(1, 'Bobby Hill', 13, 7,
                                                                                     'Dodgers', 'brown', 'Enrolled')]
    return render_template("parent_enrollments.html", children=children)


@app.route('/parent/register', methods=['GET', 'POST'])
def parent_register():
    """View presents a registration form for enrolling a new child"""
    form = ChildEnrollmentForm()
    camp_season = "Summer 2018"
    parent_name = "Jane Armadillo"
    return render_template("parent_register.html", form=form, camp_season=camp_season, parent_name=parent_name)


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
    parent_form = CreateParentForm()
    child_form = CreateChildForm()
    return render_template('admin_manage.html', parent_form=parent_form, child_form=child_form)


@app.route('/manage/parent', methods=['GET', 'POST', 'PUT', 'DELETE'])
def submit_parent_management():
    """EndPoint for Adding, Editing and Deleting a Camper"""
    # a = request.get_json(force=True)
    parent_form = CreateParentForm(request.form)
    child_form = CreateChildForm()

    first_name = parent_form.first_name.data
    last_name = parent_form.last_name.data
    birth_day = parent_form.birth_date._value()
    gender = parent_form.gender.data
    email = parent_form.email.data
    phone = parent_form.phone.data
    street_address = parent_form.street_address.data
    city = parent_form.city.data
    state = parent_form.state.data
    zip_code = parent_form.zipcode.data

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
        new_start = CampEvent.convert_ISO_datetime_to_py_datetime(event_data['start'])
        new_end = CampEvent.convert_ISO_datetime_to_py_datetime(event_data['end'])
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
    """Camp Admin and Parent login endpoint"""
    if 'email' in session:
        return redirect(url_for('campers'))
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
            else:
                return redirect(url_for('login'))

            userparent = Parent.query.filter_by(email=email).first()
            if userparent is not None and userparent.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('parent_account'))
            else:
                return redirect(url_for('login'))



    elif request.method == 'GET':
        return render_template('login.html', form=form)



@app.route('/signupAdmin', methods=['GET', 'POST'])
def signupAdmin():
    if 'email' in session:
        return redirect(url_for('campers'))
    form = SignupFormAdmin()

    if request.method == 'POST':
        if form.validate() == False:
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

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))
