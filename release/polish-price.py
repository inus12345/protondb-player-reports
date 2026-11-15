import os,json,urllib.request,datetime,pathlib
p=pathlib.Path('release');h={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token')),'Content-Type':'application/json'}
def api(route,body=None):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+route,headers=h,data=json.dumps(body).encode() if body is not None else None,method='PUT' if body is not None else 'GET'),timeout=90) as f:return json.load(f)['data']
before=api('/acts/5MfSH4T9Sv9Hnca02');current=before['pricingInfos'][-1];assert current['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']==.0005
next=json.loads(json.dumps(current));stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();next.update(createdAt=stamp,startedAt=stamp,minimalMaxTotalChargeUsd=.0504,reasonForChange='Owner-requested affordable competitive pricing:20% lower written-report rate; keep fixed preparation cost covered. Standard platform usage included.');next['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']=.0004
api('/acts/5MfSH4T9Sv9Hnca02',{'pricingInfos':before['pricingInfos']+[next]});after=api('/acts/5MfSH4T9Sv9Hnca02');saved=after['pricingInfos'][-1];assert saved['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']==.0004 and saved['minimalMaxTotalChargeUsd']==.0504
(p/'polish-pricing.json').write_text(json.dumps(saved,indent=2));print('Saved verified price:USD0.0004/report plus0.05 preparation; minimum budget0.0504')
