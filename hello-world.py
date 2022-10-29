#!/usr/bin/python
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        return """<h1 style="font-size: 60px;line-height: 60px;">Hello World!"""

    return ""

if __name__ == '__main__':
    app.run(host="localhost", port="10000", debug=True)
