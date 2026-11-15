import json,os,urllib.request,pathlib
P=pathlib.Path('release');H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token')),'Content-Type':'application/json'}
def api(route,body=None):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+route,headers=H,data=json.dumps(body).encode() if body is not None else None,method='PUT' if body is not None else 'GET'),timeout=90) as f:return json.load(f)['data']
b=json.loads((P/'unicode-build.json').read_text());assert b['status']=='SUCCEEDED'
for label,n in [('unicode-default',10),('unicode-game',100),('unicode-large',1000)]:
 q=json.loads((P/(label+'-quality.json')).read_text());assert q['count']==q['valid']==q['unique']==q['csvRows']==q['excelRows']==n
 assert json.loads((P/(label+'-source.json')).read_text())['allSourceRowsMatched']
a=api('/acts/5MfSH4T9Sv9Hnca02');assert a['isPublic'];assert a['pricingInfos'][-1]['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']==.0004
assert a['taggedBuilds']['unicode-fix']['buildId']==b['id'];tags=a['taggedBuilds'];tags['latest']=tags['unicode-fix'];api('/acts/'+a['id'],{'taggedBuilds':tags});after=api('/acts/'+a['id']);assert after['taggedBuilds']['latest']['buildId']==b['id'];assert after['defaultRunOptions']['build']=='latest';(P/'unicode-published.json').write_text(json.dumps(after,indent=2));print('LIVE verified default',b['buildNumber'],b['id'])
