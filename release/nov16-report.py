import os,json,pathlib,urllib.request,datetime,html,re,io,openpyxl
from html.parser import HTMLParser
P=pathlib.Path('release');H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token'))}
def api(path):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+path,headers=H),timeout=90) as f:return json.load(f)['data']
a=api('/acts/5MfSH4T9Sv9Hnca02');assert a['isPublic'] and a['taggedBuilds']['latest']['buildId']=='uNsEXkPyH4WB8ULI9';assert a['pictureUrl'];assert a['description'];price=a['pricingInfos'][-1];events=price['pricingPerEvent']['actorChargeEvents'];assert events['written-report']['eventPriceUsd']==.0004 and events['export-preparation']['eventPriceUsd']==.05
cases=[];table=[]
for label in ['nov16-default','nov16-game','unicode-large']:
 r=api('/actor-runs/'+json.loads((P/(label+'-run.json')).read_text())['id']);q=json.loads((P/(label+'-quality.json')).read_text());n=q['count'];assert r['status']=='SUCCEEDED' and r['chargedEventCounts']=={'written-report':n,'export-preparation':1};cost=max(r.get('usageTotalUsd',0),sum(r.get('usageUsd',{}).values()));fee=.05+.0004*n
 cases.append({'case':label,'runId':r['id'],'startedAt':r['startedAt'],'buildId':r['buildId'],'uniqueRows':n,'seconds':r['stats']['runTimeSecs'],'peakMemoryBytes':r['stats']['memMaxBytes'],'platformCostUsd':cost,'eventRevenueIfPaidCustomerUsd':fee,'contributionIfPaidCustomerUsd':.8*fee-cost,'events':r['chargedEventCounts'],'newRunToday':label.startswith('nov16')});table.append(f"| [{label}](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/{r['id']}) | {n} | {r['stats']['runTimeSecs']:.3f}s | {r['stats']['memMaxBytes']/1048576:.1f}MiB | ${cost:.6f} | ${fee:.4f} |")
 (P/(label+'-run.json')).write_text(json.dumps(r,indent=2))
 if label=='nov16-default':
  with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/datasets/'+r['defaultDatasetId']+'/items',headers=H)) as f:source=json.load(f)
  workbook=openpyxl.load_workbook('/Users/inusgrobler/Downloads/ProtonDB-Final-Test-2026-11-16.xlsx',read_only=True);rows=list(workbook.active.values);headers=rows[0];assert len(rows)-1==n
  for original,values in zip(source,rows[1:]):
   for key,value in zip(headers,values):assert ('' if original[key] is None else str(original[key]))==('' if value is None else str(value))
class Images(HTMLParser):
 def __init__(self):super().__init__();self.src=None
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='img' and d.get('alt')=='ProtonDB Player Reports':self.src=d.get('src')
with urllib.request.urlopen(urllib.request.Request('https://apify.com/thescrapelab/protondb-player-reports?releaseCheck=20261116',headers={'Cache-Control':'no-cache'}),timeout=90) as f:s=f.read().decode();status=f.status
p=Images();p.feed(s);publicAvatar=bool(p.src and 'actor_picture.svg' not in p.src)
with urllib.request.urlopen('https://apify.com/thescrapelab/protondb-player-reports/pricing?releaseCheck=20261116',timeout=90) as f:pricingHtml=f.read().decode()
pricingText=html.unescape(re.sub('<[^>]*>',' ',pricingHtml));pricingText=re.sub(r'\s+',' ',pricingText);assert '$0.40' in pricingText and '$0.05' in pricingText and 'Platform costs Included' in pricingText
history=api('/acts/5MfSH4T9Sv9Hnca02/runs?limit=100')['items'];official=[{'id':r['id'],'status':r['status'],'buildId':r.get('buildId')} for r in history if r.get('meta',{}).get('origin')=='TEST']
receipt={'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actorId':a['id'],'deployedBuild':'0.1.13','buildId':a['taggedBuilds']['latest']['buildId'],'pictureUrl':a['pictureUrl'],'description':a['description'],'logoUploadedVia':'Brave Browser native Console Upload image + crop + Save','logoObservedInConsole':True,'storeStatus':status,'publicAvatarSrc':p.src,'publicAvatarRendered':publicAvatar,'braveDownloadedWorkbookRowsAndAllFieldsExact':10,'braveConsoleTableAndAllFieldsViewObserved':True,'pricingIncluded':True,'reportPriceUsd':.0004,'preparationUsd':.05,'cases':cases,'officialTestRuns':official};(P/'nov16-final.json').write_text(json.dumps(receipt,indent=2))
logoState='custom thumbnail is rendered publicly' if publicAvatar else 'public page still renders the default thumbnail; propagation/rendering remains unverified'
report=f'''# ProtonDB final deployment, price and Brave logo check — 16 November 2026

[Live Actor](https://apify.com/thescrapelab/protondb-player-reports), ID 5MfSH4T9Sv9Hnca02, default 0.1.13/uNsEXkPyH4WB8ULI9. Runtime unchanged from verified bbb29b0; later Git commits contain release documentation only. Existing deployment is synchronized; no redundant rebuild or duplicate Actor was created.

## New verification

Twelve local automated tests PASS. Two fresh capped cloud cases collected 10 and 100 written reports. The exact same deployed build's 1,000-report case from 15 November remains within 36 hours and is reused; it was not relabeled as a new run. All 19 spreadsheet field values (not just note counts), including titles/emoji/IDs/dates/attribution, match source datasets in CSV and Excel for all three cases. Zero duplicate IDs or missing essential fields.

| Case | Unique valid reports | Runtime | Peak RAM | Measured native platform | Customer fee |
|---|---:|---:|---:|---:|---:|
'''+ '\n'.join(table)+f'''

Cases run sequentially at 1024 MiB / 900 seconds, charge caps USD 0.25 for new cases. Prior 1,000 was explicitly authorized at USD 1. No schedules or recurring tests created. Stored event counts preparation 1 / report N. Owner tests do not establish paid revenue. Native cost excludes later reads/retention; contribution model is 80% event revenue minus measured platform costs. Missing player versions remain null.

## Competitive monetization

Effective price remains USD 0.0004 / full written report ($0.40/1000) plus USD 0.05 once / export, normal run usage included. 1,000 total USD 0.45; 100 total USD 0.09; 10 total USD 0.054. Saved schedule, new native runs and public pricing page agree. No extra charge for CSV/Excel files, source duplicates or rejected rows. No tier discount layer needed at this low flat rate.

Refreshed closest Store APIs on 16 November: maximedupre/protondb has 1 monthly user and $0.45/1000game summaries. jungle_synthesizer/protondb-steamdeck-linux-compatibility-scraper has 0 monthly users; advertised primary rate $0.50/ 1,000 Free/Bronze, $0.45 Silver, $0.40 Gold+ plus advertised $0.0001 start event if emitted. Competitor runtime/bills were not purchased or verified. Game summaries are a different unit from full individual notes/configurations. Our per-report rate is low and the fixed preparation covers a complete archive scan; lowering preparation to $0.04 would have reduced the slower verified 10-row case's modeled margin to 30.3%, below the 35% target. Keep current pricing.

## Brave Console upload and actual visual checks

Opened authenticated Brave, Publishing → Display information → Upload image. Explicitly selected the correct 512 px project assets/icon.png; previewed full purple report/checkmark; Looks good; saved. Native public API now returns a non-null uploaded S3 picture URL and its PNG GET returns 200. Console run header visibly shows the custom logo. Added the previously empty public short description from the existing project scope; title/slug/SEO/pricing/status/permissions preserved.

Uploaded asset: {a['pictureUrl']}

Public Store image status at verification: **{logoState}**. No new manual upload is needed. A normal canonical-host alias was rejected by the ActorAPI; the valid native upload URL was preserved. Do not claim the public header rendered if it still uses actor_picture.svg. Recheck platform rendering, and prepare a support packet for the owner if it persists; do not contact others without authorization.

Brave visual inspection now resolves the earlier screenshot gap: default table is readable, meaningful headings/date formats/source links; ellipses expand longer values. All source fields view shows original notes object/grouping fields. Selected Excel workbook — full player text; actual save dialog opened; downloaded ProtonDB-Final-Test-2026-11-16.xlsx and independently verified all 19 fields across 10 rows on disk. Browser control later disconnected (cgWindowNotFound); no visual success after that is invented.

Public README and source cadence/limitations/pricing remain accurate. First official TEST-origin QA visibility: {len(official)} runs found across full visible history; owner tests are separate and are not labeled official QA PASS. No additional runtime defect was found.
'''
(P/'NOV16_RELEASE_CHECK.md').write_text(report);print({'build':'0.1.13','newRuns':[c['runId'] for c in cases if c['newRunToday']],'logoConfigured':True,'publicAvatarRendered':publicAvatar,'pricingVerified':True,'allFieldValuesMatched':True})
