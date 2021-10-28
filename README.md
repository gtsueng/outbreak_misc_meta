## Outbreak miscelleneous metadata appender

The script (src/append_misc_meta.py) contains modules for appending additional/script-derived metadata to existing outbreak.info resource parsers.

### To use:
 1. add the `append_misc_meta.py` file to the parser
 2. Add the line `from append_misc_meta import *` somewhere near the top of the `parser.py` file
 3. Edit the `load_annotations()` function of the parser (see below for details)
 4. Update the ES mapping in the `upload.py` file to use `https://raw.githubusercontent.com/outbreak-info/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json`
 5. Include properties such as `correction`,`evaluations`,`topicCategory`,`citedBy` if they are not already included in the upload.py file

### Adding the append_misc_meta.py file to the parser
The file can fall out of date if it is added manually. It's better to pull it fresh from github. This is an example of how it can be done:
```
import os
import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
with open(os.path.join(script_path,'append_misc_meta.py'),'w+') as appendfile:
    r = requests.get('https://raw.githubusercontent.com/gtsueng/outbreak_misc_meta/main/append_misc_meta.py')
    appendfile.write(r.text)
    appendfile.close()

from append_misc_meta import *
```

### Editing the load_annotations function
**Example of `load_annotations()` function--before:**
```
def load_annotations():
    docs = getFigshare(ID_API, FIGSHARE_API)
    for doc in docs:
        yield doc
```

Get the dictionary of paths which will locate the files where the miscelleneous annotations are stored locally
 `path_dict = fetch_path_dict()`

Use the `add_anns()` function to search for annotations to add to each document

**Example of `load_annotations()` function--after:**
```
def load_annotations():
    path_dict = fetch_path_dict()
    docs = getFigshare(ID_API, FIGSHARE_API)
    for eachdoc in docs:
        doc = add_anns(path_dict,eachdoc)
        yield doc
```

### Editing the mapping 
**Example of mapping information in the `upload.py` file of a parser**
```
MAP_URL = "https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping_.json"`
```
```
MAP_VARS = ["@type", "author", "curatedBy", "date", "dateCreated", "dateModified", "datePublished", "description", "distribution", "doi", "funding", "identifier", "isBasedOn", "keywords", "license", "name", "url"]`
```

**Example of updated mapping information in the `upload.py` file of a parser**
```
MAP_URL = "https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json"
```
```
MAP_VARS = ["@type", "author", "curatedBy", "date", "dateCreated", "dateModified", "datePublished", "description", "distribution", "doi",   "funding", "identifier", "isBasedOn", "keywords", "license", "name", "url","correction","evaluations","topicCategory", "citedBy"]
```

## Altmetrics Appender
The Altmetrics appender provides a set of functions for pinging the altmetrics API and formatting the returned result as schema-compliant AggregateReviews which can be added to the record for the corresponding publication using the `evaluations` property.

The metadata is returned for incorporation into the doc. In other words, this script may be used similar to outbreak_misc_meta 

Note that the credentials.json file contains the API key for altmetrics api and is needed to bypass rate limits, but does not provide additional data access. 

### To use:
 1. Add the altmetric appender script from github:
 ```
 import os
 import pathlib
script_path = pathlib.Path(__file__).parent.absolute()
with open(os.path.join(script_path,'append_altmetrics.py'),'w+') as appendfile:
    r = requests.get('https://raw.githubusercontent.com/gtsueng/covid_altmetrics/as_parse_script/append_altmetrics.py')
    appendfile.write(r.text)
    appendfile.close()

from append_almetrics import *
 ```
 2. Use the altmetrics appender script to pull an evaluation from altmetrics.
 If a pmid is available use the pmid that's been parsed to the `_id` field:
 ```
 script_path = pathlib.Path(__file__).parent.absolute()
 for eachdoc in doclist[]:
    pmid = eachdoc['_id']
    altmetric_dict = get_altmetrics_update(script_path,pmid)
    try:
        evaluationslist = eachdoc['evaluations']
    except:
        evaluationslist = []
    evaluationslist.append(altmetric_dict)
    eachdoc['evaluations']=evaluationslist
    return(eachdoc)
 ```
 If a doi is available use the doi:
 Note that dois should not include trailing version numbers as those do not resolve properly
 For example: this biorxiv doi: 10.1101/2021.10.18.464256v1 should not include the v1 in order to function properly and would properly be formatted as 10.1101/2021.10.18.464256
 ```
 script_path = pathlib.Path(__file__).parent.absolute()
 for eachdoc in doclist[]:
    doi = eachdoc['doi']
    altmetric_dict = get_altmetrics_update(script_path,doi)
    try:
        evaluationslist = eachdoc['evaluations']
    except:
        evaluationslist = []
    evaluationslist.append(altmetric_dict)
    eachdoc['evaluations']=evaluationslist
    return(eachdoc)
 ```
 For NCT ClinicalTrials, use the nct id that's been parsed to the `_id` field:
  ```
 script_path = pathlib.Path(__file__).parent.absolute()
 for eachdoc in doclist[]:
    nct = eachdoc['_id']
    altmetric_dict = get_altmetrics_update(script_path,nct)
    try:
        evaluationslist = eachdoc['evaluations']
    except:
        evaluationslist = []
    evaluationslist.append(altmetric_dict)
    eachdoc['evaluations']=evaluationslist
    return(eachdoc)
 ```