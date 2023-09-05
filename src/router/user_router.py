from flask import Blueprint, Request
from src.views.user import create_user, login, forgot, reset_password


user_bp = Blueprint("user", __name__)


@user_bp.route("/create_user", methods=["POST"])
def user_create():
    data = create_user()
    return data


@user_bp.route("/login", methods=["POST"])
def login_user():
    data = login()
    return data


@user_bp.route("/forgot", methods=["GET"])
def forgot_pass():
    data = forgot()
    return data


@user_bp.route("/reset_pass", methods=["PUT"])
def reset_pass():
    data = reset_password()
    return data
