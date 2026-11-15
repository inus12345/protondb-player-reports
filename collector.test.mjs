import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import { collect, validate, normalize, latest, records } from './collector.mjs';
const source = {app:{steam:{appId:'123'},title:'Test'},timestamp:1700000000,responses:{verdict:'yes',variant:'official',notes:{verdict:'It works with the listed graphics driver.'}},systemInfo:{gpu:'GPU',os:'Linux',gpuDriver:'Driver 1'}};
const snapshot={date:'2026-11-01',download_url:'https://raw.githubusercontent.com/bdefore/protondb-data/master/reports/reports_nov1_2026.tar.gz'};
const temp=()=>fs.mkdtempSync(path.join(os.tmpdir(),'protondb-test-'));
function fixture(rows) {
 const body=Buffer.from(JSON.stringify(rows)),header=Buffer.alloc(512);
 header.write('reports_piiremoved.json');header.write(body.length.toString(8).padStart(11,'0')+'\0',124);
 const gz=zlib.gzipSync(Buffer.concat([header,body,Buffer.alloc((512-body.length%512)%512+1024)]));
 const sha=crypto.createHash('sha1').update(`blob ${gz.length}\0`).update(gz).digest('hex');
 return {gz,entry:{...snapshot,name:'reports_nov1_2026.tar.gz',size:gz.length,sha}};
}
test('reject invalid controls before touching the source',async()=>{
 for(const input of [{maxResults:0},{maxResults:1.5},{maxResults:1001},{filter:'GPU'},{filter:'game:abc'},{extra:true}]) {
  assert.throws(()=>validate(input));let called=false;
  await assert.rejects(collect(input,{directory:temp(),fetcher:()=>{called=true;throw Error('network');}}));assert.equal(called,false);
 }
});
test('archive date selection uses dates, not lexical month order',()=>{
 const f=latest([{name:'reports_sep1_2026.tar.gz'},{name:'reports_nov1_2026.tar.gz'},{name:'README.md'}]);assert.equal(f.date,'2026-11-01');
});
test('similar reports retain different content identities',()=>{
 const a=normalize(source,snapshot).row,b=normalize({...source,responses:{...source.responses,notes:{verdict:'It crashes with the listed graphics driver.'}}},snapshot).row;
 assert.equal(a.identityCandidate,b.identityCandidate);assert.notEqual(a.recordId,b.recordId);
 assert.equal(a.protonVersion,null);assert.equal(a.protonVersionSpecificity,'not-supplied');
 const exact=normalize({...source,responses:{...source.responses,customProtonVersion:'GE-Proton10-29'}},snapshot).row;
 assert.equal(exact.protonVersionSpecificity,'reported-version-string');
});
test('legacy reports preserve original notes/rating without fabricating a GPU',()=>{
 const r=normalize({appId:'123',title:'Legacy',timestamp:1535971667,rating:'Borked',notes:'Crashes with a debug log',os:'Arch',specs:'CPU / GPU',protonVersion:'3.7'},snapshot).row;
 assert.equal(r.verdict,'Borked');assert.equal(r.gpu,null);assert.equal(r.noteText,'Crashes with a debug log');
});
test('truncated archive is an error, never a successful partial collection',async()=>{
 const d=temp(),f=path.join(d,'bad.gz');fs.writeFileSync(f,zlib.gzipSync(Buffer.from('incomplete')));
 await assert.rejects(async()=>{for await(const r of records(f))void r;});
});
test('integrity-checked collection orders newest, preserves similar rows, resumes and pins source',async()=>{
 const d=temp(),later={...source,timestamp:source.timestamp+5};
 const f=fixture([source,later,source,{...source,responses:{...source.responses,notes:{verdict:'Other notes with the same hardware and timestamp.'}}}]);
 const fetcher=async url=>url.includes('/contents/')?new Response(JSON.stringify([f.entry])):new Response(f.gz);
 const r=await collect({maxResults:10},{directory:d,job:'one',fetcher});
 assert.equal(r.rows.length,3);assert.equal(r.metrics.duplicates,1);assert.equal(r.rows[0].date,new Date(later.timestamp*1000).toISOString());
 const repeat=await collect({maxResults:10},{directory:d,job:'one',fetcher});assert.equal(repeat.metrics.simulatedBillableUnits,0);assert.equal(repeat.metrics.recovered,3);
 const empty=await collect({filter:'game:999',maxResults:10},{directory:d,job:'empty',fetcher});assert.equal(empty.rows.length,0);
 await assert.rejects(collect({maxResults:10},{directory:d,job:'one',fetcher:async()=>new Response(JSON.stringify([{...f.entry,sha:'changed'}]))}),/Snapshot or input changed/);
});
test('denial is not retried or presented as empty success',async()=>{
 let calls=0;await assert.rejects(collect({}, {directory:temp(),fetcher:async()=>{calls++;return new Response('denied',{status:403});}}),/403/);assert.equal(calls,1);
});
test('a transient source error retries and then retains real output',async()=>{
 const f=fixture([source]);let calls=0;
 const r=await collect({}, {directory:temp(),fetcher:async url=>{calls++;if(calls===1)return new Response('busy',{status:503,headers:{'retry-after':'1'}});return url.includes('/contents/')?new Response(JSON.stringify([f.entry])):new Response(f.gz);}});
 assert.equal(r.rows.length,1);assert.equal(calls,3);
});

import { unbilledCount } from './billing.mjs';
test('native charged prefix prevents rebilling after local receipt loss',()=>{
 assert.equal(unbilledCount(10,0,10),0);
 assert.equal(unbilledCount(1000,0,25),0);
 assert.equal(unbilledCount(25,25,25),25);
 assert.equal(unbilledCount(10,0,25),15);
});
test('invalid native counts fail rather than creating negative or duplicate charges',()=>{
 for(const n of [-1,NaN,1.5])assert.throws(()=>unbilledCount(n,0,25));
});
