from flask import Flask, request
from flask_cors import CORS
from email_validator import EmailNotValidError
from exceptionClasses import AuthError
from order import Order
from checkout import Checkout
from get_product import Products
import mysql.connector
from botocore.exceptions import ClientError, ParamValidationError

app = Flask(__name__)
CORS(app) # For Cross Origin Request Shield

@app.errorhandler(404)
def page_not_found(error):
    return 'Wrong Request', 404

@app.route('/retreive',methods = ['POST'])
def retreive():
    try:
        p = Products()
        items = p.scan()
        return items

    except ClientError as error:
        print(error)

    except ParamValidationError as error:
        print('The parameters you provided are incorrect: {}'.format(error))

@app.route('/checkout',methods = ['POST'])
def checkout():
    try:
        name = request.form['name']
        mobno = request.form['mobno']
        email = request.form['email']
        pid = request.form['pid']
        quantity = request.form['quantity']
        amt = request.form['amt']
        location = request.form['location']
        order = Order(name, mobno, email, pid, quantity, amt, location)
        c = Checkout()
        res = c.add(order)
        return res

    except (AuthError, EmailNotValidError, TypeError, mysql.connector.Error) as e:
        print(e)
        return e

@app.route('/update',methods = ['POST'])
def update():
    try:
        c = Checkout()
        res = c.update()
        return res
    except (ClientError, mysql.connector.Error) as e:
        print(e)
        return e

@app.route('/fetch',methods = ['POST'])
def fetch():
    try:
        c = Checkout()
        res = c.fetch()
        return res
    except mysql.connector.Error as e:
        print(e)
        return e