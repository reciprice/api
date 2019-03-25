from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
import requests

WALLMART_API_KEY = ""

app = Flask(__name__)

bp = Blueprint('routes', __name__, url_prefix='/api/v1/')

def get_wallmart_ingredients_by_recipe(recipe):
    arrray = []
    for val in recipe:
        print(val)
        r = requests.get("http://api.walmartlabs.com/v1/search?apiKey=" + WALLMART_API_KEY + "&categoryId=976759_1071964_976793&query=" + val['ingredient'])
        result = r.json()
        if result['numItems'] != 0:
            tmp = {}
            tmp['name'] = result['items'][0]['name']
            tmp['url'] = result['items'][0]['productUrl']
            arrray.append(tmp)
    return arrray

@bp.route('/hello')
def hello_world():
    return 'Hello, World!'

@bp.route("/random")
def random():
    r = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    result = r.json()
    response = {}
    response['ingredients'] = []
    i = 1
    while (i != 20 and result['meals'][0]['strIngredient' + str(i)] != ""):
        tmp = {}
        tmp['ingredient'] = result['meals'][0]['strIngredient' + str(i)]
        tmp['mesures'] = result['meals'][0]['strMeasure' + str(i)]
        response['ingredients'].append(tmp)
        i += 1 
    response['cart'] = {}
    response['cart']['wallmart'] = get_wallmart_ingredients_by_recipe(response['ingredients'])
    response['name'] = result['meals'][0]['strMeal']
    response['img'] = result['meals'][0]['strMealThumb']
    response['video'] = result['meals'][0]['strYoutube']
    response['instructions'] = result['meals'][0]['strInstructions'] 
    return jsonify(response)
