import json
import urllib.parse
import urllib.request
from pprint import pprint

url = 'https://api.imgur.com/3/gallery/album/lDRB2/json'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {
    'act' : 'login',
    'login[email]' : 'yzhang@i9i8.com',
    'login[password]' : '123456'
}
headers = { 'Authorization' : 'Client-ID 69a8c05a5598b21' }

data = urllib.parse.urlencode(values)
req = urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(req)
the_page = response.read()
json = json.loads(the_page.decode('utf-8'))
pprint(json)
print(json['status'])
print(json['success'])