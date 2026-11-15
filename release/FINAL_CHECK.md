# Final SEO, input, output and stress review —15 November2026

Actor https://apify.com/thescrapelab/protondb-player-reports, ID5MfSH4T9Sv9Hnca02. User authorized final review and stress test; existing full build/deploy authority retained.

## Review findings

- Live SEO title: ProtonDB Player Reports Scraper | Linux & Steam Deck. Search description accurately lists written reports, game IDs, verdicts and supplied hardware/software; correct canonical URL. Earlier Manager SEO97/100, sole suggestion troubleshooting. New README uses a natural scraper heading and includes actionable troubleshooting; no ranking claims.
- Two visible/total inputs, zero required: maximum written reports (default10, cap1000), optional game/hardware filter with examples. No new technical controls.
- Native default dataset schema has reports first, table component, readable headings, date formatting and link formatting; all-fields view available. Raw21fields preserved, default flat export19fields includes IDs, full combined notes and all rights/provenance fields. Public Store/logo markup works. Browser host unavailable/Chrome profile busy: authenticated Console pixel-level visual inspection remains UNVERIFIED.

## Actual final stress regression

Production0.1.12 runXgcy6pRKlTRlpjwu2 succeeded with1000unique valid records in290.759s, peak276049920bytes. Native reportevents1000/preparation1. JSON/CSV full notes matched1000/1000. Deep native XLSX comparison found997/1000 exact notes:3rows lost non-BMP characters such as thumbs-up and joystick emojis. This is a native exporter issue, not corruption of the stored report data. Prior checks of workbook row counts did not establish text fidelity; that gap is now tested explicitly. Native regression receipt preserved separately.

## Implemented and verified fix

Candidate0.1.13/uNsEXkPyH4WB8ULI9, commitbbb29b0. Plain Node24 generates UTF8 BOM CSV and compressed OOXML inline-string workbook, using only standard libraries. Store REPORTS.csv and REPORTS.xlsx in the run's native KVS. The workbook has frozen header, autofilter and wrapped notes; text IDs and formula-like player text stay strings. No added dependency, input, data field, billing event or price change.

Output CSV/Excel properties now target actual file records, rather than dataset URLs that Console treats as table outputs; all-fields output explicitly selects view=allFields. Dataset API remains intact. Public Console source and official output-schema documentation establish link behavior; no visual UI success is invented.

12automated tests/CI pass. Local independent openpyxl reader verified all1000source notes, including affected emojis, IDs, filters and frozen header. New sequential cloud10/100/1000 file tests passed, each capped0.25/0.25/1USD, memory1024MiB, timeout900s. Prior native total remains well below originalUSD10; no new recurring jobs.

Old-build FEATURE_CLAIMS failure is resolved by the verified0.1.13 release; reviewed current-build source/quality evidence is saved. Generic Apify dataset Excel export remains outside Actor control; README directs customers to supplied workbook. JSON/CSV remain lossless. Separate avatar upload still depends on Console UI access (TASK1054).

## Final deployed evidence

Production default **0.1.13 / uNsEXkPyH4WB8ULI9**, source commitbbb29b0. StoreHTTP200 verifies revised README/troubleshooting and unchanged$0.40/1000report rate plus$0.05preparation; ordinary platform usage remains included. Native output mappings point CSV/Excel to actual file records with correct MIME types and the all-fields table to view=allFields.

| Test | Unique valid reports | CSV/Excel exact notes | Runtime | Peak RAM | Native platform cost | Customer fee | Modeled contribution margin |
|---|---:|---:|---:|---:|---:|---:|---:|
| [unicode-default](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/97RURZ0YSTADlKWfF) | 10 | 10/10 | 255.706s | 268.7MiB | $0.021858 | $0.0540 | 39.5% |
| [unicode-game](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/XdZ6OTsdpWn4ickfP) | 100 | 100/100 | 199.660s | 234.7MiB | $0.018079 | $0.0900 | 59.9% |
| [unicode-large](https://console.apify.com/actors/5MfSH4T9Sv9Hnca02/runs/uqHSqk3Cut0gtdEB8) | 1000 | 1000/1000 | 289.316s | 276.4MiB | $0.035541 | $0.4500 | 72.1% |

Final broad run has1000/1000structurally valid and independently source-matched records, zero duplicate IDs and complete essential fields. All1000CSV and supplied-workbook notes/IDs/dates match the dataset, including3notes containing supplementary Unicode. Notes range20–2138characters. All1000have supplied GPU, OS and driver;241have a supplied Proton version, with missing versions left honest. Native generic dataset XLSX remains a platform limitation: use the supplied workbook.

Total native run/build usage across this Actor at verification is$0.690941, well below the original$10mission cap. Owner test counters are not independent customer revenue; contribution models use80%event revenue minus conservative measured platform costs, excluding support, tax, fixed plans and later storage reads/retention. No proxy/paid external API.

SEO/readme: clear source/search terms, accurate meta title/description/canonical, use cases, working input/API examples, actual output example, field meanings, price/cadence/limits, FAQ and troubleshooting. No remaining material SEO or input defect found. No further runtime change is justified by these tests. Optional future work is performance improvement only if paid demand supports it.

Native view configuration, data and file links verified; authenticated Console screenshot/pixel-level inspection remainsUNVERIFIED because browser controls are unavailable. Avatar upload remains the existing separate TASK1054 dependency. Official daily TEST-origin QA is distinct from these owner runs.

Fresh Manager audit: `reports/2026-11-15T18-34-43Z`, publication-readiness READY with no blockers; SEO/Store-readiness100/100. The display configuration matches [Apify dataset-schema semantics](https://docs.apify.com/storage/dataset-schema), and file/dataset output targets follow [the output-schema specification](https://docs.apify.com/actors/development/actor-definition/output-schema). This is configuration/content verification, not a browser screenshot or an SEO ranking guarantee.
