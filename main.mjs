import { Actor } from 'apify';
import path from 'node:path';
import { unbilledCount } from './billing.mjs';
import { collect, hash, validate } from './collector.mjs';
await Actor.init();
try {
 const input=validate(await Actor.getInput()??{});
 const startupInfo=Actor.getChargingManager().getPricingInfo();
 const startupRunId=process.env.ACTOR_RUN_ID||process.env.APIFY_ACTOR_RUN_ID;
 if(startupInfo.perEventPrices['export-preparation'] && startupRunId){
  const state=await Actor.newClient().run(startupRunId).get();
  if(!(state.chargedEventCounts?.['export-preparation']>0))await Actor.newClient().run(startupRunId).charge({eventName:'export-preparation',count:1,idempotencyKey:`preparation-${startupRunId}`});
 }
 let manifest=await Actor.getValue('EXPORT_MANIFEST');
 if(manifest && manifest.inputHash!==hash(input))throw new Error('Input changed; start a new export');
 if(!manifest){
  const result=await collect(input.filter?input:{maxResults:input.maxResults},{directory:path.resolve('.runtime/protondb'),job:'export'});
  const info=Actor.getChargingManager().getPricingInfo();
  if(info.perEventPrices['written-report']){
   const rid=process.env.ACTOR_RUN_ID||process.env.APIFY_ACTOR_RUN_ID;
   const run=await Actor.newClient().run(rid).get();
   const spent=Object.entries(run.chargedEventCounts??{}).reduce((sum,[k,n])=>sum+n*(info.perEventPrices[k]??0),0);
   const allowance=Math.max(0,Math.floor((info.maxTotalChargeUsd-spent+1e-9)/info.perEventPrices['written-report']));
   result.metrics.limitedByBudget=result.rows.length>allowance;result.rows=result.rows.slice(0,allowance);
  }
  manifest={inputHash:hash(input),rows:result.rows,collectedAt:new Date().toISOString(),metrics:result.metrics};
  await Actor.setValue('EXPORT_MANIFEST',manifest);
 }
 const client=Actor.newClient({maxRetries:0}),dataset=await Actor.openDataset();
 const existing=new Set();
 for(let offset=0;;offset+=1000){const {items}=await dataset.getData({offset,limit:1000});for(const row of items){if(!row.recordId||existing.has(row.recordId))throw new Error('Duplicate or invalid existing output');existing.add(row.recordId);}if(items.length<1000)break;}
 const pending=await Actor.getValue('PENDING_DELIVERY');
 if(pending?.recordIds?.some(id=>!existing.has(id)))throw new Error('Prior dataset write is not confirmed. No delivery was repeated. Wait for stored results to settle and resurrect; contact support if records remain missing.');
 const selected=new Set(manifest.rows.map(x=>x.recordId));
 if([...existing].some(id=>!selected.has(id)))throw new Error('Existing output does not match export');
 const pricing=Actor.getChargingManager().getPricingInfo();
 const runId=process.env.ACTOR_RUN_ID||process.env.APIFY_ACTOR_RUN_ID;
 const eventName='written-report',price=pricing.perEventPrices[eventName];
 const ledger=await Actor.getValue('DELIVERY_LEDGER')??{};
 let newRows=0;
 let billedPrefix=0;
 if(price&&runId){const native=await client.run(runId).get();billedPrefix=native.chargedEventCounts?.[eventName]??0;}
 if(billedPrefix>existing.size)throw new Error('Billed reports exceed confirmed dataset rows; stop for reconciliation');
 for(let i=0;i<manifest.rows.length;i+=25){
  const batch=manifest.rows.slice(i,i+25),key=hash(batch.map(r=>r.recordId));
  if(billedPrefix<i+batch.length && price && runId){
   const run=await client.run(runId).get();
   const total=Object.entries(run.chargedEventCounts??{}).reduce((s,[k,n])=>s+n*(pricing.perEventPrices[k]??0),0);
   if(total+unbilledCount(billedPrefix,i,batch.length)*price>pricing.maxTotalChargeUsd+1e-9){await Actor.setStatusMessage('Stopped at the spending limit; output is partial.');break;}
  }
  const missing=batch.filter(r=>!existing.has(r.recordId));
  if(missing.length){
   await Actor.setValue('PENDING_DELIVERY',{key,recordIds:missing.map(r=>r.recordId)});
   await client.dataset(dataset.id).pushItems(missing.map(row=>({...row,collectedAt:manifest.collectedAt})));
   for(const row of missing)existing.add(row.recordId);
   newRows+=missing.length;
  }
  if(billedPrefix<i+batch.length && price && runId){
   const delta=unbilledCount(billedPrefix,i,batch.length);
   await client.run(runId).charge({eventName,count:delta,idempotencyKey:`reports-${runId}-${key}`});
   billedPrefix=i+batch.length;
  }
  ledger[key]={rows:batch.length,billed:!!price};await Actor.setValue('DELIVERY_LEDGER',ledger);
  await Actor.setValue('PENDING_DELIVERY',null);
 }
 await Actor.setValue('SOURCE_PROOF',{...manifest.metrics,datasetRows:existing.size,deliveredThisExecution:newRows,billingConfigured:!!price});
 await Actor.setValue('LICENSE_NOTICE',{attribution:'ProtonDB contributors and bdefore; normalized by TheScrapeLab',databaseLicense:'https://opendatacommons.org/licenses/odbl/1-0/',contentsLicense:'https://opendatacommons.org/licenses/dbcl/1-0/',source:'https://github.com/bdefore/protondb-data',transformations:'https://github.com/inus12345/protondb-player-reports/blob/main/collector.mjs',snapshot:manifest.metrics.snapshot});
 await Actor.setStatusMessage(`Delivered ${existing.size} full written reports from snapshot ${manifest.metrics.snapshot.date}.${manifest.metrics.limitedByBudget?' Partial export: spending limit reached.':''}`);
} catch(error){await Actor.fail(error.message);}
await Actor.exit();
