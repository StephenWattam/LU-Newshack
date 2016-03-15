import json
import fuzzy

def anysim(dict1, dict2):
    #f = open('re-out.json')
    #a = json.loads(f.read())
    #f.close()
    #print(a[0]['named_entities'])
    #print(type(a[0]['named_entities']))
    #dict1 = a[0]['named_entities']
    #dict2 = a[0]['named_entities']
    if len(dict1) == 0 or len(dict2) == 0:
      return 0.0
    list_of_values = []
    for key in dict1:
        if key in dict2:
            list_of_values.append(key)
    list_of_matches = []
    for key in list_of_values:
        list1 = dict1[key]
        list2 = dict2[key]
        list_of_matches.append(compare_all_lists(list1,list2))
    sum_of_correct = 0
    sum_of_len = 0
    for a in list_of_matches:
        sum_of_correct += a[0]
        sum_of_len += a[1]
    return float(sum_of_correct)/float(sum_of_len)

def compare_all_lists(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    match_list = []
    length = 0
    if len1 > len2:
        match_list = compare_lists(list1,list2)
        length = len2
    else:
        match_list = compare_lists(list2,list1)
        length = len1
    return (len(match_list),length)




def compare_lists(list1,list2):
    metaphor = fuzzy.DMetaphone()
    count1 = 0
    count2 = 0
    match_list = []
    for item in list1:
        met1, met2 = metaphor(item)
        items = [item,met1,met2]
        for compare_item in list2:
            a_met1, a_met2 = metaphor(compare_item)
            compare_items = [compare_item, a_met1, a_met2]
            ans = compare_items_function(items,compare_items)
            if ans:
                match_list.append((count1,count2))
                break
            count2 += 1
        count2 = 0
        count1 += 1
    return match_list

def compare_items_function(list1, list2):
    ans_list = []
    length = len(list1)
    for a in range(0,length):
        if (list1[a] == list2[a] and list1[a] != None):
            ans_list.append(1)
        else:
            ans_list.append(0)
    if 1 in ans_list:
        return 1
    else:
        return 0
