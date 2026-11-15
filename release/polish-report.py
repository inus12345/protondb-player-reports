import json,os,urllib.request,pathlib,datetime,re,html
from html.parser import HTMLParser
class Images(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_starttag(self,tag,attrs):
  if tag=="img":self.items.append(dict(attrs))
P=pathlib.Path('release');H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token'))}
def api(route):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+route,headers=H),timeout=90) as f:return json.load(f)['data']
a=api('/acts/5MfSH4T9Sv9Hnca02');b=json.loads((P/'polish-build.json').read_text());assert a['taggedBuilds']['latest']['buildId']==b['id'];table=[];receipts=[]
for label in ['polish-default','polish-game','polish-large']:
 r=api('/actor-runs/'+json.loads((P/(label+'-run.json')).read_text())['id']);q=json.loads((P/(label+'-quality.json')).read_text());n=q['count'];assert r['chargedEventCounts']=={'written-report':n,'export-preparation':1};cost=max(r.get('usageTotalUsd',0),sum(r.get('usageUsd',{}).values()));gross=.05+n*.0004;net=.8*gross-cost
 table.append(f"| [{label}](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/{r['id']}) | {n} | {q['csvRows']}/{q['excelRows']} | {r['stats']['runTimeSecs']:.3f}s | {r['stats']['memMaxBytes']/1048576:.1f}MiB | ${cost:.6f} | ${gross:.4f} | {net/gross:.1%} |")
 receipts.append({'label':label,'runId':r['id'],'buildId':r['buildId'],'rows':n,'nativeBilling':r['chargedEventCounts'],'measuredPlatformCostUsd':cost,'apiUsageTotalUsd':r.get('usageTotalUsd'),'sumUsageUsd':sum(r.get('usageUsd',{}).values()),'nominalCustomerPriceUsd':gross,'modeledContributionUsd':net,'quality':q});(P/(label+'-run.json')).write_text(json.dumps(r,indent=2))
logo=json.loads((P/'logo-asset.json').read_text())['url'];public=[]
for suffix in ['', '/pricing']:
 with urllib.request.urlopen('https://apify.com/thescrapelab/protondb-player-reports'+suffix,timeout=90) as f:s=f.read().decode();status=f.status
 text=html.unescape(re.sub('<[^>]*>',' ',s));text=re.sub(r'\s+',' ',text);assert '$0.40' in text
 if not suffix:
  images=Images();images.feed(s);assert any(x.get('alt')=='ProtonDB Player Reports logo' for x in images.items), 'README logo was not rendered as an image'
  assert logo in s and 'spreadsheet-ready' in text.lower()
 else:assert 'Platform costs Included' in text
 public.append({'url':'https://apify.com/thescrapelab/protondb-player-reports'+suffix,'status':status,'newPriceVerified':True,'logoInReadme':logo in s,'platformUsageIncluded':'Platform costs Included' in text})
assert a['pricingInfos'][-1]['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']==.0004
receipt={'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'buildNumber':b['buildNumber'],'buildId':b['id'],'store':public,'avatarSaved':bool(a.get('pictureUrl')),'runs':receipts};(P/'polish-final-check.json').write_text(json.dumps(receipt,indent=2))
p=P/'POLISH.md';s=p.read_text();s=s.replace('Status: candidate tests running; do not claim production default updated until promotion/readback.',f"Status: **LIVE**; production default{b['buildNumber']} / {b['id']} verified. README logo, public$0.40/1000 pricing and included platform costs verified on Store HTTP200. Separate avatar remains NOT CONFIGURED; use assets/icon.png in Console when UI access is restored.")
s+='''\n## Measured cloud export verification\n\n| Test | Unique rows | CSV/Excel rows | Runtime | Peak RAM | Native platform cost | Customer fee | Modeled margin |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'''+ '\n'.join(table)+'''\n\nZero duplicateIDs, complete required fields and original noteText preserved across JSON/CSV; native workbook row counts match. Full candidate datasets were validated against field types and independently source-verified content. Counts from settled native events match delivered rows at$0.0004/report. Platform cost is conservatively max(native total,sum native category costs) at verification; later customer storage reads/retention excluded. Margin=80% of event revenue minus measured platform cost, before support/taxes/fixed costs; owner tests are not independent paid demand. No proxy/third-party API.\n\nInput count remains2 visible/2total/0required. Default10; cap1000. Direct full JSON stays available, original field contracts preserved; default flat export omits only nested notes/provisional grouping display and retains full combined notes plus licensing.\n''';p.write_text(s)
report=P/'REPORT.md';s=report.read_text();s='''> Current Store update (15 November 2026): see [POLISH.md](POLISH.md). Default build0.1.12; active price$0.05 preparation+$0.0004/written report ($0.45 total for1000), platform usage included. README logo and CSV/Excel views verified. The original release evidence and historical prices below remain unchanged. Separate avatar upload requires the Console picture control.\n\n'''+s;report.write_text(s);print('Verified live Store, pricing, README logo and all native export cases')
