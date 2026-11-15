import os,json,urllib.request,pathlib,csv,io,zipfile,xml.etree.ElementTree as ET,datetime
P=pathlib.Path('release');H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token'))}
def get(path,raw=False):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+path,headers=H),timeout=90) as f:return f.read() if raw else json.load(f)
r=get('/actor-runs/'+json.loads((P/'last-stress-run.json').read_text())['id'])['data'];assert r['status']=='SUCCEEDED'
rows=get('/datasets/'+r['defaultDatasetId']+'/items?limit=1000');view=get('/datasets/'+r['defaultDatasetId']+'/items?view=reports&limit=1000');csvrows=list(csv.DictReader(io.StringIO(get('/datasets/'+r['defaultDatasetId']+'/items?view=reports&format=csv&limit=1000',True).decode('utf-8-sig'))))
book=get('/datasets/'+r['defaultDatasetId']+'/items?view=reports&format=xlsx&limit=1000',True);ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(io.BytesIO(book)) as z:
 shared=[]
 if 'xl/sharedStrings.xml' in z.namelist():shared=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
 sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));table=[]
 for row in sheet.findall('.//s:sheetData/s:row',ns):
  cells={}
  for c in row.findall('s:c',ns):
   name=''.join(x for x in c.attrib['r'] if x.isalpha());typ=c.attrib.get('t');v=c.find('s:v',ns)
   if typ=='s':value=shared[int(v.text)] if v is not None else ''
   elif typ=='inlineStr':value=''.join(c.find('s:is',ns).itertext())
   else:value=v.text if v is not None else ''
   cells[name]=value
  table.append(cells)
 headers=table[0];excel=[{headers[k]:value for k,value in x.items()} for x in table[1:]]
assert len(rows)==len(view)==len(csvrows)==len(excel)==1000
assert len({x['recordId'] for x in rows})==1000
assert all(x['noteText']==y['noteText']==z['noteText'] for x,y,z in zip(rows,csvrows,excel)), 'Note text changed in exported files'
assert all(x['recordId']==y['recordId']==z['recordId'] for x,y,z in zip(rows,csvrows,excel))
assert all(x['date']==y['date']==z['date'] for x,y,z in zip(rows,csvrows,excel))
assert all(x['databaseLicense'] and x['contentsLicense'] and x['attribution'] for x in view)
schema=json.loads(pathlib.Path('.actor/dataset_schema.json').read_text());essential=['recordId','steamAppId','gameTitle','date','verdict','noteText','collectedAt','archiveUrl']
for x in rows:
 assert set(x)==set(schema['fields']);assert all(x.get(k) for k in essential)
 for k,d in schema['fields'].items():
  ts=d['type'] if isinstance(d['type'],list) else [d['type']];v=x[k];assert (v is None and 'null' in ts) or (isinstance(v,str) and 'string' in ts) or (isinstance(v,dict) and 'object' in ts)
 for k in ['date','collectedAt']:datetime.datetime.fromisoformat(x[k].replace('Z','+00:00'))
 assert len(x['noteText'].strip())>=20 and len(x['noteText'].split())>=4
known={x['recordId']:x for x in map(json.loads,pathlib.Path('../..').joinpath('Apify_Manager/Apify_Manager/checkups/2026-11-15-protondb-evaluation/revalidation/broad.ndjson').read_text().splitlines())}
for x in rows:
 for k in ['recordId','steamAppId','gameTitle','date','verdict','noteText','gpu','os','gpuDriver','protonVersion']:assert x[k]==known[x['recordId']][k]
old=json.loads((P/'polish-large-quality.json').read_text());assert old['count']==len(rows)
proof=get('/key-value-stores/'+r['defaultKeyValueStoreId']+'/records/SOURCE_PROOF');native=get('/datasets/'+r['defaultDatasetId'])['data'];nativeSchema=native['schema'];assert list(nativeSchema['views'])[0]=='reports';assert nativeSchema==schema
build=get('/acts/5MfSH4T9Sv9Hnca02/builds/default')['data'];output=build['actorDefinition']['output'];assert output==json.loads(pathlib.Path('.actor/output_schema.json').read_text())
result={'runId':r['id'],'buildId':r['buildId'],'rows':1000,'structurallyValid':1000,'duplicateCount':0,'sourceMatchedRows':1000,'csvNoteMatches':1000,'excelNoteMatches':1000,'exportIdAndDateMatches':1000,'essentialFieldCoverage':{k:1000 for k in essential},'sourceSuppliedCounts':{k:sum(x[k] is not None for x in rows) for k in ['gpu','os','gpuDriver','protonVersion','protonVariant']},'minNoteChars':min(len(x['noteText']) for x in rows),'maxNoteChars':max(len(x['noteText']) for x in rows),'nativeDefaultView':'reports','nativeTableLabels':{k:v['label'] for k,v in nativeSchema['views']['reports']['display']['properties'].items()},'spreadsheetHeaders':list(csvrows[0]),'sourceProof':proof,'visualConsoleInspection':'UNVERIFIED: browser controls unavailable'}
(P/'last-output-check.json').write_text(json.dumps(result,indent=2));print({k:result[k] for k in ['runId','rows','sourceMatchedRows','csvNoteMatches','excelNoteMatches','duplicateCount','minNoteChars','maxNoteChars','sourceSuppliedCounts']})
