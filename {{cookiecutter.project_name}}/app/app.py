import os
import playhouse.db_url

from . import utils, models, skel
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")

app.register_blueprint(skel.blueprint)

@app.route("/")
@utils.require_login
def index():
    return render_template("index.html")
