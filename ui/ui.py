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

    # Find the article if you csn
    article = search.find_article_in_list(articles, uri)

    # Check we found something
    if not article:
        return render_template('missing.html', uri = uri, explanation = 'We can\'t find that URI in the database.')

    # Build a display-format list of most likely item
    ranked_similarities = search.search_for_similar_uris(similarities, uri)
    if not ranked_similarities:
        return render_template('missing.html', uri = uri, explanation = 'We can\'t find any matches for that article.')

    languages = {}
    languages[article["language"]] = (article["assetUri"], 1.0, article)
    for language, sorted_list in ranked_similarities.items():
        articleuri, sim = sorted_list[0]
        languages[language] = (articleuri, sim, convert_xml(search.find_article_in_list(articles, articleuri)))
    all_pictures = set()
    for article in languages:
        if languages[article][2] == None:
            pass
        else:
            for media_items in languages[article][2]['media']['images']:
                for images in languages[article][2]['media']['images'][media_items]:
                    if languages[article][2]['media']['images'][media_items][images]['href'] != "http://":
                        picture = languages[article][2]['media']['images'][media_items][images]
                        all_pictures.add(picture['href'])

    another = list(all_pictures)
    print(type(another))
    print(another[0])
    return render_template('results.html', uri = uri, articles = languages, all_pictures = another, length=len(all_pictures))


def convert_xml(article):
    str = article["body"]
    str = str.replace("<paragraph", "<p").replace("</paragraph", "</p")

    article["body_html"] = str
    return article



# Entry point
if __name__ == '__main__':
    if not (len(sys.argv) == 3):
        print("ARGS: ARTICLE_JSON SIMILARITY_JSON")
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

    app.run(host='0.0.0.0')
