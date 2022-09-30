# lab2 python file
# importing necessary packages for lab2
from nltk import sent_tokenize, word_tokenize, pos_tag
import spacy
import requests
import json
import argparse
from Authentication import *


# use nltk to output count of sentences in passage and list of noun or noun phrases
# in all sentences in passage w/ respective POS tag
def p1(fname, pos):
    with open(fname) as f:
        content = f.read()
        sentences = sent_tokenize(content)
        print(len(sentences))
        for word in pos_tag(word_tokenize(content)):
            if word[1] in pos:
                print(word)


# output entities it returns from SciSpacy.nlp() function
def p2(fname):
    with open(fname) as f:
        content = f.read()
        nlp = spacy.load("en_core_sci_sm")
        doc = nlp(content)
        entity_list = []
        print("--------SciSpacy entity list----------")
        for word in doc.ents:
            print(word)
            entity_list.append(str(word))
        return entity_list


# use SpaCy derived entities list and the UMLS UTS RESTful API 'search' endpoint to
# retrieve matched concepts

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


def p3(entities):
    for entity in entities:
        umls_data = get_ulms_info(entity)
        print("\n-----------------\n" + entity)
        for result in umls_data["results"]:
            if umls_data["results"][0]["ui"] == "NONE":
                break
            print(result["ui"] + "|" + result["name"] + "|" + result["rootSource"])


file = "lab2-hpi.csv"
posWanted = ("NN", "NNP", "NNS", "NNPS")
p1(file, posWanted)
print("\n\n")
entity_list = p2(file)
p3(entity_list)
