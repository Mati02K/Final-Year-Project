from get_product import Products
import botocore
import json
from checkout import Checkout
import mysql.connector

try:
    c = Checkout()
    res = c.fetch()
    print(res)
except mysql.connector.Error as e:
    print(e)
