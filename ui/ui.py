from flask import Flask, render_template
from flask import request

import sys

app = Flask(__name__)
articles        = None
similarities    = None


# Show help/intro page
@app.route('/')
@app.route('/hello')
def hello():
    if request.form.get("uri", None):
        return render_template('results.html')

    return render_template('hello.html')

# Show results
@app.route('/go', methods=['GET', 'POST'])
def go():
    uri = request.args['uri']
    return render_template('results.html', uri = uri)

# Entry point
if __name__ == '__main__':
    if not (len(sys.argv) == 3):
        print("ARGS: ARTICLE_JSON ARTICLE_SIMILARITY")
        sys.exit(1)
    
    # TODO: load similarity search system

    app.run(debug=True)
