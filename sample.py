import requests
import hashlib
import json
import datetime

d = {
  "title": "The New Face of Democratic Struggle",
  "summary": "The struggle for democracy in Iran may take years, even decades.",
  "url": "https://www.newsweek.com/new-face-democratic-struggle-opinion-1775922",
  "thumbnail": "https://d.newsweek.com/en/full/2183763/message-saying-stop-executions-iran.webp?w=466&h=311&f=1615113b918698ef24777e027ba4fd93",
  "docid":"https://www.newsweek.com/new-face-democratic-struggle-opinion-1775922",
  "author": " Jessi Hanson-DeFusco",
  "source": "newsweek",
  "crawlDate": 1674830098
}
api = "https://cms-strapi-longriver.azurewebsites.net/api/opinoin-news-many"
token = "046cc25ba3ae6e72dbbaef44811832a588972801af297137e99e6c2113baf688554da39098d17213533a5253e04a20958de596d62907740c84b0d4d32bd3b502150c0188633eca0881c546659bf299f07091913c14b3ad3d6a2310441fb815749f4a49ec83897c18114288eb3e9734428afc259b79eb5f425a7ebf5cba177959"

headers = {"Content-Type": "application/json",
           "Authorization": f"Bearer {token}",
           }


#generate hash from a string
hashstr  = hashlib.md5(d['url'].encode()).hexdigest()
d['docid'] = hashstr
d['updateDate'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


r = requests.post(api, data={'data':d}, headers=headers)
#print(r.json())

r = requests.get(api + f"?filters[docid][$eq]={d['docid']}&fields[0]=id", headers=headers)
#print(r.json())

r = requests.put(api + '/6', headers=headers, data=json.dumps({'data':d}))
print(r.json())