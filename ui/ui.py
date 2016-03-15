from flask import Flask, render_template
from flask import request
import search 
import json
import re

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

    # Remove the first bit from the URI if it starts with BBC
    if re.match('^https?:\/\/www\.bbc\.co\.uk\/', uri):
        str = str[20:-1]

    # Find the article pointed at by the URL given
    article = None
    for language, categories in articles.items():
        for category, article_list in categories.items():
            for aid, art in article_list.items():
                if aid == uri:
                    article = art

    # Check we found something
    if not article:
        return render_template('missing.html', uri = uri, explanation = 'We can\'t find that URI in the database.')

    # Build a display-format list of most likely item
    ranked_similarities = search.search_for_similar_uris(similarities, uri)
    if not ranked_similarities:
        return render_template('missing.html', uri = uri, explanation = 'We can\'t find any matches for that article.')

    languages = {}
    for language, sorted_list in ranked_similarities.items():
        languages[language] = sorted_list[0]

    return render_template('results.html', uri = uri, articles = languages)

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



