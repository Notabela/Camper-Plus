"""Run flask App Locally in Debug Mode"""

from camperapp import app, db

if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(debug=True)
