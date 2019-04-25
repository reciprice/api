from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from . import secret
import json
import requests

app = Flask(__name__)

bp = Blueprint('routes', __name__, url_prefix='/api/v1/')


def get_cart_price(cart):
    price = 0
    for element in cart:
        price = price + element['price']
    return price


def short_url(wallmart_url):
    hed = {'Authorization': 'Bearer ' + secret.BIT_LY_API_KEY}
    data = {'long_url' : wallmart_url}
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(url, json=data, headers=hed)
    res_json = response.json();
    return res_json['link']

def get_wallmart_ingredients_by_recipe(recipe):
    arrray = []
    cart_price = []
    for val in recipe:
        r = requests.get("http://api.walmartlabs.com/v1/search?apiKey=" +
                         secret.WALLMART_API_KEY + "&query=" + val['ingredient'].replace(" ", "+"))
        if (r.status_code == 200):
            result = r.json()
            if result['numItems'] != 0:
                tmp = {}
                tmp['name'] = result['items'][0]['name']
                tmp['url'] = short_url(wallmart_url=result['items'][0]['productUrl'])
                tmp['price'] = result['items'][0]['salePrice']
                arrray.append(tmp)
    return arrray


def format_response(result):
    response = {}
    response['ingredients'] = []
    i = 1
    try:
        while (i != 20 and result['meals'][0]['strIngredient' + str(i)] != ""):
            tmp = {}
            tmp['ingredient'] = result['meals'][0]['strIngredient' + str(i)]
            tmp['mesures'] = result['meals'][0]['strMeasure' + str(i)]
            response['ingredients'].append(tmp)
            i += 1
        response['cart'] = {}
        response['cart']['wallmart'] = get_wallmart_ingredients_by_recipe(
            response['ingredients'])
        response['name'] = result['meals'][0]['strMeal']
        response['img'] = result['meals'][0]['strMealThumb']
        response['video'] = result['meals'][0]['strYoutube'].replace(
            "watch?v=", "embed/")
        response['price'] = get_cart_price(response['cart']['wallmart'])
        response['instructions'] = result['meals'][0]['strInstructions']
        response['error'] = False
    except:
        response['error'] = True
        return response
    return response


@bp.route('/hello')
def hello_world():
    return 'Hello, World!'


@bp.route('/search/<recipe_name>', methods=['GET'])
def search(recipe_name):
    r = requests.get(
        "https://www.themealdb.com/api/json/v1/1/search.php?s=" + recipe_name)
    result = r.json()
    response = format_response(result)
    return jsonify(response)


@bp.route("/random")
def random():
    r = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    result = r.json()
    response = format_response(result)
    return jsonify(response)
