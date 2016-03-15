from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return 'anything'
    else:
        if request.args['uri'] == 'anything':
            return render_template('hello.html', name='')

        return render_template('hello.html', name='')

if __name__ == '__main__':
    app.run(debug=True)
