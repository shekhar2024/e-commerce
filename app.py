from flask import Flask
from applications.database import db
from applications.models import User
from applications.config import localDevelopmentConfig
from applications.resources import api
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)

    app.config.from_object(localDevelopmentConfig)

    db.init_app(app)
    api.init_app(app)

    app.app_context().push()

    return app

app = create_app()

with app.app_context():
    db.create_all()  

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            name="Admin",
            email="admin@gmail.com",
            password_hash=generate_password_hash("admin"),
            is_admin=True
        )
        db.session.add(admin)

    db.session.commit() 

if __name__ == '__main__':
    app.run()