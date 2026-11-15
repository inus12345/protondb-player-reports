import { Actor } from 'apify';
import path from 'node:path';
import { collect, hash, validate } from './collector.mjs';

await Actor.init();
try {
    const input=await Actor.getInput()??{};
    const validated=validate(input);
    const result=await collect(input,{directory:path.resolve('.runtime/protondb'),job:'export'});
    const pin={snapshot:result.metrics.snapshot.blobSha,input:hash(validated),selection:hash(result.rows.map(r=>r.recordId))};
    const oldPin=await Actor.getValue('EXPORT_PIN');
    if(oldPin && hash(oldPin)!==hash(pin))throw new Error('Snapshot or selected records changed; start a new run instead of mixing exports.');
    await Actor.setValue('EXPORT_PIN',pin);
    const dataset=await Actor.openDataset();
    const existing=new Set();
    for(let offset=0;;offset+=1000) {
        const {items}=await dataset.getData({offset,limit:1000});
        for(const row of items){if(!row.recordId || existing.has(row.recordId))throw new Error('Existing dataset has invalid or duplicate records');existing.add(row.recordId);}
        if(items.length<1000)break;
    }
    const collectedAt=await Actor.getValue('COLLECTED_AT') || new Date().toISOString();
    await Actor.setValue('COLLECTED_AT',collectedAt);
    const selected=new Set(result.rows.map(r=>r.recordId));
    if([...existing].some(id=>!selected.has(id)))throw new Error('Existing dataset does not belong to this export');
    let deliveredThisExecution=0;
    for(const row of result.rows) {
        if(existing.has(row.recordId))continue;
        // Private test has no configured pricing. A future approved dataset-item
        // price must be reconciled against native events before publication.
        await Actor.pushData({...row,collectedAt});
        existing.add(row.recordId);deliveredThisExecution++;
    }
    await Actor.setValue('SOURCE_PROOF',{...result.metrics,deliveredThisExecution,datasetRows:existing.size,nativeBillingVerified:false});
    await Actor.setValue('LICENSE_NOTICE',{attribution:'Contains information from ProtonDB contributors, made available by bdefore under ODbL 1.0, with individual contents under DbCL 1.0. Normalization by TheScrapeLab.',databaseLicense:'https://opendatacommons.org/licenses/odbl/1-0/',contentsLicense:'https://opendatacommons.org/licenses/dbcl/1-0/',source:'https://github.com/bdefore/protondb-data',snapshot:result.metrics.snapshot,changes:'Field normalization, written-report selection, exact-content deduplication and date sorting. Report text retained.',alterations:'collector.mjs in the Actor source package; a public release must offer qualifying derivative data or alteration material under ODbL section 4.6.'});
    await Actor.setStatusMessage(`Delivered ${existing.size} written player reports from ${result.metrics.snapshot.date}.`);
} catch(error) {
    await Actor.fail(error.message);
}
await Actor.exit();
