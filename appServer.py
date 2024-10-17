from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello universe from /'

@app.route('/path1')
def hello_path1():
    return 'hello universe from /path1'

@app.route('/path1/subpath1')
def hello_subpath1():
    return 'hello universe from /path1/subpath1'

if __name__ == '__main__':
    app.run(debug=True)
