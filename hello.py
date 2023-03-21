from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Witaj, świecie!</h1>'

@app.route('/user/<name>')
def user(name):
    user_agent = request.headers.get('User-Agent')
    return '<h1>Witaj, {}!</h1><br><h2>Twoją przeglądarką jest {}.'.format(name, user_agent)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )