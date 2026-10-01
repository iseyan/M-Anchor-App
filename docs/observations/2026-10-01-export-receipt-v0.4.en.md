# v0.4 fixed demo: observation JSON receipt and review

[日本語](2026-10-01-export-receipt-v0.4.ja.md)

Received October 1, 2026 (Japan time). Target: M-Anchor App local prototype v0.4. This is a user-side operation check, separate from formal research evaluation.

English translation of the [original Japanese receipt](2026-10-01-export-receipt-v0.4.ja.md).

## Received material

- [Original JSON](records/m-anchor-app-record-2026-09-30T15-54-38-638Z.json)
- [Consistency results](2026-10-01-export-check-v0.4.json)
- Export schema: `m-anchor-app-observation/v2`
- app_version: `0.4`
- Exported: October 1, 2026, 00:54:38 Japan time
- Data label: `data`
- Original SHA256: `6da483dcd78aca642ccec25418f6bde5695016a7e0cd59a40b8b64706cd54917`

The export corresponds to the three screen-history entries previously supplied. It is separate from the v0.3 JSON reattached immediately before it; this review used the v0.4 source above.

## Observed results

| ID | Server receipt, Japan time | Case | Route | Decision | Record |
| --- | --- | --- | --- | --- | --- |
| 1 | 00:51:26 | DEMO-HOLD | Fixed demo | Rejected / invalid_transition | Retains h_A and h_B, unresolved, Version 1 |
| 2 | 00:53:27 | DEMO-UPDATE | Fixed demo | Saved / accepted | Changes to h_B, resolved, Version 1 to 2 |
| 3 | 00:53:49 | DEMO-UPDATE | Fixed demo | No change / no_state_change | Retains h_B, resolved, Version 2 |

All three execution records include route, receipt time, app version, and submitted case. Each readback is matched with an observation time. Model metadata is null, consistently with fixed demos that do not use a model.

## Consistency review

All 15 checks on the supplied JSON matched. This does not mean 15 new app runs or model tests.

- Entry order, decisions, and reasons correspond to the screen report.
- Decoded proposal Base64 matches the original UTF-8 bytes and SHA256.
- Proposal reference version/hash matches the decision's before-state.
- Rejection and no-change decisions preserve every before/after field.
- The valid update uses e_B and transitions to h_B, Version 2.
- Consecutive states connect within each case, and final records match the latest after-state.
- All state hashes recompute correctly.
- Receipt, readback, and export timestamps have a consistent order.
- The full-export declaration matches the entry count.
- Admitted evidence and interpretations match the synthetic initial configuration.
- No connection-key/API-key fields or API-key-shaped values were detected. The original contains two synthetic cases.

## Scope

The supplied observations establish the three fixed-demo outcomes and JSON export with per-run metadata on the user's v0.4 app. Matched readback is received as an app-recorded observation; the reviewer did not directly read the user's database.

The JSON contains no server stop/start events, so it alone does not verify persistence after restart. Development-side restart tests are in the [release validation record](../validation-v0.4.en.md). Full-browser rendering, opening history details, and live-model metadata retention are also outside the evidence supplied by this original.

This receipt did not change application code or the distribution ZIP.

## Follow-up: new demonstration at 01:07

A [new JSON](records/m-anchor-app-record-2026-09-30T16-07-47-577Z.json) arrived around 01:08 the same day. It was exported at 01:07:47 Japan time, with SHA256 `cf47d468693c56b6eaf747b7bb93e0cb92dcdab9546e88e26bfab96fceaf14a5`.

The data label changed from `data` to `20261001-010702-387a19`. Entries 1–3 have receipt times 01:07:21, 01:07:23, and 01:07:26. The same three proposals were newly submitted and yielded Rejected → Saved → No change.

All [14 consistency checks](2026-10-01-repeat-demo-check-v0.4.json) matched. Proposal text, state hashes, decisions, and records agreed. All three readbacks were matched, routes were fixed_demo, and model metadata was null. Excluding export time, data label, receipt times, and readback times, the entire JSON matched the earlier source.

This is an observation of the same results in a new demonstration. Its different data label and receipt times distinguish it from evidence that the previous history survived a restart.
