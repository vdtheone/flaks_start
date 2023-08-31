from flask import Flask, render_template
from src.router.auth_router import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug = True)


