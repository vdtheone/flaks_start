from flask import Flask
from flask_mail import Mail

from src.router.user_router import user_bp

app = Flask(__name__)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "vishal262.rejoice@gmail.com"
app.config["MAIL_PASSWORD"] = "tkrkeoofhvxijxqm"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEBUG"] = False
mail = Mail(app)


app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=True)
