import os
import json

def find_gen_path():
    tmp_dir = os.getcwd()
    while 'topic_classifier' not in os.listdir(tmp_dir):
        tmp_dir = os.path.dirname(tmp_dir)
    return(tmp_dir)

def fetch_path_dict():
    general_path = find_gen_path()
    topic_folder = os.path.join(general_path,'topic_classifier')
    topic_results = os.path.join(topic_folder,'results')
    alt_path = os.path.join(general_path,'covid_altmetrics')
    alt_results = os.path.join(alt_path,'results')
    preprint_path = os.path.join(general_path,'outbreak_preprint_matcher')
    preprint_results = os.path.join(preprint_path,'results')
    preprint_dumps = os.path.join(preprint_results,'update dumps')
    loe_ann_path = os.path.join(general_path,'covid19_LST_annotations')
    loe_results = os.path.join(loe_ann_path,'results')
    path_dict = {
        'topics_file':os.path.join(topic_results,'topic_cats.json'),
        'altmetrics_file':os.path.join(alt_results,'altmetric_annotations.json'),
        'litcovid_updates':os.path.join(preprint_dumps,'litcovid_update_file.json'),
        'preprint_updates':os.path.join(preprint_dumps,'preprint_update_file.json'),
        'loe_annotations':os.path.join(loe_results,'loe_annotations.json')
        }
    return(path_dict)

def fetch_topics(path_dict,outbreak_id):
    with open(path_dict['topics_file']) as infile:
        topics_dict = json.load(infile)
    for i in range(len(topics_dict)):
        if topics_dict[i]['_id']==outbreak_id:
            topicinfo = topics_dict[i]
            return(topicinfo)    

def fetch_preprint_updates(path_dict,preprint_id):
    with open(path_dict['preprint_updates'],'r') as infile:
        preprint_dict = json.load(infile)
    for i in range(len(preprint_dict)):
        if preprint_dict[i]['_id']==preprint_id:
            preprint_info = preprint_dict[i]
            return(preprint_info)

def fetch_reviewed_updates(path_dict,litcovid_id):
    with open(path_dict['litcovid_updates'],'r') as infile:
        litcovid_dict = json.load(infile)
    for i in range(len(litcovid_dict)):
        if litcovid_dict[i]['_id']==litcovid_id:
            litcovid_info = litcovid_dict[i]
            return(litcovid_info)
    
def check_altmetrics(path_dict,outbreak_id):
    with open(path_dict['altmetrics_file']) as infile:
        altmetrics_dict = json.load(infile)
    for i in range(len(altmetrics_dict)):
        if altmetrics_dict[i]['_id']==outbreak_id:
            altinfo = altmetrics_dict[i]
            return(altinfo)

def check_loe_anns(path_dict,outbreak_id):
    with open(path_dict['loe_annotations']) as infile:
        loe_dict = json.load(infile)
    for i in range(len(loe_dict)):
        if loe_dict[i]['_id']==outbreak_id:
            loe_info = loe_dict[i]
            return(loe_info)

def add_anns(doc):
    path_dict = fetch_path_dict()
    ## add corrections
    if doc['@type']=='Publication':
        if 'pmid' in doc['_id']:
            ## doc is from litcovid
            corrections = fetch_reviewed_updates(path_dict,doc['_id'])
            loe_info = check_loe_anns(path_dict,doc['_id'])
        else:
            corrections = fetch_preprint_updates(path_dict,doc['_id'])
            loe_info == None
        if corrections != None:
            if 'correction' in doc.keys():  ## check if correction field already used
                doc['correction'].append(corrections)
            else:
                doc['correction']=corrections
        if loe_info != None:
            doc['evaluations'] = loe_info['evaluations']
            if 'citedBy' in doc.keys():
                doc['citedBy'].append(loe_info['citedBy'])
            else:
                doc['citedBy'] = []
                doc['citedBy'].append(loe_info['citedBy'])
    ## add topic_cats
    topic_cats = fetch_topics(path_dict,doc['_id'])
    if topic_cats != None:
        doc['topicCategory']=topic_cats
    ## add altmetrics
    altinfo = check_altmetrics(path_dict,doc['_id'])
    if altinfo != None:
        if 'evaluations' in doc.keys():
            doc['evaluations'].append(altinfo['evaluations'][0])
        else:
            doc['evaluations'] = altinfo['evaluations']
            
    return(doc)
            
    