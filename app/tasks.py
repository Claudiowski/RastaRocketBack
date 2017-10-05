from flask.ext.mail import Mail
from flask import current_app
from . import create_celery_app

celery = create_celery_app()


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with current_app.app_context():
        current_app.send(msg)
