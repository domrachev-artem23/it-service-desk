import argparse, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
p=argparse.ArgumentParser()
p.add_argument('method');p.add_argument('path');p.add_argument('--data');p.add_argument('--base',default='http://127.0.0.1:5000')
a=p.parse_args()
body=None if a.data is None else open(a.data,encoding='utf-8').read().encode('utf-8')
request=Request(a.base+a.path,data=body,method=a.method.upper(),headers={'Content-Type':'application/json'} if body else {})
try:
    response=urlopen(request)
except HTTPError as error:
    response=error
print('HTTP',response.status)
if response.headers.get('Location'):print('Location:',response.headers['Location'])
text=response.read().decode('utf-8')
if text:
    try:print(json.dumps(json.loads(text),ensure_ascii=False,indent=2))
    except ValueError:print(text)
