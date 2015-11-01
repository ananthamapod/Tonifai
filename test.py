import requests
import urllib

key = ""

f = open("encoded.txt")
key = f.readline()

def get_tags(encoded_data):
    payload = { 
        "grant_type": "client_credentials",
        "client_id": "JBVqlsHeEhudFSEQirJzt04piCJ5fBsVux7kNoxA",
        "client_secret": "9QdRHGl5VbYSj4dgnJEegrA8ppAuH3KNmit_2A7O"
    }   
    token = requests.post("https://api.clarifai.com/v1/token/", params=payload).json()
    access_token = token['access_token']
    print access_token
    payload = { 
        "encoded_data": encoded_data
    }   
    header = { 
        "Authorization" : "Bearer " + access_token
    }   
    final = requests.post("https://api.clarifai.com/v1/tag", params=payload, headers=header)
    print final.text

def get_song(tags):
    search = ""
    for elem in tags:
        search = search + elem + "+" 

    payload = {"q" : search}

    page = requests.get("http://search.azlyrics.com/search.php", params=payload)
    tree = html.document_fromstring(page.text)

    for val in tree.xpath("//a[contains(@href, 'lyrics')]"):
        if len(val.text_content()) > 1:
                print val.text_content()

get_tags(key)
