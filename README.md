## Camper+

A wesbite to ease the work of camp administrators and the lives of parents

### Usage (Command Line)

##### Set up Python Virtual Environment
    pip install virtualenv
    virtualenv .venv
    source .venv/bin/activate

##### Set up App Environment
    python setup.py install
    pip install -r requirements.txt
    
##### Run Tests
    pip install pytest
    pytest (in base directory)
    
##### Code Coverage
    pip install pytest-cov
    pytest --cov=camperapp tests/ (in base directory)
    
##### Pylint Score
    pip install pylint
    pylint camperapp (in base directory)

##### Run Application (debug Mode)
    python application.py
    Runs on > 127.0.0.1:5000

##### Live Application at
    https://camperapp.herokuapp.com
    admin_sample_login   - email: admin@camperapp.com  password: Notabela
    parent_sameple_login - email: parent@camperapp.com password: Notabela
   
##### Generating Requirements and PipFiles
    Generate requirements file: pip freeze > requirements.txt
    Generate Pipfile/Lockfile from requirements: pipenv install -r requirements.txt
    
##### Deploying to Heroku

