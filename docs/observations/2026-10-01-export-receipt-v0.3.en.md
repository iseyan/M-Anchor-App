# v0.3 observation JSON receipt and review

[日本語](2026-10-01-export-receipt-v0.3.ja.md)

Received: October 1, 2026, 00:21 (Japan time). Material: synthetic demo observations exported by M-Anchor App v0.3.

English translation of the [original Japanese receipt](2026-10-01-export-receipt-v0.3.ja.md).

## Source

- [Received JSON](records/m-anchor-app-record-2026-09-30T15-21-20-696Z.json)
- [Machine consistency check](2026-10-01-export-check.json)
- Exported: October 1, 2026, 00:21:20 Japan time; timestamps inside JSON use UTC.
- File SHA256: `c9e660b47877436077f134fbf6fe38a61d49e82630854a12da309686ebd26ab8`

Original bytes were retained. The content concerns two synthetic cases. No connection-key fields or API-key patterns were detected.

## Results

| Entry | Decision | Before/after check |
| --- | --- | --- |
| 1: DEMO-HOLD | No change / no_state_change | h_A and h_B, unresolved, Version 1; full state identical |
| 2: DEMO-UPDATE | Saved / accepted | Uses e_B; changes h_A and h_B to h_B, unresolved to resolved, Version 1 to 2 |
| 3: DEMO-HOLD | Rejected / invalid_transition | Rejects unsupported removal of h_A; full state identical |

Exported current records matched the after-state of each case's latest history entry. Recomputed state_hash values matched for current records and every before/after state. No-change and rejection preserved full state, including version and hash.

The latest execution records `source: fixed_demo`. SHA256 recomputed from its UTF-8 proposal text matched the latest decision and entry 3's `raw_sha256`. The latest decision included `readback_verified: true` and `state_changed: false`.

This confirmed JSON export and its internal consistency in addition to the earlier screen-history report.

## Limits

Review covered correspondence among states, proposals, and history within the supplied JSON. It was not a direct connection to the user's database or signed proof of authenticity.

Full proposals, model IDs, response IDs, and usage for entries 1 and 2 are absent. Their description as live-model runs is based on the earlier guided operation order. This is distinguished from the recorded source of the latest fixed demo; the JSON alone does not establish model metadata for those two entries.

Automatic connection, full-page rendering, and persistence after restart are outside this review. No additional model API call or write to the user's store was performed.
