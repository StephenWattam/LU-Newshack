import json
import anysim
import time
import datetime
import itertools

def getdate(timestring):
  return timestring[0:timestring.index('T')]


def setsim(imgl1, imgl2):
  s1 = set(imgl1)
  s2 = set(imgl2)
  if len(s1) == 0 or len(s2) == 0:
    return 0
  return len(s1.intersection(s2))/len(s1.union(s2))


def timesim(tstr1, tstr2):
  datestring = "%Y-%m-%dT%H:%M:%S+00:00"
  t1 = datetime.datetime.strptime(tstr1, datestring)
  t2 = datetime.datetime.strptime(tstr2, datestring)
  delta = t1 - t2
  denom = datetime.timedelta(days=1).total_seconds()
  return 1-(abs(delta.total_seconds())/86400)


def get_candidate_pairs(featurelist):
  #group same-date articles
  dateblocks = {} 
  for articleitem in featurelist:
    datestr = getdate(articleitem['time_created'])
    if datestr not in dateblocks:
      dateblocks[datestr] = [articleitem]
    else:
      dateblocks[datestr] += [articleitem]

  #add all same-date pairs which are of a different language
  candidates = []
  for datestr in dateblocks:
    for aii, aij in itertools.combinations(dateblocks[datestr],2):
      if aii['lang'] != aij['lang']:
        candidates.append((aii, aij))
  return candidates


#Similarity Sum (simple standard method for thresholding)
def similarity(articleone, articletwo):
  nesim = anysim.anysim(articleone['named_entities'], articletwo['named_entities'])
  imsim = setsim(articleone['image_ids'], articletwo['image_ids'])
  visim = setsim(articleone['video_ids'], articletwo['video_ids'])
  tisim = timesim(articleone['time_created'], articletwo['time_created'])
  sim_vec = [nesim, imsim, visim, tisim]
  return sum(sim_vec)


def compare(featureslist):
  #block the list by data
  candidate_pairs = get_candidate_pairs(featureslist)
  #calculate similarity
  similarities = [similarity(cp[0], cp[1]) for cp in candidate_pairs]
  return zip(similarities, candidate_pairs)

 
def matches(articlefile, threshold):
  featureslist = json.load(open(articlefile, 'r'))
  comparison_res = compare(featureslist)
  matches = {}
  for sim, cp in comparison_res:
    if sim > threshold:
      ur1 = cp[0]['uri']
      ur2 = cp[1]['uri']
      l1 = cp[0]['lang']
      l2 = cp[1]['lang']

      if ur1 in matches:
        p2 = {'lang':l2, 'uri':ur2}
        matches[ur1].append(p2)
      else:
        matches[ur1] = [p2]

      if ur2 in matches:
        p1 = {'lang':l1, 'uri':ur1}
        matches[ur2].append(p1)
      else:
        matches[ur2] = [p1]

  return matches

def output(matches, filename):
  json.dump(matches, open(filename,'w'))

m = matches('rereout.json', 0.9)

output(m, 'thing.json')
