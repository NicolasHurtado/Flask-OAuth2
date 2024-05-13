# main.py
from flask import Flask, redirect
from src.services import auth_services, main_services
from src.database.database import db, migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_services.main)
app.register_blueprint(main_services.main)

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()
    app.run(debug=True)



# import os
# import pathlib

# import requests
# from flask import Flask, session, abort, redirect, request
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# import google.auth.transport.requests

# app = Flask("Google Login App")
# app.debug = True
# app.secret_key = "nicolas_hurtado_c"

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# GOOGLE_CLIENT_ID = "575958578293-j02g14igrc1u33ren76mlbogeqh4usuk.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
#     redirect_uri="http://127.0.0.1:5000/callback"
# )


# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()

#     return wrapper


# @app.route("/login")
# def login():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)


# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)

#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!

#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)

#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )

#     print('id_info',id_info)
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     session["img"] = id_info.get("picture")
#     return redirect("/protected_area")


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")


# @app.route("/")
# def index():
#     return "Hello World <a href='/login'><button>Login</button></a>"


# @app.route("/protected_area")
# @login_is_required
# def protected_area():
#     return (f"Hello {session['name']}! "
#             f"<div><p>Google Profile Picture: </p>"
#             f"<img src={session['img']}></img> </div><br>"
#             "<a href='/logout'><button>Logout</button></a>"
#             )


# if __name__ == "__main__":
#     app.run(debug=True)
