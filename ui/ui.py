from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.form.get('uri', None):
        print("nionio", request.form.get['url'])
    return render_template('hello.html', name='')

if __name__ == '__main__':
    app.run(debug=True)
