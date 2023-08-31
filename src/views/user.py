from flask import jsonify, request
from src.models.user import User
from config import SessionLocal

db = SessionLocal()


def test():
    new_user = User(email='john@example.com', password='vishal')
    db.add(new_user)
    db.commit()


def create_user():
    try:
        data = request.json
        if "email" in data and "password" in data:
            email = data["email"]
            password = data["password"]
            # Here you can insert the user data into your database or perform other actions
            new_user = User(email=email, password=password)
            db.add(new_user)
            db.commit()
            return jsonify({"message": "User created successfully"})
        else:
            return jsonify({"error": "Invalid data format"})
    except Exception as e:
        return jsonify({"error": str(e)})