from flask import render_template, request, redirect
from app import app, db
from app.models import User
import requests
import secrets
import json

import logging
from logging.handlers import RotatingFileHandler

from time import strftime
import traceback



from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger('tdm')
logger.setLevel(logging.ERROR)
logger.addHandler(handler)


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per minute", "1 per second"],
)

jedi = "of the jedi"




def get_key(key):

    key = User.query.filter_by(key=key).first()

    return key


def match_api_keys(key):

   if key is None :
      return False
   api_key = get_key(key)
   if api_key is None:
      return False
   elif api_key.key == key:
      return True
   return False

'''def require_app_key(f):

   def decorated(*args):
      if match_api_keys(request.args.get('key')):
         return f(*args)
      else:
         return 'key no permitida'
      return decorated'''


@app.route('/price')
@limiter.limit("10/minute")
def user():


    symbol = request.args.get('symbol')

    key = request.args.get('key')

    if symbol and key:

        if match_api_keys(key):

            response = requests.get(
                    'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=compact&apikey=X86NOH6II01P7R24'.format(symbol))

            resultado = response.content

            my_json = resultado.decode('utf8').replace("'", '"')

            data = json.loads(my_json)

            resultado = data['Time Series (Daily)']

            s = json.dumps(resultado)

            return s
        else:
            error = {'error 404': 'la key no esta permitida, registrate para obtener una.'}

            s2 = json.dumps(error)

            return s2
    else:
        return json.dumps({'error 404': 'falta parametros de key y/o symbol.'})



@app.route('/')
@app.route('/index')
def index():

    user = User.query.all()
    return render_template('index.html', user=user)

@app.route('/add', methods=['POST'])
def add():

    if request.method == 'POST':
        form = request.form
        print(form.get('nombre'))
        nombre = form.get('nombre')
        apellido = form.get('apellido')
        email = form.get('email')
        if nombre and apellido and email:

            key = secrets.token_urlsafe(16)

            user = User(nombre=nombre, apellido=apellido, email=email, key=key)

            db.session.add(user)
            db.session.commit()
            return render_template('key.html', key=key)

    return json.dumps({'error 404': 'no se pudo acceder a la url'})

@app.route('/update/<int:id>')
def updateRoute(id):

    if not id or id != 0:
        user = User.query.get(id)
        if user:
            return render_template('update.html', user=user)

    return "of the jedi"

@app.route('/update', methods=['POST'])
def update():
    form = request.form
    id = form.get('id')

    if not id or id != 0:
        user = User.query.get(id)
        if user:
            user.nombre = form.get('nombre')
            user.apellido = form.get('apellido')
            user.email = form.get('email')
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/addUser')
def addUser():

    return render_template('addUser.html')


@app.after_request
def after_request(response):
    if request.full_path == '/price?' or '/price?symbol' or '/price?key' or '/price?key&symbol':
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,request.full_path, response.status)
        return response
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.status_code
