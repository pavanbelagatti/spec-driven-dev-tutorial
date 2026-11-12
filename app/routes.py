"""HTTP endpoints for the notification service."""

import os

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("notifications", __name__)


def _email_from_request():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        return None
    return email


@bp.get("/health")
def health():
    return jsonify(status="ok", version=os.environ.get("APP_VERSION", "dev"))


@bp.post("/password-reset")
def password_reset():
    email = _email_from_request()
    if email is None:
        return jsonify(error="A valid email is required"), 400

    # NOTE: there is no rate limit here yet. Anyone can call this endpoint
    # as often as they like. See the "Rate-limit password reset emails" spec.
    current_app.config["EMAIL_SENDER"].send(
        to=email, kind="password_reset", subject="Reset your password"
    )
    # Same response whether or not the account exists, so the endpoint
    # can't be used to discover which emails are registered.
    return jsonify(message="If that account exists, a reset email is on its way."), 202


@bp.post("/welcome-email")
def welcome_email():
    email = _email_from_request()
    if email is None:
        return jsonify(error="A valid email is required"), 400

    current_app.config["EMAIL_SENDER"].send(
        to=email, kind="welcome", subject="Welcome aboard"
    )
    return jsonify(message="Welcome email sent."), 202
