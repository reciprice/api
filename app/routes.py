from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
app = Flask(__name__)

bp = Blueprint('routes', __name__, url_prefix='/test')

@bp.route('/hello')
def hello_world():
    return 'Hello, World!'