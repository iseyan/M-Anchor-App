# v0.3 user operation check

[日本語](2026-10-01-user-check-v0.3.ja.md)

Received: October 1, 2026, 00:18 (Japan time). Material: the on-screen update history supplied by the user, separate from development-environment automated tests.

English translation of the [original Japanese observation](2026-10-01-user-check-v0.3.ja.md).

## Guided procedure

1. Through the live model, request unsupported resolution of DEMO-HOLD.
2. Through the live model, request an update of DEMO-UPDATE using admitted evidence e_B.
3. Without the API, submit the unsupported DEMO-HOLD proposal using the fixed demo.

## Received history

The displayed order and values are retained; column headings and result labels are translated.

| ID | Case | Result | Reason code |
| --- | --- | --- | --- |
| 3 | DEMO-HOLD | Rejected | invalid_transition |
| 2 | DEMO-UPDATE | Saved | accepted |
| 1 | DEMO-HOLD | No change | no_state_change |

## Supported observations

The history showed the three expected results: No change, Saved, and Rejected. This supplied a user-side report of the basic paths for handling an unchanged proposal, saving a valid update, and rejecting a nonconforming update.

The material is a history table. It does not include raw proposals, model metadata, full before/after states, hashes, or readback JSON. Mapping the rows to live-model and fixed-demo routes relies on the guided operation order; the table columns alone do not establish the source.

This table alone does not verify automatic connection, JSON download, persistence after restart, or full-page rendering.

## Development record

Added as a user-side basic-operation report for v0.3. Release-time validation and raw automated logs are retained. No code change or additional model API call was made in this review.

Follow-up: [JSON was received and checked](2026-10-01-export-receipt-v0.3.en.md) at 00:21 the same day. The account of what was known when this table arrived remains as recorded above.
