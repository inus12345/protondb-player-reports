# ProtonDB Player Reports — release in progress

Actor: https://console.apify.com/actors/5MfSH4T9Sv9Hnca02 . Source: https://github.com/inus12345/protondb-player-reports . PRIVATE; not ready for publication while stress, native billing, recovery and final verification remain incomplete.

Implementation: Node24, first-party HTTPS archive download/integrity check, bounded newest-first temporary SQLite selection, content-hash identities, original player notes and supplied hardware/software values, collectedAt, native run manifest and deterministic charge-batch keys. Eight unit tests passed. Two optional inputs, no proxies or paid third-party APIs.

Optimized cloud10 run:10unique valid rows,181.371seconds,291061760peakRAMbytes,0.014733589USD snapshot usage. Earlier unbounded implementation reached approximately1GB; replaced with bounded selection.

Saved private PPE pricing: USD0.05/start perGB minimumone, USD0.0005/fullwrittenreport; platformusage included; no tier discounts. Not claimed billing-verified or production-ready.

| Test | Run ID | Status | Seconds | Usage USD |
|---|---|---|---:|---:|
| normal-run | Z1BpvCgisAjhZszTb | READY | pending | 5e-05 |
| optimized-small-run | bVHUtklBlpgyABQuc | SUCCEEDED | 181.371 | 0.014733589115242161 |
| small-run | MCxd4kuxInfzv8ZIz | SUCCEEDED | 260.891 | 0.02209032901881139 |
| current-small-run | 7Fgdg1rwBuACalqJa | RUNNING | 226.81 | 0.016478579638034105 |

Combined native test/build budget: below USD10. Future10k case uses measured projection. No public listing until release gates pass. Source-use notices and public collector code provide attribution and alteration method; archive provenance remains the maintainer periodic dump.
