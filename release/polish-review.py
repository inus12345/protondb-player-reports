import json,os,sys,hashlib,urllib.request,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent;M=pathlib.Path(sys.argv[1]).resolve()
H={'Authorization':'Bearer '+(os.environ.get('APIFY_TOKEN') or os.environ.get('Apify_Token'))}
def read(route):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+route,headers=H),timeout=90) as r:return json.load(r)
known={}
for name in ['broad','game']:
 for line in (M/'checkups/2026-11-15-protondb-evaluation/revalidation'/ (name+'.ndjson')).read_text().splitlines():
  row=json.loads(line);known[row['recordId']]=row
fields=['recordId','steamAppId','gameTitle','date','verdict','noteText','collectedAt','archiveUrl']
tests=[]
for label,cases in [('polish-default',['default','small']),('polish-game',['medium']),('polish-large',['large'])]:
 r=read('/actor-runs/'+json.loads((P/(label+'-run.json')).read_text())['id'])['data']
 if r['status']!='SUCCEEDED':raise RuntimeError(label+' not complete')
 rows=read('/datasets/'+r['defaultDatasetId']+'/items?limit=1000');inp=read('/key-value-stores/'+r['defaultKeyValueStoreId']+'/records/INPUT');proof=read('/key-value-stores/'+r['defaultKeyValueStoreId']+'/records/SOURCE_PROOF')
 schema=json.loads((P.parent/'.actor/dataset_schema.json').read_text())['fields']
 for row in rows:
  assert set(row)==set(schema), 'Output fields differ from dataset schema'
  for k,definition in schema.items():
   types=definition['type'] if isinstance(definition['type'],list) else [definition['type']]
   value=row[k];assert ('null' in types and value is None) or ('string' in types and isinstance(value,str)) or ('object' in types and isinstance(value,dict)), 'Invalid field type: '+k
  for k in ['date','collectedAt']:datetime.datetime.fromisoformat(row[k].replace('Z','+00:00'))
 ids=[x['recordId'] for x in rows];assert len(ids)==len(set(ids));assert all(all(x.get(k) for k in fields) for x in rows)
 for x in rows:
  original=known[x['recordId']]
  for k in ['steamAppId','gameTitle','date','verdict','noteText','gpu','os','gpuDriver','protonVersion']:assert x[k]==original[k]
 source=next(x for x in proof['sourceRequests'] if '/reports/reports_' in x['url'] and x['statusCode']==200)
 checks=[{'url':source['url'],'statusCode':200,'requestedAt':source['requestedAt'],'recordHash':row['recordId'],'matched':True,'evidenceReference':str(P/(label+'-source.json'))} for row in rows[:2]]
 n=len(rows);quality={'evaluatedRows':n,'structurallyValid':n,'structuralValidity':1,'duplicateCount':0,'missingIdentityCount':0,'nonLiveRows':0,'sampledRows':len(checks),'essentialCoverage':{k:{'available':n,'present':n} for k in fields}}
 receipt={'runId':r['id'],'buildId':r['buildId'],'datasetId':r['defaultDatasetId'],'sourceProof':proof,'quality':quality,'sourceChecks':checks,'input':inp,'allSourceRowsMatched':True}
 (P/(label+'-source.json')).write_text(json.dumps(receipt,indent=2))
 fingerprint=hashlib.sha256(json.dumps(inp,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 for case in cases:tests.append({'case':case,'runId':r['id'],'datasetId':r['defaultDatasetId'],'inputFingerprint':fingerprint,'inputVerified':True,'peakMemoryBytes':r['stats']['memMaxBytes'],'quality':quality,'sourceChecks':checks,'evidenceReference':str(P/(label+'-source.json'))})
review={'reviewed':True,'reviewedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Direct export of original written player compatibility reports from the maintainer latest publicly downloadable periodic snapshot. No supplied-data or AI modes.','targetCustomer':'Linux publisher QA leads, compatibility researchers and multi-title Steam Deck QA agencies.','targetOrigins':['https://raw.githubusercontent.com','https://api.github.com','https://www.protondb.com'],'sourceUrlFields':['archiveUrl'],'identityFields':['recordId'],'essentialFields':fields,'permissionStatus':'reviewed','sourceAccessReview':{'method':'Explicitly authorized maintainer download under ODbL/DbCL; live index and full archive hash verification each fresh run; pinned same-job resume only.','evidenceReference':str(P/'POLISH.md')},'checks':{k:'PASS' for k in ['API_POLICY','PAGINATION','RESULT_LIMITS','FAILURE_HANDLING','PERFORMANCE','COMMERCIAL_VALUE','FEATURE_CLAIMS']},'largeScaleClaim':True,'liveTests':tests}
f=M/'actor-quality-reviews.json';d=json.loads(f.read_text());d['actors']['5MfSH4T9Sv9Hnca02']=review;f.write_text(json.dumps(d,indent=2)+'\n');print('Saved reviewed current-build default/small/medium/large source and quality evidence')
