# Development log

## October 1: publication preparation for Zenodo

Prepared English-first publication materials describing the app as a deterministic gate for containing prompt-induced unauthorized record updates. Added a technical note in both languages, six-scenario reproduction instructions, a record-to-claim table, copy-ready Zenodo description, upload guidance, and `CITATION.cff` using the existing Ise/iseyan author spelling. Four fixed attack types and three model-route observations remain explicitly distinct. The app, gate, model instructions, and original evidence bytes are unchanged. The app is still 1.0.0; source commit and package hash distinguish this documentation snapshot. No Zenodo record, DOI, license grant, or release tag was created. Owner selection of distribution terms remains before final publication.

[English](development-log.en.md) | [日本語](development-log.ja.md)

This log explains the app's purpose, decisions, changes, and observations for third-party readers. It is separate from the existing formal research evaluation. Dates below follow Japan time where specified in the original records.

## September 30, 2026: a small distribution

The scope was narrowed to one dedicated Python client and one protected operation: updating a case record. The model proposes; the external gate and store decide whether to commit. No UI approval bypasses the rules.

The original name was Anchor Control. After basic checks, the project became M-Anchor App in `iseyan/M-Anchor-App`. The original Japanese [planning memo](../plans/m-anchor-app-plan-2026-09-30.ja.md) remains a dated record; the [evidence guide](evidence-guide.md) explains it in both languages.

## v0.1 and v0.2: observations

| Observation | Material | Supported conclusion |
| --- | --- | --- |
| Unsupported fixed proposal rejected | JSON with before/after, reject, invalid_transition, readback_verified | This proposal left the authoritative state intact |
| Supported fixed update saved | JSON with commit, h_B, Version 1→2, readback | The admitted-evidence update was committed |
| DEMO-HOLD via real model yielded no change | Model ID/usage and unchanged before/after JSON | The model/gate path preserved uncertainty in this run |
| DEMO-UPDATE displayed h_B and Version 2 after model operation | User-provided case table | The visible outcome matched the intended update; the table was not a full execution log |

The supplied model log named `gpt-5.4-mini-2026-03-17`. These examples do not establish general attack rates or guarantees for arbitrary inputs.

Observed usability problems included finding keys, connection failures before server startup, selecting the wrong target, and understanding no-change results on already updated cases.

## v0.3: operation and explanation

The launcher waits for server readiness and connects through a one-use ticket. Cases start unselected; the run button names the target. The UI displays before/after state and separates Saved, Rejected, and No change. Fresh demos use separate data, and JSON exports/documentation support external explanations.

Gate, formal core, model bridge, and client bytes remained unchanged from v0.2. One of 25 development tests initially failed because the export transaction conflicted with the gate transaction. Export was corrected to read a consistent in-memory SQLite backup without changing the gate; all 25 passed. UI logic also passed using a DOM substitute and real HTTP, not browser rendering. See the original [v0.3 validation](validation-v0.3.ja.md).

## October 1: v0.3 user records

The user reported three history entries: HOLD/no change, UPDATE/saved, HOLD/rejected. The table matched expected outcomes but did not itself establish model provenance, full proposals, or readback. A separate receipt preserves that distinction.

A v0.3 JSON export at 00:21 Japan time then supported state/hash consistency, preserved state for no-change/rejection, the admitted Version 1→2 update, and the latest fixed proposal's correspondence to history #3. It did not contain model metadata for entries #1–2. See the [evidence guide](evidence-guide.md) and linked originals.

## v0.4: persistent execution records

The received v0.3 export retained only the latest page execution metadata. v0.4 addressed that gap by committing state, decision/raw bytes, and execution metadata together. Readback remains a separate later observation; interruption is not counted as verified.

Routes are derived from server processing, not caller claims. One-use internal tickets bind model metadata to target case and exact proposal bytes. Ordinary client API records do not identify the proposal's author as AI or human.

Old history is preserved without inventing missing dates/model IDs. History IDs distinguish repeated identical proposals. The UI shows 100 entries; exports include all. Details reopen past proposals, states, decisions, and available model metadata.

All 34 application tests and UI logic passed locally. Tests covered restart, migration, rollback on SQL failure, and 103-entry exports. Models were mocked; no paid API was used. See the original [v0.4 validation](validation-v0.4.ja.md).

## v0.4: received demo exports

The 00:54:38 Japan-time export included three fixed runs: Rejected → Saved → No change. Fifteen consistency checks matched proposal text/Base64/SHA256, state hashes, chronology, and final records. This established fixed-demo execution and JSON export on the user's side, not a restart or a real-model run.

A second export at 01:07 used a different data-folder label and reproduced the same three decisions and final state. Fourteen checks passed. It was a separate fresh demonstration, not proof of retaining the previous store through restart. Original bytes, checks, and the Japanese receipt remain linked in the [evidence guide](evidence-guide.md).

## v0.5: automated verification and distribution

GitHub Actions verifies Linux/Python 3.10 and 3.13 and Windows/Python 3.13 with Node.js 24. Failed verification blocks packaging while retaining logs. No model API keys are needed. Source checksums and every ZIP entry are verified; data and credential files are excluded.

The first Actions run passed all three environments and packaging for commit `6a986b396fd1cba895e959ddc9982db9054b379b`. A follow-up documentation commit passed again. See [v0.5 validation](validation-v0.5.en.md). This added development automation, not AWS deployment or public gate access.

## v0.5.1: English-first bilingual presentation

The user requested English as the primary language with Japanese alongside it, including the app. Static headings, dynamic decisions/errors/history, and editable demo requests now follow that order. English documents are paired with Japanese documents; README and changelog present both languages.

Stored proposals, reason codes, JSON schema, and historical observation bytes remain unchanged. Earlier Japanese records are retained with an English/bilingual evidence guide. The language change does not alter evidence admission or commit authority. See [current validation](validation-v0.5.1.md).

The v0.5.1 code passed all three hosted verification environments and the packaging job in [Actions run #3](https://github.com/iseyan/M-Anchor-App/actions/runs/36746901627). The bilingual validation record links the API receipt and local logs.

## October 1: V1 record-protection workflow

The user requested a prompt-attack protection app and authorized V1 implementation. This release keeps the protected object to local case records. It adds four synthetic attacks, two controls, and explicit separation of fixed-proposal execution from model-input execution.

The missing link in prior explanation records was the input that produced a proposal. V1 stores that exact text and SHA256 with optional exercise metadata, using the existing one-use ticket and atomic state/audit/execution transaction. The UI and documentation disclose the changed retention behavior. Older inputs are not reconstructed.

The screen shows input, proposal, gate decision, and independent readback. A transport or generation failure is left unverified, not scored as a blocked attack. No attack classifier or universal jailbreak claim is added. Gate rules, formal core, provider request implementation, and client bytes are retained from v0.5.1. See [V1 guide](v1-guide.md) and [validation](validation-v1.md).

V1 passed Linux/Python 3.10 and 3.13, Windows/Python 3.13, and packaging in [Actions run #5](https://github.com/iseyan/M-Anchor-App/actions/runs/36791415008). Each verification environment passed 40 application tests, 3 packaging tests, UI logic, and source checksums. The [validation record](validation-v1.md) links the original API receipt and local logs.

## Remaining work

- Simplify the two fixed-execution controls; guided user operation exposed repeated legacy-demo runs when a scenario run was intended.
- Check CI and packaging results for each new change.
- Specify one business record, its evidence authority, and valid/invalid update examples.
- Decide licensing and executable distribution.
- Select cloud operation only after defining the integration and run frequency.

Future entries should state what changed, why, the verification environment and method, and remaining uncertainty.

## October 1: V1 user export through 10:01 Japan time

Received 20 cumulative records: 14 legacy fixed-demo runs, four fixed scenarios, and two model API runs. The fixed runs cover unsupported candidate removal, forged evidence admission, authority escalation, reference-hash tampering, unchanged state, and a valid evidence-based update. Source bytes and an English-first bilingual [observation](observations/2026-10-01-user-check-v1.md) are retained.

The model preserved HOLD's unresolved candidates in #19. UPDATE was already Version 2 before model run #20, so no change was appropriate. Neither is a gate rejection of an invalid model output or a new model-generated commit. The latter positive-control observation remains pending; only one fresh UPDATE run is needed. All 20 raw-proposal/state hashes, recorded readbacks and history continuity matched. Both model input hashes matched. No application code or research-stage status was changed.

## October 1: positive control received at 10:22 Japan time

A separate one-entry export records model `gpt-5.4-mini-2026-03-17` proposing the admitted e_B update, which the gate saved as h_B / resolved / Version 2 from Version 1. Input and proposal hashes, before/after states, exported records, and matched readback agree. This completes the positive-control observation left pending above and the planned basic checks for these examples. Both original exports are linked in the [observation](observations/2026-10-01-user-check-v1.md). Their common `data` label does not establish folder identity or how the Version 1 state was initialized. App code is unchanged; no new API call was made during review.
