"""Run flask App Locally in Debug Mode"""

from camperapp import app, db

if __name__ == "__main__":
    app.run(debug=True)
