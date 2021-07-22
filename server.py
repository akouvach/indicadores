from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello</h1>'


@app.route('/<name>')
def name(name):
    return '<h1>Hello {}</h1>'.format(name)