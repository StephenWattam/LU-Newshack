from socket import *
import json

PORT=1234
HOST='localhost'

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

  languages = rawdata
  for lang in languages:
    for cat in languages[lang]:
      for uri in languages[lang][cat]:
          print(lang)
          print(cat)
          print(uri)
          result = languages[lang][cat][uri]
          if not result or not 'summary' in result:
            continue
          text = result['summary']
          time = result['firstCreated']
          vidids = []
          imgids = []
          if 'media' in result:
            if 'images' in result['media']:
              for key in result['media']['images']:
                iids = result['media']['images'][key].keys()
                for iid in iids:
                  imgdata = result['media']['images'][key][iid]
                  if 'altText' in imgdata:
                    text += imgdata['altText']
                imgids += iids

            if 'videos' in result['media']:
              for key in result['media']['videos']:
                vids = result['media']['videos'][key].keys()
                for vid in vids:
                  viddata = result['media']['videos'][key][vid]
                  if 'image' in viddata and 'altText' in viddata['image']:
                    text += viddata['image']['altText']
                vidids += vids

            
          nes =  getEntities(text)
          fmap = {
            "uri" : uri,
            "lang" : lang, 
            "named_entities": nes,
            "time_created": time,
            "image_ids" : imgids,
            "video_ids" : vidids 
          }
          featurevector += [fmap]

  json.dump(featurevector, of)

