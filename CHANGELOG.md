# Changelog

[日本語](CHANGELOG.ja.md)

## 1.3.0 release candidate: results of Experiment 4 (robustness benchmark) — 2026-11-23 (Japan time)

- "Read the benchmark" now shows the results of Experiment 4. Passing the cause on as confirmed, approved payments that did not go through, and joint success sit in one table, as counts over planned trials (A ordinary caution, M M-Anchor, G Prompt Guard 2).
- Joint success is shown as defined in advance (99/300 → 142/300). The post-hoc count that also accepts "refuted" (155/300 → 161/300) is a note, not a table row.
- E7 (a signed report is present but does not support the cause for this request) is shown next to the overall table: passed on as confirmed 14/60 → 12/60, joint success 12/60 → 3/60.
- Column G carries a footnote: none of the 140 untrusted documents was detected, so G shares the responses and results of A.
- The review status is displayed: "Recount and cross-check by Claude are complete. Human review has not been done."
- The bundled verification script gains `--exp4-run`, which recounts every row on the screen from the trial records.
- This is a separate candidate from the accepted 1.2.0 candidate (ZIP `3ad39103…`). Record replay (Case A, its control, Case B) is unchanged.

## 1.2.0 release candidate: case selector and side-by-side comparison — 2026-11-22 (Japan time)

- Workflow demo: add a case selector and a side-by-side comparison of two records of the same case. Difference marks follow mapped states and payment content, not wording or order.
- The second card is now "How was the cause handed off?" and shows the state expected for the case next to the state the handoff states.
- Add a "Read the benchmark" view. Until the run is complete it shows "not run yet" and no numbers.
- Case A (pilot, `gpt-oss:20b`) is included. Its two records, ordinary caution and the M-Anchor method, open side by side. Replayed through this app's gate and simulated ledger, the payment is applied once in both conditions, and the cause is handed off as "confirmed" and "unconfirmed". It is a development example with one run per condition and is not counted in any benchmark. The receiver was not measured.
- A control for Case A (a signed investigation report exists) is added. The expected state is "confirmed", and both conditions handed it off as confirmed. The Experiment 3 joint measure is not computed for this case.
- The pilot output has two fields (payment proposal, cause state). The replayed input is converted from it, and amount, payee and IDs are demo values. The original output stays on the screen and in the record.
- Results and hashes of the four Case B records are unchanged from the 1.1.0 candidate. The 1.1.0 candidate was not released.

## 1.1.0 release candidate: workflow demo — 2026-11-22 (Japan time)

- Add a screen (`/workflow`) that judges an unresolved cause and an authorized payment separately. Two views: "Replay a record" and "Read the experiment results".
- Replay: four submissions for case `F-LT6-01`, repetition 1, copied from the frozen Experiment 3 records of M-Anchor-challenge. Assessment, proposal, gate decision, ledger and handoff are shown side by side, with three results from the same record: was the correct payment applied, did the handoff keep the cause unresolved, was any proposal denied. The receiver's decision is shown in its own box.
- Frozen records, the field display example, and simulated runs of edited input are told apart on screen and in the saved record. The two-choice versus three-value comparison is a display example and changes neither the record, the results nor the hash.
- Results: frozen aggregates of Experiment 2 (C3/C4) and Experiment 3 (C4/C4P), bundled as fixed values with source commits and SHA-256. `scripts/verify_workflow_results.py` recomputes them from episode data and compares.
- `start.cmd` and `start-fresh-demo.cmd` first check whether `py -3` gives Python 3.10 or later, then fall back to `python`; if neither is available they print the required version.
- The screen uses no key, calls no model, and does not read or write the authoritative store. Existing gate rules, storage format and integration interface are unchanged.
- See the [workflow demo guide](docs/workflow-demo.en.md).

## Documentation language editions — 2026-10-01 (Japan time)

- Separate non-app documentation into English and Japanese files, with language-specific navigation. Add English translations of historical Japanese plans and review notes.
- Supply the technical briefing as separate English and Japanese PDFs. Keep the bilingual app interface, model instructions, raw evidence, and standard license text unchanged. App version remains 1.0.0.

## V1 licensing and publication update — 2026-10-01 (Japan time)

- License this distribution under Apache-2.0, permitting commercial use, modification, and redistribution under its terms. Add LICENSE and NOTICE; align citation and publication materials.
- Keep application code and original observations unchanged. App version remains 1.0.0; source commit and archive hash identify the licensed distribution.

## V1 / 1.0.0 — 2026-10-01 (Japan time)

- Add four synthetic attack scenarios and two valid controls, with fixed-proposal and model-input execution paths.
- Display input, proposal, gate decision, and verified stored state together.
- Persist exact model input and SHA256 as optional execution.exercise metadata, bound to the proposal through the one-use ticket.
- Add admin-only scenario catalog/run routes. API failures before proposal submission remain errors, not gate rejections.
- Keep gate rules, formal core, provider request, and client behavior; retain old history without inventing input metadata.
- Add V1 demonstration and validation records in English and Japanese.

## v0.5.1 — 2026-10-01 (Japan time)

- Present app headings, decisions, history, errors, and editable example requests in English first, followed by Japanese.
- Add paired English documentation and a bilingual guide to original historical evidence.
- Update existing UI checks to exercise both languages; show a bilingual error for invalid manual JSON.
- Keep gate rules, stored proposal bytes, API field names, and observation schema unchanged.

## v0.5 — 2026-10-01(Japan time)

- Added GitHub Actions verification on Linux/Python 3.10 and 3.13 and Windows/Python 3.13.
- Run app tests, UI logic, packaging tests, and source checksums.
- Package successful push/manual runs after all environments pass; verify pull requests without packaging.
- Retain logs, verification JSON, ZIP, SHA256, and build records with source commits as artifacts.
- Check every ZIP entry and reject altered inputs or unsafe packaging paths.
- Preserve repository file bytes across Windows and Linux.
- Update the displayed app version to 0.5; retain v0.4 gate rules and record format.

## v0.4 — 2026-10-01(Japan time)

- Persist route, server receipt time, app version, and model metadata with each decision.
- Bind model metadata to the case and proposal SHA256 using an internal single-use ticket.
- Use distinct admin routes for fixed demos and manual submissions; all routes use the same gate.
- Add past-entry details, persisted readback observations, and complete JSON export (schema v2).
- Distinguish repeated proposals by audit_id and export raw bytes in Base64.
- Preserve old history and use null for metadata that was never recorded.
- Pass 34 tests and UI logic; record plans for later GitHub Actions and AWS work.

## v0.3 — 2026-09-30

### Operation

- Use M-Anchor App consistently as the interface name.
- Add a launcher that opens the browser after checking server readiness.
- Add automatic connection with a single-use launch ticket.
- Start with no case selected and show the target on the run button.
- Show Saved, Rejected, No change, and before/after candidates, status, and version.
- Submit fixed demos in one click without a model API.
- Start fresh demos without deleting previous data.

### Records and explanation

- Export records, evidence settings, history, and the latest page execution metadata as JSON.
- Add overview, demo guide, integration/boundary documentation, and development/validation records.
- Keep gate, formal core, model bridge, and Python client byte-identical to v0.2.

## v0.2 — 2026-09-30

- Add single-request proposal generation via the OpenAI Responses API.
- Submit unmodified model output to the gate via the dedicated Python client.
- Display proposal text, gate decision, and model usage.
- Observe uncertainty retention and a supported-update outcome using a real API on the user’s Windows environment.

## v0.1 — 2026-09-30

- Connect the existing gate and formal core to a local HTTP API, SQLite store, and browser UI.
- Check unsupported-resolution rejection and admitted-evidence updates with fixed proposals.
