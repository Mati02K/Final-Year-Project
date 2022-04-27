from flask import Flask,request
app = Flask(__name__)


@app.route('/')
def intro():
    return 'Hi, Welcome to Transbot app developed by Mathesh'

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.route('/buy/<string:pname>',methods = ['POST'])
def login(pname):
    seen = {}
    # return request.args.get('pname', '')
    seen['mathesh'] = {"Name" : "Mathesh", "Age" : 21}
    seen['allen'] = {"Name": "Allen", "Age": 20}
    if request.method == 'POST':
        return seen[pname]