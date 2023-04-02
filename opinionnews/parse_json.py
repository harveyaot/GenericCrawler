import requests
import json

# readline json from file tmp_a.json
with open('scmp.json', 'r') as f:
    d = json.load(f)
    
qs_opinions = []
if "contentService" in d:
    for qs in d["contentService"].keys():
        if "opinion" in qs:
            qs_opinions.append(qs)

count = 0
for qs in qs_opinions:
    val = d["contentService"][qs]

    if val.get("__typename", None) != "Article":
        continue

    url = val.get("urlAlias", "")
    title = val.get("headline", "")
    subHeadline = val.get("socialHeadline", "")
    updateDate = val.get("updatedDate",0) / 1000

    # process image
    imgs = val.get("images", [])
    if imgs:
        id = imgs[0].get("id", None)
        if id and id in d["contentService"]:
            image = d["contentService"][id]['url']
            print(image)
            
    # process author
    authors = val.get("authors", []) 
    id = authors[0].get("id", None)
    if id and id in d["contentService"]:
        author = d["contentService"][id]['name']
        authorLink = d["contentService"][id]['urlAlias']
        print(author, authorLink)

    #  process summary
    
    summary = val.get("summary", {})
    if "json" in summary:
        ps = []
        for p in summary["json"]:
            if p["type"] == "p":
                ps.extend([c["data"] for c in p["children"]])
                print(p["children"][0]["data"]) 

    # process summary 
    print(url, updateDate)
    
print(len(qs_opinions))