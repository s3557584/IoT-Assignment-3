"""
Task A: API

Written by:Ching Loo(s3557584)

Test API
"""
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
def index():
    """
    Display users
    """
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/user")
    data = json.loads(response.text)

    return render_template("user.html", user = data)

@site.route("/car")
def vehicle():
    """
    Display Vehicles
    """
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/vehicle")
    data = json.loads(response.text)

    return render_template("cars.html", user = data)
