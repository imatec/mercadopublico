from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from celery import Celery
# from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
#mail = Mail()

# from config import Config
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    # import here or else manage.py cant update os.environ inside config
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production
        import logging
        from logging.handlers import SysLogHandler
        handler = SysLogHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
    else:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        handler = RotatingFileHandler(
            os.path.join(app.config['LOG_ROOT'], 'app.log'),
            maxBytes=10000,
            backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    # from pprint import pprint
    # pprint(app.logger.handlers)

    # module.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
#    celery.conf.update(app.config)
#    mail.init_app(app)

    @app.route('/')
    def index():
        return jsonify({'response': 'OK'})

#    @babel.localeselector
#    def get_locale():
#        return session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys()))

    app.jinja_env.line_statement_prefix = '#'
    return app

