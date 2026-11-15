import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { Readable, Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { DatabaseSync } from 'node:sqlite';

export const canonical = v => v && typeof v === 'object' ? Array.isArray(v) ? v.map(canonical) : Object.fromEntries(Object.keys(v).sort().map(k => [k, canonical(v[k])])) : v;
export const hash = v => crypto.createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');
export function validate(input = {}) {
    input = {...input}; if(typeof input.filter === 'string' && !input.filter.trim()) delete input.filter;
    const maxResults = input.maxResults ?? 10;
    if (!Number.isInteger(maxResults) || maxResults < 1 || maxResults > 10000) throw new Error('maxResults must be an integer from 1 to 10000');
    if (input.filter !== undefined && (typeof input.filter !== 'string' || !/^(game:[1-9]\d*|hardware:\S.{0,99})$/.test(input.filter))) throw new Error('filter must be game:STEAM_ID or hardware:TEXT');
    if (Object.keys(input).some(k => !['filter', 'maxResults'].includes(k))) throw new Error('Only filter and maxResults are supported');
    return { maxResults, filter: input.filter ?? '' };
}
export function latest(index) {
    const months = {jan:1,feb:2,mar:3,apr:4,may:5,jun:6,jul:7,aug:8,sep:9,oct:10,nov:11,dec:12};
    const files = index.flatMap(x => {
        const m = x.name.match(/^reports_([a-z]+)(\d+)_(\d+)\.tar\.gz$/);
        if (!m || !months[m[1]]) return [];
        return [{...x, date:`${m[3]}-${String(months[m[1]]).padStart(2,'0')}-${m[2].padStart(2,'0')}`}];
    }).sort((a,b) => a.date.localeCompare(b.date));
    if (!files.length) throw new Error('No supported archive in source index');
    return files.at(-1);
}
export function normalize(raw, snapshot) {
    const legacy = !raw.responses, r = raw.responses ?? {}, sys = raw.systemInfo ?? {};
    const appId = String(legacy ? raw.appId ?? '' : raw.app?.steam?.appId ?? '');
    const title = legacy ? raw.title : raw.app?.title;
    const notes = legacy ? {report:raw.notes} : {...r.notes};
    if (r.concludingNotes) notes.concludingNotes = r.concludingNotes;
    const writtenNotes = Object.fromEntries(Object.entries(notes).filter(([,v]) => typeof v === 'string' && v.trim()));
    const noteText = Object.values(writtenNotes).join('\n');
    const verdict = legacy ? raw.rating : r.verdict;
    const os = legacy ? raw.os : sys.os;
    const gpuDriver = legacy ? raw.gpuDriver : sys.gpuDriver;
    const gpu = legacy ? null : sys.gpu;
    const protonVersion = legacy ? raw.protonVersion : r.protonVersion || r.customProtonVersion;
    if (!/^\d+$/.test(appId) || typeof title !== 'string' || !title || !Number.isSafeInteger(raw.timestamp) || raw.timestamp <= 0 || !verdict || ![gpu,os,gpuDriver,protonVersion].some(Boolean)) return {reject:'incomplete'};
    if (noteText.trim().length < 20 || noteText.trim().split(/\s+/).length < 4) return {reject:'withoutSubstantiveNotes'};
    // Content identity deliberately preserves different reports sharing game/date/hardware.
    const recordId = hash(raw);
    const identityCandidate = hash({appId,timestamp:raw.timestamp,systemInfo:legacy ? {os,gpuDriver,specs:raw.specs} : sys});
    const exact = typeof protonVersion === 'string' && /\d+\.\d+|GE-Proton\d+|Proton-?\d+/i.test(protonVersion) && !/^(default|official|experimental|ge|native)$/i.test(protonVersion.trim());
    const row = {recordId,identityCandidate,steamAppId:appId,gameTitle:title,date:new Date(raw.timestamp*1000).toISOString(),verdict,notes:writtenNotes,noteText,gpu:gpu??null,os:os??null,gpuDriver:gpuDriver??null,protonVersion:protonVersion??null,protonVariant:r.variant??null,protonVersionSpecificity:exact?'reported-version-string':protonVersion?'unspecified-label':'not-supplied',snapshotDate:snapshot.date,sourceUrl:`https://www.protondb.com/app/${appId}`,archiveUrl:snapshot.download_url,attribution:'ProtonDB contributors; public export by bdefore. Normalized by TheScrapeLab.',databaseLicense:'https://opendatacommons.org/licenses/odbl/1-0/',contentsLicense:'https://opendatacommons.org/licenses/dbcl/1-0/'};
    return {row,timestamp:raw.timestamp,hardware:[gpu,os,gpuDriver].filter(Boolean).join('\n').toLowerCase()};
}
export async function* records(filename) {
    let header = Buffer.alloc(0), remaining = null, depth=0, quoted=false, escaped=false, obj='', started=false, ended=false;
    const decoder = new TextDecoder('utf-8',{fatal:true});
    for await (let chunk of fs.createReadStream(filename).pipe(zlib.createGunzip())) {
        if (remaining === null) {
            header=Buffer.concat([header,chunk]); if(header.length<512) continue;
            const name=header.subarray(0,100).toString().replace(/\0.*$/,'');
            if(!name.endsWith('.json')) throw new Error('Unexpected archive member');
            remaining=parseInt(header.subarray(124,136).toString().replace(/\0.*$/,'').trim(),8);
            if(!Number.isSafeInteger(remaining) || remaining<2) throw new Error('Invalid tar member size');
            chunk=header.subarray(512);header=null;
        }
        const data=chunk.subarray(0,remaining);remaining-=data.length;
        for(const c of decoder.decode(data,{stream:true})) {
            if(!depth) {
                if(!started){if(/\s/.test(c))continue;if(c!=='[')throw new Error('Expected JSON array');started=true;continue;}
                if(c===']'){ended=true;continue;}
                if(/\s|,/.test(c))continue;
                if(c!=='{' || ended)throw new Error('Invalid top-level JSON');
                depth=1;obj='{';continue;
            }
            obj+=c;
            if(obj.length>2_000_000)throw new Error('Oversized source record');
            if(quoted){if(escaped)escaped=false;else if(c==='\\')escaped=true;else if(c==='"')quoted=false;}
            else if(c==='"')quoted=true;
            else if(c==='{')depth++;
            else if(c==='}' && --depth===0){yield JSON.parse(obj);obj='';}
        }
    }
    if(remaining!==0 || depth || !ended)throw new Error('Truncated JSON archive');
}
async function request(url, metrics, fetcher) {
    for(let attempt=0;attempt<3;attempt++) {
        metrics.requests++;
        const r=await fetcher(url,{signal:AbortSignal.timeout(120000),headers:{'User-Agent':'TheScrapeLab-ProtonDB-archive-evaluation'}});
        if(r.ok)return r;
        if(![429,500,502,503,504].includes(r.status) || attempt===2)throw new Error(`Source HTTP ${r.status}`);
        const wait=Number(r.headers.get('retry-after')??(attempt+1));
        await r.body?.cancel();
        if(!Number.isFinite(wait)||wait>60)throw new Error('Source asks for a later retry; stop and resume later');
        await new Promise(resolve=>setTimeout(resolve,Math.max(1,wait)*1000));
    }
}
const atomic = (filename,data) => {fs.writeFileSync(filename+'.tmp',JSON.stringify(data,null,2));fs.renameSync(filename+'.tmp',filename);};
export async function collect(input={}, {directory, job='export', failAfter, fetcher=fetch}={}) {
    const validated=validate(input), started=Date.now();
    if(!directory)throw new Error('Internal storage directory required');
    if(!/^[a-z0-9-]+$/.test(job))throw new Error('Invalid internal job name');
    fs.mkdirSync(directory,{recursive:true});
    const metrics={requests:0,downloadBytes:0,fetched:0,emitted:0,duplicates:0,incomplete:0,withoutSubstantiveNotes:0,filteredOut:0,excludedByLimit:0,recovered:0,simulatedBillableUnits:0};
    const response=await request('https://api.github.com/repos/bdefore/protondb-data/contents/reports',metrics,fetcher);
    const snapshot=latest(await response.json());
    const output=path.join(directory,job+'.ndjson'),stateFile=path.join(directory,job+'-state.json');
    const state=fs.existsSync(stateFile)?JSON.parse(fs.readFileSync(stateFile)):null;
    if(state && (state.blobSha!==snapshot.sha || hash(state.input)!==hash(validated)))throw new Error('Snapshot or input changed; start a separate export');
    const archive=path.join(directory,snapshot.sha+'.tar.gz'),dbFile=path.join(directory,snapshot.sha+'-'+hash(validated).slice(0,16)+'.sqlite');
    const db=new DatabaseSync(dbFile);
    try {
        db.exec('PRAGMA journal_mode=MEMORY; PRAGMA synchronous=OFF; CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY,v TEXT); CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, ts INTEGER, game TEXT, hardware TEXT, payload TEXT);');
        const cached=db.prepare("SELECT v FROM meta WHERE k='counts'").get();
        if(!cached) {
            const download=await request(snapshot.download_url,metrics,fetcher);
            const blob=crypto.createHash('sha1').update(`blob ${snapshot.size}\0`);
            const counter=new Transform({transform(chunk,enc,cb){metrics.downloadBytes+=chunk.length;blob.update(chunk);cb(null,chunk);}});
            await pipeline(Readable.fromWeb(download.body),counter,fs.createWriteStream(archive+'.part'));
            if(metrics.downloadBytes!==snapshot.size || blob.digest('hex')!==snapshot.sha)throw new Error('Archive integrity mismatch');
            fs.renameSync(archive+'.part',archive);
            db.exec('BEGIN; DELETE FROM reports;');
            const insert=db.prepare('INSERT OR IGNORE INTO reports VALUES (?,?,?,?,?)');
            const sourceSeen=new Set(); metrics.eligibleTotal=0;metrics.filteredTotal=0;
            const trim=db.prepare('DELETE FROM reports WHERE id NOT IN (SELECT id FROM reports ORDER BY ts DESC,id LIMIT ?)');
            try {
                for await(const raw of records(archive)) {
                    metrics.fetched++;const n=normalize(raw,snapshot);
                    if(n.reject){metrics[n.reject]++;continue;}
                    if(sourceSeen.has(n.row.recordId)){metrics.duplicates++;continue;}sourceSeen.add(n.row.recordId);
                    const matches=!validated.filter || (validated.filter.startsWith('game:')?n.row.steamAppId===validated.filter.slice(5):n.hardware.includes(validated.filter.slice(9).toLowerCase()));
                    if(!matches){metrics.filteredTotal++;continue;}metrics.eligibleTotal++;
                    insert.run(n.row.recordId,n.timestamp,n.row.steamAppId,n.hardware,JSON.stringify(n.row));
                    if(metrics.eligibleTotal%100===0)trim.run(validated.maxResults);
                }
                trim.run(validated.maxResults);
                db.prepare('INSERT OR REPLACE INTO meta VALUES (?,?)').run('counts',JSON.stringify(metrics));
                db.exec('CREATE INDEX IF NOT EXISTS report_date ON reports(ts DESC,id); COMMIT;');
            } catch(e){db.exec('ROLLBACK;');throw e;}
        } else {
            const original=JSON.parse(cached.v);for(const k of ['fetched','duplicates','incomplete','withoutSubstantiveNotes','eligibleTotal','filteredTotal'])metrics[k]=original[k];
        }
        const [kind, ...rest]=validated.filter.split(':'),term=rest.join(':');
        const where=kind==='game'?'WHERE game=?':kind==='hardware'?'WHERE instr(hardware,?)>0':'';
        const args=where?[term.toLowerCase()]:[];
        const eligible=metrics.eligibleTotal;
        const unique=db.prepare('SELECT COUNT(*) AS n FROM reports').get().n;
        metrics.filteredOut=metrics.filteredTotal;
        const selected=db.prepare(`SELECT payload FROM reports ${where} ORDER BY ts DESC,id LIMIT ?`).all(...args,validated.maxResults).map(x=>JSON.parse(x.payload));
        metrics.excludedByLimit=Math.max(0,eligible-selected.length);
        if(state && state.selectionHash!==hash(selected.map(x=>x.recordId)))throw new Error('Resume selection changed');
        atomic(stateFile,{blobSha:snapshot.sha,input:validated,selectionHash:hash(selected.map(x=>x.recordId)),status:'delivering'});
        let delivered=[];
        if(fs.existsSync(output)) {
            const text=fs.readFileSync(output,'utf8'),end=text.lastIndexOf('\n');
            if(end!==text.length-1)fs.truncateSync(output,Buffer.byteLength(text.slice(0,end+1)));
            delivered=text.slice(0,end+1).split('\n').filter(Boolean).map(x=>JSON.parse(x));
        }
        const seen=new Set(delivered.map(x=>x.recordId));
        if(seen.size!==delivered.length || delivered.some((x,i)=>hash(x)!==hash(selected[i])))throw new Error('Existing output does not match selected source rows');
        metrics.recovered=delivered.length;
        const fd=fs.openSync(output,'a');
        try {
            for(const row of selected) {
                if(seen.has(row.recordId))continue;
                fs.writeSync(fd,JSON.stringify(row)+'\n');fs.fsyncSync(fd);
                // Test-only hard exit after durable output, before job completion acknowledgement.
                if(failAfter && seen.size+1===failAfter)process.exit(86);
                seen.add(row.recordId);metrics.simulatedBillableUnits++;
            }
        } finally {fs.closeSync(fd);}
        metrics.emitted=seen.size;metrics.elapsedMs=Date.now()-started;metrics.peakRssBytes=process.resourceUsage().maxRSS*1024;
        metrics.cacheHit=!!cached;metrics.snapshot={name:snapshot.name,date:snapshot.date,blobSha:snapshot.sha};
        atomic(stateFile,{blobSha:snapshot.sha,input:validated,selectionHash:hash(selected.map(x=>x.recordId)),status:'complete',metrics});
        return {rows:selected,metrics,output};
    } finally {db.close();}
}
