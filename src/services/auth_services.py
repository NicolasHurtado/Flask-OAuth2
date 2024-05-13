# services.py
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask import session, abort, request, redirect, Blueprint
from src.database.database import db
from src.models.models import User

main = Blueprint('auth_services', __name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Obtener la ruta absoluta del directorio actual (donde está el archivo auth_services.py)
current_dir = os.path.abspath(os.path.dirname(__file__))

# Navegar a la ubicación del archivo client_secret.json (en la raíz del proyecto)
client_secrets_file = os.path.join(current_dir, "../../client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@main.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@main.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=flow.client_config['client_id']
    )

    print('id_info',id_info)
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["img"] = id_info.get("picture")
     # Crear un nuevo usuario en la base de datos si no existe
    user = User.query.filter_by(google_id=id_info.get("sub")).first()
    if not user:
        new_user = User(google_id=id_info.get("sub"), name=id_info.get("name"), img=id_info.get("picture"))
        db.session.add(new_user)
        db.session.commit()
    return redirect("/protected_area")


@main.route("/logout")
def logout():
    session.clear()
    return redirect("/")