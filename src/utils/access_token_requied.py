from flask import jsonify, request
import os
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def required_access_token(func):
    def inner(*args):
        try:
            token = request.headers.get("Authorization").split()

            if not token:
                return jsonify({"message": "Token is missing !!"}), 401
            token = token[1]

            jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        except InvalidSignatureError:
            return jsonify({"error": "Signature verification failed"})
        except ExpiredSignatureError:
            return jsonify({"error": "Token Expired"})
        except Exception as e:
            return jsonify({"error": str(e)})
        return func(*args)

    return inner
