# ProtonDB final deployment, price and Brave logo check — 16 November 2026

[Live Actor](https://apify.com/thescrapelab/protondb-player-reports), ID 5MfSH4T9Sv9Hnca02, default 0.1.13/uNsEXkPyH4WB8ULI9. Runtime unchanged from verified bbb29b0; later Git commits contain release documentation only. Existing deployment is synchronized; no redundant rebuild or duplicate Actor was created.

## New verification

Twelve local automated tests PASS. Two fresh capped cloud cases collected 10 and 100 written reports. The exact same deployed build's 1,000-report case from 15 November remains within 36 hours and is reused; it was not relabeled as a new run. All 19 spreadsheet field values (not just note counts), including titles/emoji/IDs/dates/attribution, match source datasets in CSV and Excel for all three cases. Zero duplicate IDs or missing essential fields.

| Case | Unique valid reports | Runtime | Peak RAM | Measured native platform | Customer fee |
|---|---:|---:|---:|---:|---:|
| [nov16-default](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/bK1qS33V0D169AYZy) | 10 | 220.682s | 272.8MiB | $0.018940 | $0.0540 |
| [nov16-game](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/PBt7nO9ReJLd3vo66) | 100 | 184.691s | 271.1MiB | $0.016829 | $0.0900 |
| [unicode-large](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/uqHSqk3Cut0gtdEB8) | 1000 | 289.316s | 276.4MiB | $0.035541 | $0.4500 |

Cases run sequentially at 1024 MiB / 900 seconds, charge caps USD 0.25 for new cases. Prior 1,000 was explicitly authorized at USD 1. No schedules or recurring tests created. Stored event counts preparation 1 / report N. Owner tests do not establish paid revenue. Native cost excludes later reads/retention; contribution model is 80% event revenue minus measured platform costs. Missing player versions remain null.

## Competitive monetization

Effective price remains USD 0.0004 / full written report ($0.40/1000) plus USD 0.05 once / export, normal run usage included. 1,000 total USD 0.45; 100 total USD 0.09; 10 total USD 0.054. Saved schedule, new native runs and public pricing page agree. No extra charge for CSV/Excel files, source duplicates or rejected rows. No tier discount layer needed at this low flat rate.

Refreshed closest Store APIs on 16 November: maximedupre/protondb has 1 monthly user and $0.45/1000game summaries. jungle_synthesizer/protondb-steamdeck-linux-compatibility-scraper has 0 monthly users; advertised primary rate $0.50/ 1,000 Free/Bronze, $0.45 Silver, $0.40 Gold+ plus advertised $0.0001 start event if emitted. Competitor runtime/bills were not purchased or verified. Game summaries are a different unit from full individual notes/configurations. Our per-report rate is low and the fixed preparation covers a complete archive scan; lowering preparation to $0.04 would have reduced the slower verified 10-row case's modeled margin to 30.3%, below the 35% target. Keep current pricing.

## Brave Console upload and actual visual checks

Opened authenticated Brave, Publishing → Display information → Upload image. Explicitly selected the correct 512 px project assets/icon.png; previewed full purple report/checkmark; Looks good; saved. Native public API now returns a non-null uploaded S3 picture URL and its PNG GET returns 200. Console run header visibly shows the custom logo. Added the previously empty public short description from the existing project scope; title/slug/SEO/pricing/status/permissions preserved.

Uploaded asset: https://apify-image-uploads-prod.s3.us-east-1.amazonaws.com/qUOjbhgHPenc6biI9-actor-5MfSH4T9Sv9Hnca02-WfbNcKLp2o-icon.png

Public Store image status at verification: **public page still renders the default thumbnail; propagation/rendering remains unverified**. No new manual upload is needed. A normal canonical-host alias was rejected by the ActorAPI; the valid native upload URL was preserved. Do not claim the public header rendered if it still uses actor_picture.svg. Recheck platform rendering, and prepare a support packet for the owner if it persists; do not contact others without authorization.

Brave visual inspection now resolves the earlier screenshot gap: default table is readable, meaningful headings/date formats/source links; ellipses expand longer values. All source fields view shows original notes object/grouping fields. Selected Excel workbook — full player text; actual save dialog opened; downloaded ProtonDB-Final-Test-2026-11-16.xlsx and independently verified all 19 fields across 10 rows on disk. Browser control later disconnected (cgWindowNotFound); no visual success after that is invented.

Public README and source cadence/limitations/pricing remain accurate. First official TEST-origin QA visibility: 0 runs found across full visible history; owner tests are separate and are not labeled official QA PASS. No additional runtime defect was found.
