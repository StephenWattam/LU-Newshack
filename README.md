Lancaster University Team A BBC NewsHack 2016 entry

This project is a small tool that examines news data (as downloaded from the BBC's CANDY API) and uses a number of simple techniques to align articles written on the same topic.

## Approach
BBC news articles are written for various languages by independent teams.  This means that there are no direct translations available (unless machine translated), so journalists covering a topic will do with various different document structures and sources.

In order to align articles with differing content, we focus on features that summarise the topic.  This means:

 * Entities
 * Verbs
 * Dates

We also tried image path and some other features, but these were very ineffective.  We restrict searches to only the title, summary, and image alt text.  In order to allow the tool to operate on many languages, we translate the text prior to running feature extractors.

Using these features we compute a similarity matrix for documents in the corpus, which we use to look up similar articles.  These are then displayed in the sample web interface.

## Execution
The tool works in several stages:

 1. Download a corpus of news data for several languages using the `download/` tool.
 2. Run the translation system in `translate/` to create a translated corpus.
 3. Annotate the translations using the tool in `extract/` to create the similarity matrix.
 4. Run the UI by passing the translated corpus and similarity matrix to the flask app in `ui/`: `python ui.py articles.json similarities.json`
 5. Visit [http://localhost:5000](http://localhost:5000) and enter a URL.

### Sample data
There are two corpora, gathered over the course of the hackathon, left in `data/`.  To use them, you must find some URLs that existed at that time.  The ones we gave as samples in our presentation are:

 * `/news/business-35782239` (Oil)
 * `/news/election-us-2016-35790460` (Trump)
 * `/arabic/middleeast/2016/03/160312_zind_egypt_profile` (Egypt)

## Other writeups

 * [Matt's site](http://xn--bta-yla.net/posts/projects/linkatron.html)
 * [Steve's site](https://stephenwattam.com/blog/?/20160322/meet-the-linkatron)
 * [Steve's photos](https://flic.kr/s/aHskwHcpNH)
 * [The BBC writeup](http://bbcnewslabs.co.uk/2016/03/17/newsHACK-language-hack/)

