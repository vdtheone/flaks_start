from flask import Blueprint
from src.views.user import create_user, test


user_bp = Blueprint('user', __name__)


@user_bp.route('/') 
def index():	
    test()
    return "data"	


@user_bp.route('/create_user', methods=['POST'])    
def kfj():	
    data = create_user()
    return data
