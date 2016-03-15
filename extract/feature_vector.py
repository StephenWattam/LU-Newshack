from socket import *
import json

PORT=1234
HOST='localhost'
claimedomains = ['facebook.com','twitter.com','gplus.com','linkedin.com']
webextensions = ['','.html','.php','.aspx']
knownpeoplemaps = {}
PHONE_REGEX='0[0-9 ]{9,}'
EMAIL_REGEX='[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}'

@staticmethod
def makePageName(path):
  if path in ['','/']:
    return 'root.cache'
  else:
    return path.replace('/','^')+'.cache'

def regexGet(regex,text):
  return [st for st in re.findall(regex,text) if isinstance(st,str)]

@staticmethod
def visibleText(source):
  soup = BeautifulSoup(source)
  texts = soup.find_all(text=True)
  fulltext = ''
  for t in texts:
    ntext = ''
    if t.parent.name not in ['style', 'script', '[document]']:
      ntext = re.sub('<!--.*-->|\r|\n', ' ', str(t), flags=re.DOTALL)
      ntext = re.sub('\s{2,}|&nbsp;', ' ', ntext)
      if t.parent.name == 'td':
        ntext += ';'
    fulltext += ntext+'\n'
  return fulltext

def getEntities(text):
  text = text.replace('\n\n',' ')
  tagged_text = ''
  for line in text.split('\n'):
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((HOST,PORT))
    s.sendall((line+'\n').encode('utf-8'))
    try:
      tagged_text += s.recv(4096).decode('utf-8')
    except Exception as e:
      logging.warn("Error handling entity-tagger result.")
      logging.warn(e)
    s.close()
  return slashTags_parse_entities(tagged_text)

def slashTags_parse_entities(tagged_text):
  """Thanks to dat hoang, https://github.com/dat.
  Return a list of token tuples (entity_type, token) parsed
  from slashTags-format tagged text.
  :param tagged_text: slashTag-format entity tagged text
  """
  import re
  from itertools import groupby
  from operator import itemgetter
  SLASHTAGS_EPATTERN = re.compile(r'(.+?)/([A-Z]+)?\s*')
  entities = (match.groups()[::-1] for match in SLASHTAGS_EPATTERN.finditer(tagged_text))
  entities = ((etype, " ".join(t[1] for t in tokens)) for (etype, tokens) in groupby(entities, key=itemgetter(0)) if etype != None)
  entities = dict((first, list(map(itemgetter(1), second))) for (first, second) in groupby(sorted(entities, key=itemgetter(0)), key=itemgetter(0)))
  if 'O' in entities:
    del entities['O']
  for types in entities:
    entities[types] = list(set(entities[types]))
  return entities


def process(rawfilename, outfilename):
  rawdata = json.load(open(rawfilename, 'r'))
  of = open(outfilename, 'w')
  featurevector = []
  results = rawdata['results']

  for result in results:
    text = result['summary']
    time = result['firstCreated']
    vidids = []
    imgids = []
    for key in result['media']['images']:
      iids = result['media']['images'][key].keys()
      for iid in iids:
        text += result['media']['images'][key][iid]['altText']
      imgids += iids

    for key in result['media']['videos']:
      vids = result['media']['videos'][key].keys()
      for vid in vids:
        text += result['media']['videos'][key][vid]['image']['altText']
      vidids += vids

      
    nes =  getEntities(text)
    fmap = {
      "named_entities": nes,
      "time_created": time,
      "image_ids" : imgids,
      "video_ids" : vidids 
    }
    featurevector += [fmap]

  json.dump(featurevector, of)

