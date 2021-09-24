## Outbreak miscelleneous metadata appender

The script (src/append_misc_meta.py) contains modules for appending additional/script-derived metadata to existing outbreak.info resource parsers.

### To use:
 1. add the `src` folder to the parser
 2. Add the line `from src/append_misc_meta import *`
 3. Edit the `load_annotations()` function of the parser (see below for details)
 4. Update the ES mapping in the `upload.py` file to use `https://raw.githubusercontent.com/outbreak-info/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json`
 5. Include properties such as `correction`,`evaluations`,`topicCategory`,`citedBy` if they are not already included in the upload.py file

### Editing the load_annotations function
**Example of `load_annotations()` function--before:**
`def load_annotations():
    docs = getFigshare(ID_API, FIGSHARE_API)
    for doc in docs:
        yield doc`

Get the dictionary of paths which will locate the files where the miscelleneous annotations are stored locally
 `path_dict = fetch_path_dict()`

Use the `add_anns()` function to search for annotations to add to each document

**Example of `load_annotations()` function--after:**
`def load_annotations():
    path_dict = fetch_path_dict()
    docs = getFigshare(ID_API, FIGSHARE_API)
    for eachdoc in docs:
        doc = add_anns(eachdoc)
        yield doc`

### Editing the mapping 
**Example of mapping information in the `upload.py` file of a parser**
`MAP_URL = "https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping_.json"`
`MAP_VARS = ["@type", "author", "curatedBy", "date", "dateCreated", "dateModified", "datePublished", "description", "distribution", "doi", "funding", "identifier", "isBasedOn", "keywords", "license", "name", "url"]`

**Example of updated mapping information in the `upload.py` file of a parser**
`MAP_URL = "https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json"`
`MAP_VARS = ["@type", "author", "curatedBy", "date", "dateCreated", "dateModified", "datePublished", "description", "distribution", "doi",   "funding", "identifier", "isBasedOn", "keywords", "license", "name", "url","correction","evaluations","topicCategory", "citedBy"]`