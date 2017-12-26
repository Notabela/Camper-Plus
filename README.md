Camper+
==========

A wesbite to ease the work of camp administrators and the lives of parents

LIVE DEMO
----------------------
[Deployed on Heroku (https://camperapp.herokuapp.com)](https://camperapp.herokuapp.com)

[FAQ (https://camperapp.herokuapp.com/faq)](https://camperapp.herokuapp.com/faq)


Sample Admin Login `email: admin@camperapp.com  password: notabela`

Sample Parent Login `email: parent@camperapp.com password: notabela`


HOW TO USE IT
-------------------
### Checking out and initializing the git repository
    git clone https://github.com/Notabela/Camper-Plus.git
    cd Camper-Plus
    
### Set up Python Virtual Environment
    pip install virtualenv
    virtualenv .venv
    source .venv/bin/activate

### Set up App Environment
    python setup.py install
    pip install -r requirements.txt
    
### Create an admin and parent sign in accounts
To sign in, you'll need to create an admin and/or a parent account

To create an admin account(In ipython in Home Directory):

        ipython
        from camperapp import db, User, Role
        email = 'testadmin@mail.com'
        password = testadmin
        user = User(email, password, Role.admin)
        db.session.add(user)
        db.session.commit()
    
To create a parent account(In ipython in Home Directory):

        from camperapp import db, User, Parent, Role
        email = 'testparent@mail.com'
        password = testparent

        parent = Parent()
        parent.first_name = 'Example'
        parent.last_name = 'Example'
        parent.email = email

        db.session.add(parent)
        db.session.commit()

        user = User(email, password, Role.parent)
        user.parent_id = parent.id
        db.session.add(user)
        db.session.commit()
    
### Run Application Locally (debug Mode)
change db_path in `camperapp/__init.py__` to mock_db_path

    python application.py
    Runs at http://127.0.0.1:5000
    
    
### Developer Documentation
[Developer Docs (https://notabela.github.io/Camper-Plus/)](https://notabela.github.io/Camper-Plus/)


TESTS, PYLINT & COVERAGE
-----------------------------
### Run Tests
    pip install pytest
    pytest (in base directory)
    
### Code Coverage
    pip install pytest-cov
    pytest --cov=camperapp tests/ (in base directory)
    
### Pylint Score
    pip install pylint
    pylint camperapp (in base directory)

