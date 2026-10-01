# Evidence guide

[日本語](evidence-guide.ja.md)

This index links English translations of earlier Japanese planning and observation records. The Japanese originals and raw JSON bytes are preserved. A summary does not add evidence that was absent from the source.

| Record | What it supports | Limits |
| --- | --- | --- |
| [Dated plan, 2026-09-30](../plans/m-anchor-app-plan-2026-09-30.en.md) | One Python client, case-record updates, external gate, and a small distribution. | A dated plan, not a test result. |
| [v0.3 local validation](validation-v0.3.en.md) | 25 app tests and UI logic passed on Linux/Python 3.12. | DOM substitute, not browser rendering. |
| [v0.3 user history](observations/2026-10-01-user-check-v0.3.en.md) | Reported HOLD/no change, UPDATE/saved, HOLD/rejected. | A table does not establish complete execution provenance. |
| [v0.3 export receipt](observations/2026-10-01-export-receipt-v0.3.en.md) | State hashes, retained state, a supported update, and the latest proposal matched. | Model metadata for entries 1–2 was absent. |
| [v0.4 local validation](validation-v0.4.en.md) | 34 tests: restart, migration, rollback, full export beyond 100 entries; UI logic. | Mocked models; not a paid API run. |
| [v0.4 export receipt and repeat demo](observations/2026-10-01-export-receipt-v0.4.en.md) | Fixed Rejected → Saved → No change runs, proposal/hash correspondence, readbacks, and reproduction in separate data. | Separate data is not proof of restarting the same store; no model API was used. |
| [V1 user observation](observations/2026-10-01-user-check-v1.md) | 18 fixed runs and two model-route no-change results; exact input/proposal linkage, hashes and readbacks matched. | The model kept HOLD unresolved; UPDATE was already Version 2. A new model-generated commit remains unobserved in this export. |
| [V1 model commit follow-up](observations/2026-10-01-user-check-v1.md) | A separate model-route entry saved UPDATE from Version 1 to 2, using admitted e_B, with matched readback. | Both exports say `data`; directory identity and launch/reset method are not established. |

Raw exports

- [v0.3 export](observations/records/m-anchor-app-record-2026-09-30T15-21-20-696Z.json) — SHA256 `c9e660b47877436077f134fbf6fe38a61d49e82630854a12da309686ebd26ab8`
- [v0.4 export](observations/records/m-anchor-app-record-2026-09-30T15-54-38-638Z.json) — SHA256 `6da483dcd78aca642ccec25418f6bde5695016a7e0cd59a40b8b64706cd54917`
- [v0.4 fresh-demo export](observations/records/m-anchor-app-record-2026-09-30T16-07-47-577Z.json) — SHA256 `cf47d468693c56b6eaf747b7bb93e0cb92dcdab9546e88e26bfab96fceaf14a5`
- [V1 cumulative export, 20 entries](observations/records/m-anchor-app-record-2026-10-01T01-01-50-675Z.json) — SHA256 `098377b4761f2d118e5fdb46ebd1e7550bfa15a13493c1aa706f11b13e1692d8`
- [V1 model commit export, one entry](observations/records/m-anchor-app-record-2026-10-01T01-22-01-406Z.json) — SHA256 `c3f0f0adbe7f8374c4587a47121a3ee271636f26177c87b7b10c34587a3fd3b6`

Receipt times may be expressed in Japan time; JSON timestamps use UTC. App observations do not replace formal research evaluation.
