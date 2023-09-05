import os
from hashlib import sha256
from random import randint

import jwt
from flask import jsonify, request
from flask_mail import Message
from sqlalchemy.exc import IntegrityError

import app
from config import SessionLocal
from src.models.user import User
from src.utils.access_token_requied import required_access_token
from src.utils.generate_jwt import create_access_token

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


db = SessionLocal()


def hash_password(password: str):
    hash_obj = sha256()
    hash_obj.update(password.encode("utf-8"))
    hashed_password = hash_obj.hexdigest()
    return hashed_password


def create_user():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "Invalid data format"})

        otp = randint(000000, 999999)

        email = data.get("email")
        password = data.get("password")

        if not email and not password:
            return jsonify({"error": "Email, password, or OTP is missing"}), 400

        # Send OTP via email
        send_otp_email(email, otp)

        password = hash_password(password)

        new_user = User(email=email, password=password, otp=otp)
        db.add(new_user)
        db.commit()
        return jsonify({"message": "User created successfully"})

    except IntegrityError:
        return jsonify({"error": "Email already exist"})

    except Exception as e:
        return jsonify({"error": str(e)})


# Send OTP via email
def send_otp_email(recipient_email, otp):
    try:
        msg = Message(
            "OTP", sender="vishal262.rejoice@gmail.com", recipients=[recipient_email]
        )
        msg.body = str(otp)
        app.mail.send(msg)
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")


def login():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "Invalid data format"}), 400

        email = data.get("email")
        password = data.get("password")
        password = hash_password(password)
        otp_return = data.get("otp")

        if not email or not password or not otp_return:
            return jsonify({"error": "Email, password, or OTP is missing"}), 400

        user_details = (
            db.query(User)
            .filter_by(email=email, password=password, otp=otp_return)
            .first()
        )

        if user_details is None:
            return jsonify({"error": "email or passworrd or otp is wrong"}), 404

        if not user_details.is_varified:
            user_details.is_varified = True
            db.commit()
            db.refresh(user_details)

        user_dict = {"id": user_details.id, "email": user_details.email}
        access_token = create_access_token(user_dict)

        return jsonify({"message": "Login successful", "token": access_token})

    except Exception as e:
        return jsonify({"error": str(e)})


@required_access_token
def forgot():
    try:
        token = request.headers.get("Authorization").split()
        if not token:
            return jsonify({"error": "token not provided"})
        payload = jwt.decode(token[1], JWT_SECRET_KEY, ALGORITHM)

        user = db.query(User).filter_by(id=payload.get("id")).first()
        if not user:
            return jsonify({"error": "user not found"})

        if not user.is_varified:
            return jsonify({"error": "Login first"})

        otp = randint(000000, 999999)

        send_otp_email(user.email, otp)

        user.otp = otp
        db.commit()
        db.refresh(user)

        return jsonify({"message": "sent otp to your email id"})

    except Exception as e:
        return jsonify({"error": str(e)})


def get_jwt_identity():
    try:
        token = request.headers.get("Authorization").split()
        if not token:
            return jsonify({"error": "token not provided"})
        payload = jwt.decode(token[1], JWT_SECRET_KEY, ALGORITHM)
        return payload.get("id")
    except Exception as e:
        return jsonify({"error": str(e)})


@required_access_token
def reset_password():
    try:
        current_user_id = get_jwt_identity()
        user = db.query(User).filter_by(id=current_user_id).first()

        data = request.json
        if not data:
            return jsonify({"error": "Invalid data format"}), 400

        password = data.get("password")
        otp_return = data.get("otp")

        if not password or not otp_return:
            return jsonify({"error": "Please provide both password and OTP"}), 400

        if user.otp != otp_return:
            return jsonify({"error": "Invalid OTP"}), 400

        # Hash the new password
        hashed_password = hash_password(password)
        user.password = hashed_password

        db.commit()
        db.refresh(user)

        return jsonify({"message": "Password reset successfully"})

    except Exception:
        return jsonify({"error": "An error occurred while resetting the password"}), 500
