# ProtonDB Player Reports

Export complete player-written Linux and Steam Deck compatibility reports from the latest public download published by ProtonDB's maintainer. Compare reports for the same Steam game across supplied GPUs, operating systems, drivers and Proton versions.

The maintainer generally publishes monthly snapshots, with irregular release dates. This export uses the latest available snapshot; it is not a live report feed. Reports are sorted newest first. The snapshot's filename date is a label, not a guaranteed collection cutoff; inspect each report's date.

## Quick start

Start with `{}` for ten recent written reports across games, or use:

```json
{"filter":"game:292030","maxResults":100}
```

Use `hardware:NVIDIA` instead to match public GPU, OS or driver text. There is one optional filter and one result limit. Download the dataset as JSON or CSV from Apify Console.

Each row contains the Steam app ID and title, report date, original verdict, full notes, supplied GPU/OS/driver, supplied Proton version or variant, source and archive URLs, snapshot date and license information. A `recordId` identifies the exact source record content. It is not an author identifier. Different notes with the same game/date/hardware remain separate.

## Limits

Written reports must contain at least 20 non-whitespace-trimmed characters and four words, plus identity/verdict and available hardware or software information. Missing values remain null. A reported version string is user-supplied and has not been validated against an installed build. `Default`, `official` and similar labels never establish an exact version. SteamOS text does not prove a particular handheld model. Player experiences are not controlled benchmarks.

Results cover the latest archive, not every report on the live site. Older schema generations may be absent from that archive. A cold run downloads and indexes the complete archive before selecting the newest rows. Fewer rows are returned when the source has fewer matching usable reports. Empty matches return an empty dataset.

Export retries reconcile existing rows in the same run. A fresh run is a new export and may return the same records. Content changes create new content IDs; this product does not promise author-level edit tracking. Interrupted runs retain their selected snapshot and delivery ledger. If a dataset write has an uncertain outcome, the run fails rather than blindly repeating the write; resume reconciles existing output before continuing.

## Attribution and licensing

Contains information from ProtonDB contributors, exported by [bdefore](https://github.com/bdefore/protondb-data), under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/); individual contents are under [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1-0/). TheScrapeLab normalizes fields, selects written reports, sorts by date and removes exact duplicates. Preserve these notices and source links with exports. Derivative database reuse remains subject to the applicable share-alike and access obligations. A public release must offer the qualifying derivative data or alteration material under ODbL section 4.6. This is independent of ProtonDB and Valve.

## Pricing

The preparation charge is **$0.05 per run per GB of allocated memory, with a minimum of one unit**. The normal 1 GB configuration therefore starts at $0.05. Each full written report delivered costs **$0.0005 ($0.50 per 1,000 reports)**. Platform compute, transfer and ordinary run storage are included. No tier discounts apply.

Examples at 1 GB: ten reports cost $0.055; 100 cost $0.10; 1,000 cost $0.55. The preparation charge applies even if no reports match or collection fails after starting. Rejected records, suppressed duplicates and same-run delivery retries do not incur additional report charges. A fresh run is a separate export. User-initiated storage reads/retention after a run can generate normal account storage costs.

## Python API example

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thescrapelab/protondb-player-reports").call(run_input={"filter": "game:292030", "maxResults": 100})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row["gameTitle"], row["gpu"], row["noteText"])
```

Public transformation source and data-license notices: https://github.com/inus12345/protondb-player-reports . The collection timestamp is `collectedAt` in UTC; `date` is the player report date.
