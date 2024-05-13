from flask import Blueprint, session, jsonify, abort
from .auth_services import login_is_required
from src.models.models import User

main = Blueprint('main_services', __name__)

def login_required():
    if "google_id" not in session:
        abort(401)  # Unauthorized

@main.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

@main.route("/protected_area")
@login_is_required
def protected_area():
    return (f"Hello {session['name']}! "
            f"<div><p>Google Profile Picture: </p>"
            f"<img src={session['img']}></img> </div><br>"
            "<a href='/logout'><button>Logout</button></a>"
            )

@main.route("/users")
def list_users():
    login_required()
    users = User.query.all()
    user_list = [{
        "id": user.id,
        "google_id": user.google_id,
        "name": user.name,
        "img": user.img
    } for user in users]
    return jsonify(user_list)
