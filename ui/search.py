import json

def search_for_similar_uris(similarities, uri):
    '''similarities is the data to search (similarities),
       uri is the URI to search for '''
    if not uri in similarities.keys():
        return None
    relevant_uris = similarities[uri]

    language_dict = {}
    for rel_uri in relevant_uris:
        lang, sim = rel_uri['lang'], rel_uri['sim']
        if lang in language_dict:
            language_dict[lang].append((rel_uri['uri'], sim))
        else:
            language_dict[lang] = [(rel_uri['uri'], sim)]

    sorted_language_dict = {}

    for lang, entry in language_dict.items():
        sorted_list = sorted(language_dict[lang], key=lambda item: item[1])
        sorted_language_dict[lang] = sorted_list

    return sorted_language_dict


# Find the article pointed at by the URL given
def find_article_in_list(articles, uri):
    article = None
    
    for language, categories in articles.items():
        for category, article_list in categories.items():
            for aid, art in article_list.items():
                if aid == uri:
                    article = art

    return article


