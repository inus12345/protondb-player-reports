import os,json,time,urllib.request,pathlib,csv,io,zipfile,xml.etree.ElementTree as ET
P=pathlib.Path(__file__).resolve().parent
H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token')),'Content-Type':'application/json'}
def api(route,body=None,raw=False):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+route,headers=H,data=json.dumps(body).encode() if body is not None else None),timeout=90) as f:return f.read() if raw else json.load(f)
def wait(route):
 while True:
  d=api(route)['data']
  if d['status'] not in ['READY','RUNNING','ABORTING','TIMING-OUT']:return d
  time.sleep(10)
a=api('/acts/5MfSH4T9Sv9Hnca02')['data'];b=wait('/actor-builds/'+a['taggedBuilds']['latest']['buildId']);assert b['status']=='SUCCEEDED';print('Verified deployed build',b['buildNumber'],flush=True)
for label,inp,n,cap in [('nov16-default',{'maxResults':10},10,.25),('nov16-game',{'filter':'game:292030','maxResults':100},100,.25)]:
 r=api('/acts/5MfSH4T9Sv9Hnca02/runs?build='+b['buildNumber']+'&memory=1024&timeout=900&maxTotalChargeUsd='+str(cap),inp)['data'];(P/(label+'-run.json')).write_text(json.dumps(r,indent=2));print(label,r['id'],'started',flush=True)
 r=wait('/actor-runs/'+r['id']);assert r['status']=='SUCCEEDED'
 for _ in range(18):
  if r.get('chargedEventCounts')=={'written-report':n,'export-preparation':1}:break
  time.sleep(5);r=api('/actor-runs/'+r['id'])['data']
 assert r['chargedEventCounts']=={'written-report':n,'export-preparation':1}
 assert r['pricingInfo']['pricingPerEvent']['actorChargeEvents']['written-report']['eventPriceUsd']==.0004
 rows=api('/datasets/'+r['defaultDatasetId']+'/items?limit=1000');view=api('/datasets/'+r['defaultDatasetId']+'/items?view=reports&limit=1000');csvrows=list(csv.DictReader(io.StringIO(api('/key-value-stores/'+r['defaultKeyValueStoreId']+'/records/REPORTS.csv',raw=True).decode('utf-8-sig'))))
 book=api('/key-value-stores/'+r['defaultKeyValueStoreId']+'/records/REPORTS.xlsx',raw=True)
 with zipfile.ZipFile(io.BytesIO(book)) as z:sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));excelRows=len(sheet.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'))-1
 import openpyxl
 workbook=openpyxl.load_workbook(io.BytesIO(book),read_only=False,data_only=False);sheet=workbook.active;values=list(sheet.values);headers=values[0];noteCol=headers.index('noteText');idCol=headers.index('recordId');dateCol=headers.index('date')
 assert all(x['noteText']==v[noteCol] for x,v in zip(rows,values[1:])), 'Excel altered player notes'
 assert all(x['recordId']==v[idCol] and x['date']==v[dateCol] for x,v in zip(rows,values[1:]))
 assert sheet.freeze_panes=='A2' and sheet.auto_filter.ref=='A1:S'+str(n+1)
 assert len(rows)==len(view)==len(csvrows)==excelRows==n
 assert len({x['recordId'] for x in rows})==n
 assert all(x['noteText']==y['noteText'] for x,y in zip(rows,csvrows))
 assert all(x['databaseLicense'] and x['contentsLicense'] and x['attribution'] for x in view)
 assert 'notes' not in csvrows[0] and 'identityCandidate' not in csvrows[0]
 valid=sum(all(x.get(k) for k in ['recordId','steamAppId','gameTitle','date','verdict','noteText','collectedAt']) for x in rows);assert valid==n
 proof={'count':n,'unique':n,'valid':valid,'csvRows':len(csvrows),'excelRows':excelRows,'excelExactNotes':n,'excelIdsAndDates':n,'frozenHeader':True,'filterEnabled':True,'viewRows':len(view),'runtimeSeconds':r['stats']['runTimeSecs'],'peakRamBytes':r['stats']['memMaxBytes'],'usageTotalUsd':r.get('usageTotalUsd'),'status':r['status'],'nativeBilling':r['chargedEventCounts'],'reportEventPriceUsd':.0004,'flatSpreadsheetColumns':list(csvrows[0])};(P/(label+'-quality.json')).write_text(json.dumps(proof,indent=2));(P/(label+'-run.json')).write_text(json.dumps(r,indent=2));print(label,proof,flush=True)
