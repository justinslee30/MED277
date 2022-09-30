# lab3 python file
# importing necessary packages for lab3
import spacy
import json
from Authentication import *
from pathlib import Path
import wikipedia
import webbrowser


# use Spacy and SciSpacy to identify entities in the "entire" text (not just HPI)
# use SciSpacy model "en_ner_bc5cdr_md"
def entities(wname, rname):

    with open(rname) as r:
        with open(wname, "w") as w:
            path = Path().absolute()
            print("   Analyzing with SciSpacy Model...")
            content = r.read()
            nlp = spacy.load("en_ner_bc5cdr_md")
            doc = nlp(content)
            entityList = []
            w.write("Spacy Entity List\n")
            for word in doc.ents:
                entityList.append((str(word)))
            entityList = list(dict.fromkeys(entityList))
            result = []
            marker = set()
            for l in entityList:
                ll = l.lower()
                if ll not in marker:
                    marker.add(ll)
                    result.append(l)
            for entity in result:
                w.write(entity + "\n")
            print("Saved Spacy Entities to file " + str(path.as_posix()) + "/" + wname)
            return result


# use UMLS UTS for each entity and for those that are UMLS concepts, identify which are
# diseases/syndromes by using the UMLS concept's semantic type. To do this, you will use the /search end
# point to retrieve CUIs for those entities that are UMLS concepts. For each of these, then use the
# /content/current/CUI?{CUI}
# 2. For each Spacy identified "entity", fetch the following from the UMLS:
# CUI | Term | Source Terminology.
def get_ulms_info(string):
    apikey = "69d2ad47-8307-4f4c-b0aa-dfa5fbeae47e"
    version = "current"
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/" + version
    # get at ticket granting ticket for the session
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    pageNumber = 0
    # generate a new service ticket for each page if needed
    ticket = AuthClient.getst(tgt)
    pageNumber += 1
    # construct the RESTful API command variable
    query = {'string': string, 'ticket': ticket, 'pageNumber': pageNumber}
    query['searchType'] = "exact"
    query['sabs'] = "SNOMEDCT_US"
    r = requests.get(uri + content_endpoint, params=query)
    r.encoding = 'utf-8'
    items = json.loads(r.text)
    jsonData = items["result"]
    return jsonData


def semantic_type(CUI):
    jsonData = []
    apikey = "69d2ad47-8307-4f4c-b0aa-dfa5fbeae47e"
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/content/current/CUI/"
    # get at ticket granting ticket for the session
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    # generate a new service ticket for each page if needed
    ticket = AuthClient.getst(tgt)
    # construct the RESTful API command variable
    query = {'ticket': ticket}
    r = requests.get(uri + content_endpoint + CUI, params=query)
    r.encoding = 'utf-8'
    items = json.loads(r.text)
    for i in range(len(items["result"]["semanticTypes"])):
        jsonData.append(items["result"]["semanticTypes"][i]["name"])
    return jsonData


def umls_semantic(entities, wname):
    with open(wname, "w") as w:
        path = Path().absolute()
        print("   Retrieving UMLS info for matches...")
        entity_list = []
        for entity in entities:
            umls_data = get_ulms_info(entity)
            for result in umls_data["results"]:
                print(entity)
                if umls_data["results"][0]["ui"] != "NONE":
                    print(result["ui"] + "|" + result["name"] + "|" + result["rootSource"])
                    w.write(result["ui"] + "|" + result["name"] + "|" + result["rootSource"] + "\n")
                    for semanticType in semantic_type(result["ui"]):
                        if semanticType == "Disease or Syndrome":
                            entity_list.append(entity)
                            print("   Disease or Syndrome - found")
                            w.write("   Disease or Syndrome - found\n")
                        else:
                            print("   " + semanticType)
                            w.write("   " + semanticType + "\n")
        entity_list = list(dict.fromkeys(entity_list))
        print("Saved UMLS Concepts to file " + str(path.as_posix()) + "/" + wname)
        print("List of diseases/syndromes, duplicates removed")
        print(entity_list)
        return entity_list


# For each of the disease/syndrome items, obtain the Wikipedia summary information and open the Wikipedia web page.
# For each of the concepts that are "Disease or Syndrome", obtain information from Wikipedia using the Wikipedia API.
# Write the Wikipedia entry's 'summary' to a .txt file named for the drug and  launch the default desktop web browser
# to access the relevant Wikipedia page.
def getWikiSummary (entity_list):
    print("   Retrieving Wikipedia entries for:\n   Writing Wikipedia info to files and opening browser pages...")
    print(str(Path().absolute().as_posix()))
    for entity in entity_list:
        with open('{}.txt'.format(entity), "w", encoding="utf-8") as w:
            wikiSummary = wikipedia.summary(entity, auto_suggest=False)
            page = wikipedia.page(entity,auto_suggest=False).url
            print(wikiSummary)
            w.write(wikiSummary)
            webbrowser.open_new_tab(page)


rfile = "L3.csv"
wfile = "SpacyEntities.txt"
entityList = entities(wfile, rfile)
wfile2 = "UMLS_Concepts.txt"
umls = umls_semantic(entityList, wfile2)
getWikiSummary(umls)
print('Done!')