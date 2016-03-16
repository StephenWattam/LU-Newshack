from socket import *
import json
import subprocess
import os
import sys

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


def get_pos(text):
  origWD = os.getcwd()
  if 'stanford-postagger' not in sys.path[0]:
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), 'stanford-postagger-2015-12-09'))
  tempfile = open("tempfile", 'w')
  tempfile.write(text)
  tempfile.close()
  stdoutdata = subprocess.check_output(['./stanford-postagger.sh models/english-bidirectional-distsim.tagger tempfile'], shell=True)
  outtext = stdoutdata.decode('utf-8')
  outtext = [tuple(word.split('_')) for word in outtext.split()]
  os.chdir(origWD)
  return outtext


def process(rawfilename, outfilename):
  """ Extract desired features from the output file
  produced by the download/translate process, and
  output to a different JSON file. """

  rawdata = json.load(open(rawfilename, 'r'))
  of = open(outfilename, 'w')
  featurevector = []

  languages = rawdata
  for lang in languages:
    for cat in languages[lang]:
      print("Category: "+cat)
      for uri in languages[lang][cat]:
          print("URI: "+uri)
          result = languages[lang][cat][uri]
          if not result or not 'summary' in result:
            print("Skipping")
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
                    text += ' ' + imgdata['altText']
                  if 'href' in imgdata:
                    imgids.append(imgdata['href'])

            if 'videos' in result['media']:
              for key in result['media']['videos']:
                vids = result['media']['videos'][key].keys()
                for vid in vids:
                  viddata = result['media']['videos'][key][vid]
                  if 'href' in viddata:
                      vidids.append(viddata['href'])
                  if 'image' in viddata:
                    if 'altText' in viddata['image']:
                      text += ' '  + viddata['image']['altText']
                    if 'href' in viddata['image']:
                      vidids.append(viddata['image']['href'])

          verbs = []
          print(text)
          try:
            pos_text = get_pos(text)
          except Exception as e:
            print(e)
            pos_text = []
          for string, tag in pos_text:
            if 'VB' in tag:
              verbs.append(string)
            
          nes =  getEntities(text)
          fmap = {
            "uri" : uri,
            "lang" : lang, 
            "named_entities": nes,
            "time_created": time,
            "verbs" : list(set(verbs))
          }
          featurevector += [fmap]

  json.dump(featurevector, of)
