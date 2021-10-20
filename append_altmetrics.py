import os
import json
import requests
import random
from datetime import datetime
import time
import pathlib

def generate_alt_curator():
    todate = datetime.now()
    curatedByObject = {"@type": "Organization", "identifier": "altmetric",  
                       "name": "Altmetric", "affiliation": ["Digital Science"],
                       "curationDate": todate.strftime("%Y-%m-%d")}
    return(curatedByObject)
    
    
def load_key(script_path):
    cred_path = os.path.join(script_path, 'credentials.json')
    with open(cred_path) as f:
        credentials = json.load(f) 
        apikey = credentials["key"]
    return(apikey)


def fetch_meta(key_url,pubid):
    base_url = 'https://api.altmetric.com/v1/'
    if 'pmid' in pubid:
        api_call = base_url+'pmid/'+pubid.replace("pmid","")+key_url
    elif 'NCT' in pubid:
        api_call = base_url+'nct_id/'+pubid+key_url       
    else:
        api_call = base_url+'doi/'+pubid+key_url
    r = requests.get(api_call)
    try:
        hourlylimit = r.headers["X-HourlyRateLimit-Limit"]
        secondslimit = int(hourlylimit)/3600
        sleeptime = 1/secondslimit
    except:
        sleeptime = 1
    if r.status_code==200:
        rawmeta = json.loads(r.text)
        error=False
    else:
        rawmeta={}
        error=True
    return(rawmeta,error,sleeptime)
    
    
def get_altmetrics_update(script_path,eachid):
    apikey = load_key(script_path)
    key_url = '?key='+apikey
    aspectslist = ['cited_by_fbwalls_count','cited_by_feeds_count','cited_by_gplus_count',
                   'cited_by_msm_count','cited_by_posts_count','cited_by_rdts_count',
                   'cited_by_tweeters_count','cited_by_videos_count','cited_by_accounts_count',
                   'readers_count']
    readerlist = ['citeulike','mendeley','connotea']
    rawmeta,error,sleeptime = fetch_meta(key_url,eachid)
    if error == False :
        authorObject = generate_alt_curator()
        altdict = {"@type":"AggregateRating", "author":authorObject, "identifier":rawmeta["altmetric_id"],
                   "url":rawmeta["details_url"], "image":rawmeta["images"]["small"], "name":"Altmetric",
                   "reviewAspect":"Altmetric score", "ratingValue":rawmeta["score"]}
        reviewlist = []
        for eachrating in aspectslist:
            a_review = {"@type":"Review","reviewAspect":eachrating}
            try:
                a_review["reviewRating"]={"ratingValue":rawmeta[eachrating]}
            except:
                a_review["reviewRating"]={"ratingValue":0}
            reviewlist.append(a_review)
        for eachreader in readerlist:
            a_review = {"@type":"Review","reviewAspect":eachreader+" reader count"}
            try:
                a_review["reviewRating"]={"ratingValue":rawmeta["readers"][eachreader]}
            except:
                a_review["reviewRating"]={"ratingValue":0}
            reviewlist.append(a_review)
        altdict["reviews"]=reviewlist
    time.sleep(sleeptime)
    return(altdict)
