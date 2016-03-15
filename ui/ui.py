from flask import Flask, render_template
from flask import request
import search 
import json

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
   
    print("Loading articles from: ", sys.argv[1]);
    f = open(sys.argv[1])
    articles = json.loads(f.read())
    f.close()
    print("Done.")
    print("Loading similarity results from: ", sys.argv[2]);
    f = open(sys.argv[2])
    similarities = json.loads(f.read())
    f.close()
    print("Done.")

    app.run(debug=True)
