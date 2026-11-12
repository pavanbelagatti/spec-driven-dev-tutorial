"""Notification service: sends transactional emails (password reset, welcome)."""

from flask import Flask

from app.email_sender import FakeEmailSender


def create_app(email_sender=None):
    """Create the Flask app. Tests pass their own sender to inspect sent emails."""
    app = Flask(__name__)
    app.config["EMAIL_SENDER"] = email_sender or FakeEmailSender()

    from app.routes import bp

    app.register_blueprint(bp)
    return app
