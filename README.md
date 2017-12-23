# Camper+

A wesbite to ease the work of camp administrators and the lives of parents

## Application Demo
##### Live Application
    https://camperapp.herokuapp.com
    admin_sample_login   - email: admin@camperapp.com  password: notabela
    parent_sameple_login - email: parent@camperapp.com password: notabela
    
##### FAQ
    https://camperapp.herokuapp.com/faq

## Usage (MacOS)

### Environment
##### Set up Python Virtual Environment
    pip install virtualenv
    virtualenv .venv
    source .venv/bin/activate

##### Set up App Environment
    python setup.py install
    pip install -r requirements.txt
    
##### Run Application Locally (debug Mode)
    change `db_path` in camperapp/__init.py__ to `'sqlite:///./app.db'`
    python application.py
    Runs at http://127.0.0.1:5000
    
### Tests and Linter
##### Run Tests
    pip install pytest
    pytest (in base directory)
    
##### Code Coverage
    pip install pytest-cov
    pytest --cov=camperapp tests/ (in base directory)
    
##### Pylint Score
    pip install pylint
    pylint camperapp (in base directory)
  
### Developer
##### Developer Documentation
    https://camperapp.herokuapp.com/dev_docs

##### Generating Requirements and PipFiles
    Generate requirements file: pip freeze > requirements.txt
    Generate Pipfile/Lockfile from requirements: pipenv install -r requirements.txt
    
##### Deployment on Heroku

    To get this project to work on Heroku, you need to:

    1. comment out db_path in camperapp/__init.py__
    2. comment out python app.config['SQLALCHEMY_DATABASE_URI'] = db_path in camperapp/__init.py__
    
     * More to come

