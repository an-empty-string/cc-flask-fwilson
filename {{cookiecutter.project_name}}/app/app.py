import os
import playhouse.db_url
import utils

from flask import Flask, flash, redirect, render_template, request, session, url_for
import models

auth = utils.SSOAuthenticator("{{ cookiecutter.auth_endpoint }}")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")

@app.before_request
def before_request():
    utils.set_csrf()
    models.database.connect()

@app.after_request
def after_request(resp):
    models.database.close()
    return resp

@app.route("/")
@utils.require_login
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    return redirect(auth.request_url(url_for("verify", _next=request.args.get("_next", "/"), _external=True)))

@app.route("/verify/")
def verify():
    result = auth.verify(request.args.get("token", ""), request.url)
    if result:
        session["username"] = result["username"]
        flash("Login successful.")
        return redirect(request.args.get("_next", "/"))
    return "There was a problem with your authentication token; please try that again.", 401

if __name__ == "__main__":
    app.run(port=5050, debug=True)
