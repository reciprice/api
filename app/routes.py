from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
import requests

WALLMART_API_KEY = "yzrgcfx54sxhvdc8s88e25q5"

app = Flask(__name__)

bp = Blueprint('routes', __name__, url_prefix='/api/v1/')


@bp.route('/hello')
def hello_world():
    return 'Hello, World!'

@bp.route("/random")
def random():
    r = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    result = r.json()
    name = result['meals'][0]['strMeal']
    return name