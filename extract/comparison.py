import json
import itertools

def getdate(timestring):
  return timestring[0:timestring.index('T')]

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
      if aii['language'] != aij['language']:
        candidates.append(aii, aij)
  return candidates

#Similarity Sum
def similarity(articleone, articletwo):
  nesim = nesim(articleone['named_entities'], articletwo['named_entities'])
  imsim = setsim(articleone['image_ids'], articletwo['image_ids'])
  visim = setsim(articleone['video_ids'], articletwo['video_ids'])
  tisim = setsim(articleone['time_created'], articletwo['time_created'])
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
  comparison_res = compare(featurelist)
  matches = []
  for sim, cp in comparison_res:
    matches.append((cp[1]['uid'], cp[2]['uid']))
  return matches
