import os,json,urllib.request,pathlib,io,csv,openpyxl
P=pathlib.Path('release');H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token'))}
def get(url,raw=False):
 with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=90) as f:return f.read() if raw else json.load(f)
checks=[]
for label in ['nov16-default','nov16-game','unicode-large']:
 r=json.loads((P/(label+'-run.json')).read_text());items=get('https://api.apify.com/v2/datasets/'+r['defaultDatasetId']+'/items?limit=1000');csvrows=list(csv.DictReader(io.StringIO(get(r['output']['csv'],True).decode('utf-8-sig'))));w=openpyxl.load_workbook(io.BytesIO(get(r['output']['excel'],True)),read_only=True);values=list(w.active.values);fields=list(values[0]);assert len(items)==len(csvrows)==len(values)-1
 for a,b,c in zip(items,csvrows,values[1:]):
  for key,cell in zip(fields,c):
   expected='' if a[key] is None else str(a[key]);assert b[key]==expected and ('' if cell is None else str(cell))==expected,(label,key)
 checks.append({'case':label,'runId':r['id'],'rows':len(items),'fieldsPerReport':len(fields),'csvAndExcelAllFieldValuesMatch':True,'newRunToday':label.startswith('nov16')})
(P/'nov16-file-values.json').write_text(json.dumps(checks,indent=2));print(checks)
