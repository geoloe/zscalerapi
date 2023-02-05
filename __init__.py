from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(24))
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://zscaler:start123@localhost:3306/zscaler_automation"
    #app.run(host='1.16.6.100')
    #'sqlite:///db.sqlite'
    
    with app.app_context():

        # initialize db tables and add default values
        @app.before_first_request
        def create_tables():
            db.create_all()
            from .models import init_defaults
            init_defaults()
        
        @app.before_request
        def make_session_permanent():
            session.permanent = True 
        
        # Close open connections if inactive
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db.session.remove()

        db.init_app(app)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        from .models import User, Kunde

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # blueprint for optional features parts of app
        from .extras import extras as extras_blueprint
        app.register_blueprint(extras_blueprint)
        

    return app

### initialize flask app ###
if __name__ == '___main___':
    app = create_app()
    app.run(host='1.16.6.100')