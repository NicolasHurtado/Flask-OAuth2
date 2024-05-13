# main.py
from flask import Flask, redirect
from src.services import auth_services, main_services
from src.database.database import db, migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_services.main)
app.register_blueprint(main_services.main)

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
