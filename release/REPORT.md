> Current Store update (15 November 2026): see [POLISH.md](POLISH.md). Default build0.1.12; active price$0.05 preparation+$0.0004/written report ($0.45 total for1000), platform usage included. README logo and CSV/Excel views verified. The original release evidence and historical prices below remain unchanged. Separate avatar upload requires the Console picture control.

# ProtonDB Player Reports release report

Updated 2026-11-15T16:55:01.768693+00:00. Publication: **LIVE**.

Actor ID `5MfSH4T9Sv9Hnca02`; [Console](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02); [Store](https://apify.com/thescrapelab/protondb-player-reports); [public GitHub repository](https://github.com/inus12345/protondb-player-reports). Default deployed build `0.1.11` / `CCkJRkujxFrddIS06`. Runtime commit bb7a111. Source https://github.com/bdefore/protondb-data .

## Implementation and scope

Node24, Apify SDK3.7.2, ordinary first-party HTTPS, Git blob integrity verification, streaming JSON and bounded temporary SQLite newest-row selection. No proxies, browser, paid external API or shared stale cache. Each fresh run resolves the archive index and downloads the real publisher file. Resume pins the original manifest. Two inputs: optional game/hardware `filter`, and `maxResults` default10, cap1000. README documents full output, schema, cadence, licensing and usage. No website pagination or deep links are required: one index request and one archive download per cold run.

Maintainer snapshots are generally monthly, with irregular dates. Latest verified file `reports_nov1_2026.tar.gz`, Git blob `f7cc83789b70458f5bae84fbce59fa14099db918`, 72,586,929 downloaded bytes. This is not a real-time feed; the filename is not a guaranteed cutoff. Public transformation code and attribution/ODbL/DbCL links are supplied in README, NOTICE and every row. Code MIT licensing does not relicense source data.

## Tests and measured costs

| Test | Unique results | Runtime | Peak RAM | Native platform cost | Status |
|---|---:|---:|---:|---:|---|
| [safe-default](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/EkdLuMoTk29dehPIG) | 10 | 203.402s | 304.4 MiB | $0.017395 | SUCCEEDED |
| [safe-game](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/y0QFciusmJcx2IxoV) | 100 | 217.248s | 272.3 MiB | $0.019450 | SUCCEEDED |
| [medium](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/5oCByp2J5xFCujjlb) | 500 | 229.772s | 278.8 MiB | $0.024917 | SUCCEEDED |
| [safe-large](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/tXAVJTHYQPYpIeKL1) | 1000 | 306.284s | 270.0 MiB | $0.036833 | SUCCEEDED |
| [repeat-large](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/hIewjDXuRNGs54dLE) | 1000 | 292.446s | 294.1 MiB | $0.035672 | SUCCEEDED |
| [release-empty](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/aoGtj2jhh8K2B1aex) | 0 | 166.244s | 266.7 MiB | $0.014095 | SUCCEEDED |
| [budget](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/HxRBcH5MpicTdeMqV) | 1 | 258.536s | 280.2 MiB | $0.021953 | SUCCEEDED |
| [production](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/2N3tLvWpgWxXZ1lE6) | 10 | 247.144s | 281.2 MiB | $0.021044 | SUCCEEDED |

Ten automated local tests pass, including schema generations, similar-record identity, invalid inputs, limits, integrity/truncation failure, access denial, transient retry, pinned resume and billing reconciliation. GitHub CI passes. Progressive500 and fresh-repeat1000 runs are historical earlier builds; safe-default/game/large validate the exact production build. Mandatory fields and types are validated across every final dataset row; 1000 source identities/content match independent archive verification. Zero duplicate dataset IDs; no proxies. Sparse filters may return fewer rows. The budget test deliberately returns only one of ten requested rows and identifies the spending limit.

Full scan: fetched 400,906; emitted 1,000; suppressed duplicates 148; incomplete 4; missing/short written notes 59,978; eligible distinct 340,776; excluded by result limit 339,776. Counts are source records, not game summaries. Peak RAM is native Apify run metadata, not estimated process RSS. All native run/build usage currently totals **$0.497411**, below the $10 authorization; owner event counters are not independent customer revenue. Settled owner compute rate is conservatively retained in economics.

### Large-run native resource breakdown

The 1000-row run's Apify-metered quantities and USD costs (including storage operations and transfer) are preserved below. HTTP requests are not a separate paid provider: two first-party source requests, no proxy. Later dataset reads/retention are outside the completed run's metered total.

```json
{
  "usage": {
    "ACTOR_COMPUTE_UNITS": 0.08507888888888888,
    "DATASET_READS": 0,
    "DATASET_WRITES": 1000,
    "KEY_VALUE_STORE_READS": 1,
    "KEY_VALUE_STORE_WRITES": 124,
    "KEY_VALUE_STORE_LISTS": 0,
    "REQUEST_QUEUE_READS": 0,
    "REQUEST_QUEUE_WRITES": 0,
    "DATA_TRANSFER_INTERNAL_GBYTES": 0.0009667864069342613,
    "DATA_TRANSFER_EXTERNAL_GBYTES": 0.00028075650334358215,
    "PROXY_RESIDENTIAL_TRANSFER_GBYTES": 0,
    "PROXY_SERPS": 0,
    "PROXY_UNBLOCKER_UNITS": 0
  },
  "costUsd": {
    "ACTOR_COMPUTE_UNITS": 0.025523666666666663,
    "DATASET_READS": 0,
    "DATASET_WRITES": 0.005,
    "KEY_VALUE_STORE_READS": 5e-06,
    "KEY_VALUE_STORE_WRITES": 0.006200000000000001,
    "KEY_VALUE_STORE_LISTS": 0,
    "REQUEST_QUEUE_READS": 0,
    "REQUEST_QUEUE_WRITES": 0,
    "DATA_TRANSFER_INTERNAL_GBYTES": 4.833932034671307e-05,
    "DATA_TRANSFER_EXTERNAL_GBYTES": 5.615130066871643e-05,
    "PROXY_RESIDENTIAL_TRANSFER_GBYTES": 0,
    "PROXY_SERPS": 0,
    "PROXY_UNBLOCKER_UNITS": 0
  }
}
```

[Published storage rates](https://apify.com/pricing) include$1 per1000GB-hours on the entry paid tiers. As an illustrative30-day retention reserve, each additional1MB of dataset/manifest storage costs about$0.00072; this is a projection, not a settled measured invoice. Standard account retention and customer reads vary.

## Identity, recovery and billing

`recordId` is SHA256 of source-record content. Exact duplicates collapse; similar notes remain distinct. Source has no dependable author report ID across generations: content changes create new IDs; `identityCandidate` is only a grouping clue. The prior independent October–November archive comparison found395300 unchanged raw content identities and5439 additions, with no observed edits or removals. The fresh repeat used the same archive hash and returned the same1000selected IDs; no natural content change was observed during cloud testing. Local similar-record fixtures verify that differing notes remain distinct, but are not evidence of an actual player edit. Fresh exports may legitimately return the same IDs and incur new export charges. Resume/resurrection of the same run reconciles existing dataset IDs and native cumulative billing counts.

A controlled old-build fault test exposed double billing after local ledger loss. That build was never published. Fixed replay [he1yA68pKwXGg8EDL](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/he1yA68pKwXGg8EDL) retained10unique rows, preparation1/report10 before and after deletion of the local billing acknowledgement. The first finished production metadata briefly showed report0 before settling to report10 without another charge or run. Billing/cost verification therefore uses settled metadata; wait for counters and stored results to settle before manually resurrecting an interrupted export. Uncertain prior dataset appends stop for reconciliation instead of blindly repeating. A failure before a selection manifest exists may require another full download. Resume using Apify's resurrect action on the original run; starting a fresh run is a separate billed export.

## Monetization and contribution

Saved/verified PPE: `export-preparation` **$0.05 once per export**, plus primary `written-report` **$0.0005 each / $0.50 per1000**. No tier discounts; no automatic startup/dataset-item events in the active schedule. Minimum max charge$0.0505. Preparation is charged even for empty matches or later failure. Platform usage is included under standard PPE. Own runs display USER usage billing, so these measurements do not independently prove a third-party invoice. Public Store and pricing pages were fetched anonymously with HTTP200: $0.50/1000 written reports, $0.05 preparation, and platform costs explicitly Included on all displayed tiers. The public README matches the periodic-source and recovery descriptions.

Current [Apify PPE rules](https://docs.apify.com/actors/monetize/pay-per-event) give80% of eligible event revenue before developer-paid platform costs. Below are modeled paying-customer contributions using measured native owner run costs, not realized revenue; support, taxes and fixed-plan allocation excluded.

| Case | Rows | Customer events total | Measured platform | Cost/1000 usable | Contribution after20% fee | Gross margin |
|---|---:|---:|---:|---:|---:|---:|
| safe-default | 10 | $0.0550 | $0.017395 | $1.73951 | $0.026605 | 48.4% |
| safe-game | 100 | $0.1000 | $0.019450 | $0.19450 | $0.060550 | 60.5% |
| medium | 500 | $0.3000 | $0.024917 | $0.04983 | $0.215083 | 71.7% |
| safe-large | 1000 | $0.5500 | $0.036833 | $0.03683 | $0.403167 | 73.3% |
| repeat-large | 1000 | $0.5500 | $0.035672 | $0.03567 | $0.404328 | 73.5% |
| budget | 1 | $0.0505 | $0.021953 | $21.95335 | $0.018447 | 36.5% |
| production | 10 | $0.0550 | $0.021044 | $2.10439 | $0.022956 | 41.7% |

10,000-row collection is NOT offered. A linear projection using the500 control and earlier/final1000 runs gives roughly1111–1684seconds. Extrapolating settled500($0.024917) and final1000($0.036833) platform totals gives approximately$0.2513 for10000($0.02513/1000), including the same compute, transfer and storage-operation categories, excluding later retention. These are projections, not a verified capacity or price offer; network variance and SDK operations make them uncertain. Future expansion requires its own cloud test.

## Commercial rationale

[Five-Actor competitor comparison](COMPETITORS.md) dated15November2026 includes TheScrapeLab's existing Steam Review Changes Tracker; it handles Steam reviews, not ProtonDB hardware compatibility notes, so this is not a duplicate Actor. Closest ProtonDB summary Actor charges$0.45/1000 game summaries with one monthly user; adjacent Steam review Actors charge$0.25–$1/1000 reviews depending on plan. Those units are not equivalent to individual player compatibility reports. This product removes archive download, schema normalization, newest-report selection and exact deduplication work. Free source downloads remain better for technically capable buyers requiring the complete database.

Buyer: Linux publisher or multi-title Steam Deck QA lead deciding which player symptoms and configurations to reproduce after updates. Approved feasibility evidence found paid QA budgets and recurring filtering/version frustrations, but no verified exact/adjacent Apify Ideas request, export-specific willingness to pay or independent paying adoption. This is a bounded launch experiment, not proof of demand. The cheapest next commercial test is observe one independent buyer's paid export and repeat usage, with no new feature work or unsolicited outreach.

## Representative output and spot-check

Below are two real source rows; long free text is truncated for this report. Full notes are delivered to customers. No player names or contact fields are exported.

```json
[
  {
    "steamAppId": "730",
    "gameTitle": "Counter-Strike 2",
    "date": "2026-11-02T03:13:11.000Z",
    "verdict": "yes",
    "gpu": "Mesa zink Vulkan 1.4(AMD Radeon 890M (RADV STRIX1) (MESA_RADV))",
    "os": "Arch Linux",
    "gpuDriver": "4.6 Mesa 26.2.5-arch1.1",
    "protonVersion": null,
    "noteText": "fixed with SDL_VIDEO_DRIVER=wayland\nfixed with SDL_VIDEO_DRIVER=wayland\nif you are on wayland and experience your mouse not working right or [remainder redacted]"
  },
  {
    "steamAppId": "1430190",
    "gameTitle": "Killing Floor 3",
    "date": "2026-11-02T01:57:23.000Z",
    "verdict": "yes",
    "gpu": "AMD Radeon RX 7900 XT (radeonsi, navi31, LLVM 17.0.6, DRM 3.56, 6.7.0-204.fsync.fc39.x86_64)",
    "os": "Nobara Linux 39 (KDE Plasma)",
    "gpuDriver": "4.6 Mesa 23.3.5",
    "protonVersion": "GE-Proton10-29",
    "noteText": "Crashes were fixed by using VKD3D_CONFIG=single_queue in the launch options\nGreat is game. Works well.\nEnabling of FSR 4.1 also possible usi [remainder redacted]"
  }
]
```

Final source receipts record actual archive HTTP200 timestamps within their runs. All1000 report IDs and comparison fields agree with the independent verified source sample. Representative historical schema tests preserve original ratings/notes without inventing versions or GPUs.

## Remaining limits and follow-up

Manual first-week review: distinguish owner/free usage from independent paid customers, measure repeat exports, net contribution, empty-filter costs and recovery support. First official daily QA success remains distinct from manual owner runs. No recurring jobs were created. Each customer run uses its own container and native storage; no cross-customer mutable cache is required. Simultaneous multi-customer load was not tested, and source-wide limits still apply. Version/hardware omissions and unreliable author identity are source limitations. Do not expand beyond1000 until demand and runtime justify it.

Release verification: Store/price HTTP200; production2N3tLvWpgWxXZ1lE6 SUCCEEDED with10unique JSON and CSV rows and native preparation1/report10. Manager publication-readiness READY at reports/2026-11-15T16-49-50Z; final post-production audit recorded separately in portfolio evidence.
