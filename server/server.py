from flask import Flask, send_from_directory
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

import sys
sys.path.insert(3, './')

from followBezier import followBezier


@app.route('/',methods = ['GET'])
def rend():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/followPath',methods = ['GET'])
def follow():
    p1 = request.args.get('p1', '')
    p2 = request.args.get('p2', '')
    cp1 = request.args.get('cp1', '')
    cp2 = request.args.get('cp2', '')
    points = [p1, cp1, cp2, p2]

    followBezier(points)
    return p1+p2+cp1+cp2


if __name__ == '__main__':
   app.run()

