import os,json,urllib.request,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent
H={'Authorization':'Bearer '+(os.getenv('APIFY_TOKEN') or os.getenv('Apify_Token'))}
def api(path):
 with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2'+path,headers=H),timeout=90) as f:return json.load(f)
actor=api('/acts/5MfSH4T9Sv9Hnca02')['data'];table=[];econ=[]
for label in ['safe-default','safe-game','medium','safe-large','repeat-large','release-empty','budget','production']:
 f=P/(label+'-run.json')
 if not f.exists():continue
 r=api('/actor-runs/'+json.loads(f.read_text())['id'])['data'];f.write_text(json.dumps(r,indent=2));rows=api('/datasets/'+r['defaultDatasetId']+'/items?limit=1000');n=len(rows);assert len({x['recordId'] for x in rows})==n
 
 if label.startswith('safe-') or label in ['production','budget']:
  assert r.get('chargedEventCounts')=={'export-preparation':1,'written-report':n}, 'Native billing mismatch: '+label
 cost=r.get('usageTotalUsd',0);sec=r['stats']['runTimeSecs'];ram=r['stats']['memMaxBytes']/1048576
 table.append(f"| [{label}](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/{r['id']}) | {n} | {sec:.3f}s | {ram:.1f} MiB | ${cost:.6f} | {r['status']} |")
 if n: 
  gross=.05+.0005*n;profit=.8*gross-cost;econ.append(f'| {label} | {n} | ${gross:.4f} | ${cost:.6f} | ${cost/n*1000:.5f} | ${profit:.6f} | {profit/gross:.1%} |')
large=json.loads((P/'safe-large-run.json').read_text());large=api('/actor-runs/'+large['id'])['data'];proof=api('/key-value-stores/'+large['defaultKeyValueStoreId']+'/records/SOURCE_PROOF');(P/'safe-large-proof.json').write_text(json.dumps(proof,indent=2))
rows=api('/datasets/'+large['defaultDatasetId']+'/items?limit=2');examples=[]
for x in rows:
 examples.append({k:x.get(k) for k in ['steamAppId','gameTitle','date','verdict','gpu','os','gpuDriver','protonVersion']});examples[-1]['noteText']=x['noteText'][:140]+(' [remainder redacted]' if len(x['noteText'])>140 else '')
recovery=json.loads((P/'native-recovery-fixed-check.json').read_text());assert recovery['passed']
pricing=actor['pricingInfos'][-1];(P/'production-pricing.json').write_text(json.dumps(pricing,indent=2))
allruns=api('/acts/5MfSH4T9Sv9Hnca02/runs?limit=100')['data']['items'];builds=api('/acts/5MfSH4T9Sv9Hnca02/builds?limit=100')['data']['items'];total=sum(x.get('usageTotalUsd',0) for x in allruns+builds)
state='LIVE' if actor.get('isPublic') else 'PRIVATE'
report=f'''# ProtonDB Player Reports release report

Updated {datetime.datetime.now(datetime.timezone.utc).isoformat()}. Publication: **{state}**.

Actor ID `5MfSH4T9Sv9Hnca02`; [Console](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02); [Store](https://apify.com/thescrapelab/protondb-player-reports); [public GitHub repository](https://github.com/inus12345/protondb-player-reports). Default deployed build `{actor['taggedBuilds']['latest']['buildNumber']}` / `{actor['taggedBuilds']['latest']['buildId']}`. Runtime commit bb7a111. Source https://github.com/bdefore/protondb-data .

## Implementation and scope

Node24, Apify SDK3.7.2, ordinary first-party HTTPS, Git blob integrity verification, streaming JSON and bounded temporary SQLite newest-row selection. No proxies, browser, paid external API or shared stale cache. Each fresh run resolves the archive index and downloads the real publisher file. Resume pins the original manifest. Two inputs: optional game/hardware `filter`, and `maxResults` default10, cap1000. README documents full output, schema, cadence, licensing and usage. No website pagination or deep links are required: one index request and one archive download per cold run.

Maintainer snapshots are generally monthly, with irregular dates. Latest verified file `{proof['snapshot']['name']}`, Git blob `{proof['snapshot']['blobSha']}`, {proof['downloadBytes']:,} downloaded bytes. This is not a real-time feed; the filename is not a guaranteed cutoff. Public transformation code and attribution/ODbL/DbCL links are supplied in README, NOTICE and every row. Code MIT licensing does not relicense source data.

## Tests and measured costs

| Test | Unique results | Runtime | Peak RAM | Native platform cost | Status |
|---|---:|---:|---:|---:|---|
'''+ '\n'.join(table)+f'''

Ten automated local tests pass, including schema generations, similar-record identity, invalid inputs, limits, integrity/truncation failure, access denial, transient retry, pinned resume and billing reconciliation. GitHub CI passes. Progressive500 and fresh-repeat1000 runs are historical earlier builds; safe-default/game/large validate the exact production build. Mandatory fields and types are validated across every final dataset row; 1000 source identities/content match independent archive verification. Zero duplicate dataset IDs; no proxies. Sparse filters may return fewer rows. The budget test deliberately returns only one of ten requested rows and identifies the spending limit.

Full scan: fetched {proof['fetched']:,}; emitted {proof['emitted']:,}; suppressed duplicates {proof['duplicates']:,}; incomplete {proof['incomplete']:,}; missing/short written notes {proof['withoutSubstantiveNotes']:,}; eligible distinct {proof['eligibleTotal']:,}; excluded by result limit {proof['excludedByLimit']:,}. Counts are source records, not game summaries. Peak RAM is native Apify run metadata, not estimated process RSS. All native run/build usage currently totals **${total:.6f}**, below the $10 authorization; owner event counters are not independent customer revenue. Settled owner compute rate is conservatively retained in economics.

### Large-run native resource breakdown

The 1000-row run's Apify-metered quantities and USD costs (including storage operations and transfer) are preserved below. HTTP requests are not a separate paid provider: two first-party source requests, no proxy. Later dataset reads/retention are outside the completed run's metered total.

```json
{json.dumps({'usage':large['usage'],'costUsd':large['usageUsd']},indent=2)}
```

[Published storage rates](https://apify.com/pricing) include$1 per1000GB-hours on the entry paid tiers. As an illustrative30-day retention reserve, each additional1MB of dataset/manifest storage costs about$0.00072; this is a projection, not a settled measured invoice. Standard account retention and customer reads vary.

## Identity, recovery and billing

`recordId` is SHA256 of source-record content. Exact duplicates collapse; similar notes remain distinct. Source has no dependable author report ID across generations: content changes create new IDs; `identityCandidate` is only a grouping clue. The prior independent October–November archive comparison found395300 unchanged raw content identities and5439 additions, with no observed edits or removals. The fresh repeat used the same archive hash and returned the same1000selected IDs; no natural content change was observed during cloud testing. Local similar-record fixtures verify that differing notes remain distinct, but are not evidence of an actual player edit. Fresh exports may legitimately return the same IDs and incur new export charges. Resume/resurrection of the same run reconciles existing dataset IDs and native cumulative billing counts.

A controlled old-build fault test exposed double billing after local ledger loss. That build was never published. Fixed replay [{recovery['runId']}](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/{recovery['runId']}) retained10unique rows, preparation1/report10 before and after deletion of the local billing acknowledgement. The first finished production metadata briefly showed report0 before settling to report10 without another charge or run. Billing/cost verification therefore uses settled metadata; wait for counters and stored results to settle before manually resurrecting an interrupted export. Uncertain prior dataset appends stop for reconciliation instead of blindly repeating. A failure before a selection manifest exists may require another full download. Resume using Apify's resurrect action on the original run; starting a fresh run is a separate billed export.

## Monetization and contribution

Saved/verified PPE: `export-preparation` **$0.05 once per export**, plus primary `written-report` **$0.0005 each / $0.50 per1000**. No tier discounts; no automatic startup/dataset-item events in the active schedule. Minimum max charge$0.0505. Preparation is charged even for empty matches or later failure. Platform usage is included under standard PPE. Own runs display USER usage billing, so these measurements do not independently prove a third-party invoice. Public Store and pricing pages were fetched anonymously with HTTP200: $0.50/1000 written reports, $0.05 preparation, and platform costs explicitly Included on all displayed tiers. The public README matches the periodic-source and recovery descriptions.

Current [Apify PPE rules](https://docs.apify.com/actors/monetize/pay-per-event) give80% of eligible event revenue before developer-paid platform costs. Below are modeled paying-customer contributions using measured native owner run costs, not realized revenue; support, taxes and fixed-plan allocation excluded.

| Case | Rows | Customer events total | Measured platform | Cost/1000 usable | Contribution after20% fee | Gross margin |
|---|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(econ)+'''

10,000-row collection is NOT offered. A linear projection using the500 control and earlier/final1000 runs gives roughly1111–1684seconds. Extrapolating settled500($0.024917) and final1000($0.036833) platform totals gives approximately$0.2513 for10000($0.02513/1000), including the same compute, transfer and storage-operation categories, excluding later retention. These are projections, not a verified capacity or price offer; network variance and SDK operations make them uncertain. Future expansion requires its own cloud test.

## Commercial rationale

[Five-Actor competitor comparison](COMPETITORS.md) dated15November2026 includes TheScrapeLab's existing Steam Review Changes Tracker; it handles Steam reviews, not ProtonDB hardware compatibility notes, so this is not a duplicate Actor. Closest ProtonDB summary Actor charges$0.45/1000 game summaries with one monthly user; adjacent Steam review Actors charge$0.25–$1/1000 reviews depending on plan. Those units are not equivalent to individual player compatibility reports. This product removes archive download, schema normalization, newest-report selection and exact deduplication work. Free source downloads remain better for technically capable buyers requiring the complete database.

Buyer: Linux publisher or multi-title Steam Deck QA lead deciding which player symptoms and configurations to reproduce after updates. Approved feasibility evidence found paid QA budgets and recurring filtering/version frustrations, but no verified exact/adjacent Apify Ideas request, export-specific willingness to pay or independent paying adoption. This is a bounded launch experiment, not proof of demand. The cheapest next commercial test is observe one independent buyer's paid export and repeat usage, with no new feature work or unsolicited outreach.

## Representative output and spot-check

Below are two real source rows; long free text is truncated for this report. Full notes are delivered to customers. No player names or contact fields are exported.

```json
'''+json.dumps(examples,indent=2)+'''
```

Final source receipts record actual archive HTTP200 timestamps within their runs. All1000 report IDs and comparison fields agree with the independent verified source sample. Representative historical schema tests preserve original ratings/notes without inventing versions or GPUs.

## Remaining limits and follow-up

Manual first-week review: distinguish owner/free usage from independent paid customers, measure repeat exports, net contribution, empty-filter costs and recovery support. First official daily QA success remains distinct from manual owner runs. No recurring jobs were created. Each customer run uses its own container and native storage; no cross-customer mutable cache is required. Simultaneous multi-customer load was not tested, and source-wide limits still apply. Version/hardware omissions and unreliable author identity are source limitations. Do not expand beyond1000 until demand and runtime justify it.
'''
(P/'REPORT.md').write_text(report);print('report saved',state,'native total',total)
