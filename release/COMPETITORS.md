# Current competitor pricing — 15 November 2026

Game summaries and ordinary Steam reviews are adjacent products, not equivalent full player compatibility reports.

| Actor | Monthly users | Effective event prices | Reviews |
|---|---:|---|---:|
| https://apify.com/memo23/steam-reviews-scraper | 28 | apify-actor-start: 0.005; review: 0.001 | 0 |
| https://apify.com/maximedupre/steam-reviews | 1 | steam-review-extracted: {'FREE': {'tieredEventPriceUsd': 0.0005}, 'GOLD': {'tieredEventPriceUsd': 0.00025}, 'BRONZE': {'tieredEventPriceUsd': 0.00045}, 'SILVER': {'tieredEventPriceUsd': 0.00035}, 'DIAMOND': {'tieredEventPriceUsd': 0.00025}, 'PLATINUM': {'tieredEventPriceUsd': 0.00025}} | 0 |
| https://apify.com/maximedupre/protondb | 1 | steam-game-compatibility-result: 0.00045 | 0 |
| https://apify.com/jungle_synthesizer/protondb-steamdeck-linux-compatibility-scraper | 0 | apify-actor-start: 0.1; data-record: 0.0005 | 1 |
| https://apify.com/thescrapelab/steam-review-changes-tracker | 1 | apify-actor-start: 0.003; apify-default-dataset-item: 0.0005 | 0 |

Prices are the effective schedules captured from live Apify API reads. Future schedules excluded. The active report event is USD0.40/1000 plus USD0.05 once-per-export preparation after the owner-requested pricing update. Advantages: recent full written notes, supplied GPU/OS/driver/Proton fields, source attribution, content-based identity. Limitations: periodic snapshot, missing versions, no author identity or real-time updates. Customer platform usage is included in this Actor fee. Competitor usage pass-through must be checked against each pricing record; unknown values are not assumed zero.

Store descriptions checked on the same date; API counts above are current API observations, while cached public-page counts can lag.

| Actor | Features / unit | API modified date | Evidence limits |
|---|---|---|---|
| memo23/steam-reviews-scraper | Steam review text, authors, exact date windows; language and recommendation filters | 2026-11-13 | Adjacent Steam reviews, no structured ProtonDB configuration reports; no customer reviews visible |
| maximedupre/steam-reviews | App ID/URL/name, language, recommendation, dates, reviewer context | 2026-09-16 | Adjacent review product; no customer reviews visible |
| maximedupre/protondb | App-ID list; current/best/trending compatibility tier, score/confidence/report count | 2026-08-13 | A row is a game summary; no full individual notes/configurations advertised; no customer reviews visible |
| jungle_synthesizer/protondb-steamdeck-linux-compatibility-scraper | App-ID list/default popular games; aggregate tiers, score and report count | 2026-11-13 | One 5-star review, no verified recurring complaint; aggregate data, not individual reports |
| thescrapelab/steam-review-changes-tracker | Current Steam reviews and observed before/after changes | 2026-11-03 | Existing own adjacent Actor; change tracking is not author-level tracking of ProtonDB submissions |

Public success counters are operational signals, not extraction-quality proof. These competitors were not run or charged during this comparison. Unverified customer-specific platform fees and review text are not invented. The new product differentiates on individual written compatibility notes and supplied hardware/software, rather than claiming better real-time aggregate ratings. Our cold archive scan is slower than a game-summary lookup and the source is freely downloadable; the preparation fee pays for this fixed scan cost.

## Owner-requested pricing polish — 15 November 2026

The active written-report price is reduced20%, from$0.50 to$0.40/1000, while preparation remains$0.05/export. Total customer cost:10reports$0.054;100reports$0.09;1000reports$0.45, with standard platform usage included. The per-report rate is below the closest$0.45/1000 game-summary Actor and the adjacent$0.50/1000 summary Actor, although those units are not equivalent to individual player reports. It remains above the$0.25 lowest plan-tier ordinary Steam review offer because source scans have fixed costs.

At measured earlier-build1000cost$0.036833, modeled contribution is0.8*$0.45-$0.036833=$0.323167, or71.8% of gross. At measured production10cost$0.020541, contribution is$0.022659, or42.0% of$0.054 gross. No bulk-discount layer is necessary at this low flat rate. New-build export tests and native lower-price events are recorded separately. These are contribution models, not independent buyer revenue.
