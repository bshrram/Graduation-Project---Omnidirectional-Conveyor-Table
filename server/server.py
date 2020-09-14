from flask import Flask, send_from_directory
from flask import render_template
from flask import request

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

import sys
sys.path.insert(3, './')

from followBezier import followBezier
from boxesClassifications import classifyBoxes
from shortestPath import followshortestPath
from table import Table
from data.cellDatabase import *


myTable = Table(cellDatabase)



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

    followBezier(myTable, points)
    return p1+p2+cp1+cp2

@app.route('/classify',methods = ['GET'])
def classify():
    type1 = request.args.get('type1', '')
    type2 = request.args.get('type2', '')
    classifyBoxes(myTable, [type1, type2])
    return redirect("http://127.0.0.1:5000", code=302)

@app.route('/shortestPath',methods = ['GET'])
def followShortestPath():
    cell1Row = request.args.get('beginCellRow', '')
    cell1Col = request.args.get('beginCellColumn', '')
    cell2Row = request.args.get('endCellRow', '')
    cell2Col = request.args.get('endCellColumn', '')

    followshortestPath(myTable, [cell1Row, cell1Col], [cell2Row, cell2Col])
    return redirect("http://127.0.0.1:5000", code=302)





if __name__ == '__main__':
   app.run()

