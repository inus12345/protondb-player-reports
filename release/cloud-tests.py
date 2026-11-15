import os,json,time,urllib.request,pathlib
P=pathlib.Path(__file__).resolve().parent
H={'Authorization':'Bearer '+(os.environ.get('APIFY_TOKEN') or os.environ.get('Apify_Token')),'Content-Type':'application/json'}
def api(route,data=None):
 req=urllib.request.Request('https://api.apify.com/v2'+route,headers=H,data=json.dumps(data).encode() if data is not None else None)
 with urllib.request.urlopen(req,timeout=90) as r:return json.load(r)['data']
def wait(route):
 while True:
  d=api(route)
  if d['status'] not in ['READY','RUNNING','ABORTING','TIMING-OUT']:return d
  time.sleep(10)
b=wait('/actor-builds/hxIdVBWmJHI3ba5jz');(P/'build-optimized.json').write_text(json.dumps(b,indent=2));print('build',b['status'],flush=True)
if b['status']!='SUCCEEDED':raise SystemExit(1)
for label,inp,n in [('optimized-small',{'maxResults':10},10),('normal',{'maxResults':100},100),('medium',{'maxResults':500},500),('large',{'maxResults':1000},1000)]:
 r=api('/acts/5MfSH4T9Sv9Hnca02/runs?build='+b['buildNumber']+'&memory=1024&timeout=300&maxTotalChargeUsd=1',inp);(P/(label+'-run.json')).write_text(json.dumps(r,indent=2));print(label,r['id'],'started',flush=True)
 r=wait('/actor-runs/'+r['id']);(P/(label+'-run.json')).write_text(json.dumps(r,indent=2))
 rows=api('/datasets/'+r['defaultDatasetId']+'/items?limit=10000') if False else None
 # Dataset item endpoint returns an array, not an API data wrapper.
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/datasets/'+r['defaultDatasetId']+'/items?limit=10000',headers=H)) as f:rows=json.load(f)
 ids=[x.get('recordId') for x in rows];valid=sum(all(x.get(k) for k in ['recordId','steamAppId','gameTitle','date','verdict','noteText','collectedAt']) for x in rows)
 proof={'count':len(rows),'unique':len(set(ids)),'valid':valid,'runtimeSeconds':r['stats']['runTimeSecs'],'peakRamBytes':r['stats'].get('memMaxBytes'),'usageTotalUsd':r.get('usageTotalUsd'),'status':r['status']};(P/(label+'-quality.json')).write_text(json.dumps(proof,indent=2));print(label,proof,flush=True)
 if r['status']!='SUCCEEDED' or len(rows)!=n or len(set(ids))!=n or valid!=n:raise SystemExit('Release gate failed')
