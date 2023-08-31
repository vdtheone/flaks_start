from flask import Blueprint

from src.views.auth import test


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/') 
def index():	
    data = test()
    return data	


