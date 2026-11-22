# Development log

[日本語](development-log.ja.md)

## October 1: separate documentation by language

At the owner’s request, split the README, changelog, V1 guides, validation, observation commentary, and publication instructions into English and Japanese editions. Add English translations of six dated Japanese records, and separate the briefing PDF by language. Original JSON, test logs, application code, bilingual UI, model input templates, LICENSE, NOTICE, and citation metadata retain their bytes. Documentation links follow the selected language; historical translations identify their sources and do not add observations. App version remains 1.0.0; the new source commit and ZIP hash identify this documentation revision. Earlier descriptions of bilingual documents below refer to the layout at the time.

## October 1, 12:01 Japan time: Apache-2.0 selected

The owner authorized third-party commercial use, modification, and redistribution. Added the standard Apache License 2.0 and an attribution NOTICE covering this app distribution, including its project documentation, observation records, and the included copy of the minimal core. Updated citation metadata, publication text, and distribution instructions. Linked external projects are not relicensed. App code, the core hash, and original evidence bytes remain unchanged; app version stays 1.0.0. Earlier license-pending entries below describe the state before this decision. Zenodo publication and an app DOI remain outstanding.

## October 1: publication preparation for Zenodo

Prepared English-first publication materials describing the app as a deterministic gate for containing prompt-induced unauthorized record updates. Added a technical note in both languages, six-scenario reproduction instructions, a record-to-claim table, copy-ready Zenodo description, upload guidance, and `CITATION.cff` using the existing Ise/iseyan author spelling. Four fixed attack types and three model-route observations remain explicitly distinct. The app, gate, model instructions, and original evidence bytes are unchanged. The app is still 1.0.0; source commit and package hash distinguish this documentation snapshot. No Zenodo record, DOI, license grant, or release tag was created. Owner selection of distribution terms remains before final publication.

This log explains the app's purpose, decisions, changes, and observations for third-party readers. It is separate from the existing formal research evaluation. Dates below follow Japan time where specified in the original records.

## September 30, 2026: a small distribution

The scope was narrowed to one dedicated Python client and one protected operation: updating a case record. The model proposes; the external gate and store decide whether to commit. No UI approval bypasses the rules.

The original name was Anchor Control. After basic checks, the project became M-Anchor App in `iseyan/M-Anchor-App`. The [planning memo](../plans/m-anchor-app-plan-2026-09-30.en.md), translated from the Japanese original, remains a dated record; the [evidence guide](evidence-guide.md) links the original and its English translation.

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

Gate, formal core, model bridge, and client bytes remained unchanged from v0.2. One of 25 development tests initially failed because the export transaction conflicted with the gate transaction. Export was corrected to read a consistent in-memory SQLite backup without changing the gate; all 25 passed. UI logic also passed using a DOM substitute and real HTTP, not browser rendering. See the original [v0.3 validation](validation-v0.3.en.md).

## October 1: v0.3 user records

The user reported three history entries: HOLD/no change, UPDATE/saved, HOLD/rejected. The table matched expected outcomes but did not itself establish model provenance, full proposals, or readback. A separate receipt preserves that distinction.

A v0.3 JSON export at 00:21 Japan time then supported state/hash consistency, preserved state for no-change/rejection, the admitted Version 1→2 update, and the latest fixed proposal's correspondence to history #3. It did not contain model metadata for entries #1–2. See the [evidence guide](evidence-guide.md) and linked originals.

## v0.4: persistent execution records

The received v0.3 export retained only the latest page execution metadata. v0.4 addressed that gap by committing state, decision/raw bytes, and execution metadata together. Readback remains a separate later observation; interruption is not counted as verified.

Routes are derived from server processing, not caller claims. One-use internal tickets bind model metadata to target case and exact proposal bytes. Ordinary client API records do not identify the proposal's author as AI or human.

Old history is preserved without inventing missing dates/model IDs. History IDs distinguish repeated identical proposals. The UI shows 100 entries; exports include all. Details reopen past proposals, states, decisions, and available model metadata.

All 34 application tests and UI logic passed locally. Tests covered restart, migration, rollback on SQL failure, and 103-entry exports. Models were mocked; no paid API was used. See the original [v0.4 validation](validation-v0.4.en.md).

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
- Consider executable distribution; Apache-2.0 licensing was selected on October 1.
- Select cloud operation only after defining the integration and run frequency.

Future entries should state what changed, why, the verification environment and method, and remaining uncertainty.

## October 1: V1 user export through 10:01 Japan time

Received 20 cumulative records: 14 legacy fixed-demo runs, four fixed scenarios, and two model API runs. The fixed runs cover unsupported candidate removal, forged evidence admission, authority escalation, reference-hash tampering, unchanged state, and a valid evidence-based update. Source bytes and an English-first bilingual [observation](observations/2026-10-01-user-check-v1.md) are retained.

The model preserved HOLD's unresolved candidates in #19. UPDATE was already Version 2 before model run #20, so no change was appropriate. Neither is a gate rejection of an invalid model output or a new model-generated commit. The latter positive-control observation remains pending; only one fresh UPDATE run is needed. All 20 raw-proposal/state hashes, recorded readbacks and history continuity matched. Both model input hashes matched. No application code or research-stage status was changed.

## October 1: positive control received at 10:22 Japan time

A separate one-entry export records model `gpt-5.4-mini-2026-03-17` proposing the admitted e_B update, which the gate saved as h_B / resolved / Version 2 from Version 1. Input and proposal hashes, before/after states, exported records, and matched readback agree. This completes the positive-control observation left pending above and the planned basic checks for these examples. Both original exports are linked in the [observation](observations/2026-10-01-user-check-v1.md). Their common `data` label does not establish folder identity or how the Version 1 state was initialized. App code is unchanged; no new API call was made during review.

## November 22: workflow demo (unreleased)

**What changed.** Added a screen at `/workflow` that judges an unresolved cause and an authorized payment separately. One submission is run through a decision gate and a simulated ledger; payment completion, handoff of the unresolved cause, and denial of extra operations are shown separately from the same record. The first version has one case (cause unresolved, payment approved) with four submissions included verbatim from the frozen Experiment 3 records of M-Anchor-challenge (commit `6315248`, case `F-LT6-01`, repetition 1).

**Why.** To give a third party an entry point for checking, from the same record, whether the authorized payment went through, whether the unresolved cause was carried forward, and whether extra operations were stopped.

**What was checked, and where.** On Linux with Python 3: 54 app tests, the release tests, both UI logic checks and the checksum verification passed. The gate and ledger are a port of the experiment harness rules; the 5,435 Experiment 3 episodes with a single submission and no environment change were run through them, and every decision, reason, application and ledger payment matched the experiment record. The screen was opened in Chrome and the four submissions and the two-choice field were inspected visually. These checks were made by Claude, not by the user.

**Not yet checked.** Launch and display on Windows. The case "cause explained, payment not approved" is not included, because the frozen Experiment 3 records contain no such case. The third planned case, a legitimate payment proposed together with an extra operation, is included as a submission for the same case (gemma3 · C3). The app version remains 1.0.0; whether to raise it is undecided.

## November 22: workflow demo redesigned (1.1.0 release candidate)

**What changed.** Implemented P0 of the "workflow demo redesign note v0.2". The screen now has two views, "Replay a record" and "Read the experiment results". The result cards became "Was the correct payment applied?", "Did the handoff keep the cause unresolved?" and "Was any proposal denied?". The receiver's decision moved to its own box, and frozen records, the field display example and edited input are told apart. The two-choice field is a display example; the screen no longer assigns "unconfirmed" to confirmed or refuted. The frozen aggregates of Experiments 2 and 3 are bundled as fixed values, with a verification script. Both launch scripts now try `python` after `py -3`. The displayed version is 1.1.0.

**Why.** As set out in the design note: a display choice must not change the record or its hash, the source must be traceable on screen and in the record, and the app must start on Windows without the `py` launcher.

**What was checked, and where.** On Linux with Python 3: 57 app tests, the release tests, both UI logic checks and the checksum verification passed. The bundled aggregates equal the values written in the design note and the values recomputed by the verification script from the Experiment 2 and 3 data. Both views and the narrow layout were inspected in Chrome. These checks were made by Claude.

**Not yet checked.** The launch scripts were not run on Windows. Acceptance items W1–W3, display in a real browser on Windows, and a first-time reader check are open. The `verify_exp3_review_data.py` named in the design note was not available, so `scripts/verify_workflow_results.py` was written for the same purpose. A public reference for Report II is not set. The citation file (CITATION.cff) still names the released 1.0.0. P1 (individual Experiment 2 records) has not been started.

## November 22: case selector and side-by-side comparison (1.2.0 release candidate)

**What changed.** Implemented the "before the original records arrive" work of design note v0.4: a case selector, a side-by-side comparison of two records of the same case, a "Read the benchmark" view (showing "not run yet"), and the expected state next to the stated one on the second card. Case A (pilot) is present only as "original records not included yet".

**Why.** The demo's lead example becomes the difference between two records of the same model under two conditions. The screen is built on the Experiment 3 records before the pilot records arrive.

**What was checked, and where.** On Linux with Python 3: 59 app tests, the release tests, both UI logic checks and the checksum verification passed. A test pins the hashes of the four Case B records to those of the 1.1.0 candidate. The comparison, the pending case and the benchmark view were inspected in Chrome. Checked by Claude.

**Not yet checked.** The Case A package has not arrived; fixing it in the repository and acceptance item A1 are open. Including the control case (S3) requires widening joint success to "matches the expected state", which will raise the rules version. Launch on Windows (W1–W3) and a first-time reader check remain open.

## November 22: readability of the comparison (1.2.0 candidate, continued)

**What changed.** Above the comparison table: a one-sentence reading of the two records and the kind of comparison (same model or not, same condition or not). Column headings now show model, condition and the meaning of the condition symmetrically, with source details folded. The "4 of 6 items differ" count was replaced by a sentence naming what differs and what is the same. The joint row is named "Payment and correct handoff together (Experiment 3 primary)" and its condition is stated once under the table. The interface language can be switched between Japanese, English and both; original record text is not affected.

**Checks.** On Linux: 59 app tests, the UI logic checks and the checksum verification passed. The Japanese-interface comparison was inspected in Chrome. Checked by Claude. Launch on Windows and a first-time reader check remain open.

## November 22: Case A (pilot) included

**What changed.** The GPT pilot package (SHA-256 `fe946a01…e844`) was fixed unchanged in the experiment repository (M-Anchor-challenge, branch `exp4-pilot-case-a`, commit `b2a346a`). S2 was imported as Case A and S3 as its control, and Case A is now the initial view. It opens with ordinary caution (B) and the M-Anchor method (C) side by side.

**Conversion.** The pilot output has two fields, `payment` and `cause_state`, and its ledger record is a payment count only. To run it through the app's gate, `pay` becomes one payment matching the approval in a demo ledger, and `cause_state` becomes the cause field of the handoff. Amount, payee, request ID and approval ID are values supplied for this demo. The original output is kept in the case file, on the screen and in the source of each record.

**A1 check (automated, by Claude; not a human check).** Replayed through the app's gate and simulated ledger: in both B and C the payment is allowed (all 14 checks pass), ledger payments go 0 → 1, nothing is denied and no unauthorized change is applied. The cause is handed off as "confirmed" in B and "unconfirmed" in C. This matches the pilot record (payment count 1, cause state, joint flag). Amount and payee are checked against the demo ledger only.

**Rules.** The hashes of the four Case B records are unchanged from the 1.1.0 candidate (pinned by a test). The rules version stays `workflow-rules/1`. The Experiment 3 joint measure is defined for a cause handed off as unconfirmed, so it is not computed for the control case, whose expected state is "confirmed"; agreement with the expected state is shown instead. The two S3 outputs are the same text, so the source of the record follows the selected record.

**Reading notes.** In condition C the cause state (`unconfirmed`) is given to the model as an input field. This one example shows that a state passed in a field stayed in the handoff. One run per condition; variation was not measured. Request text is reconstructed from the pilot code; the request as sent and the full model response were not saved. Arms B and C are not exact replications of GC and C4 of Experiments 2 and 3. The receiver was not measured.

**Checks.** On Linux: app tests, release tests, both UI logic checks and the checksum verification passed. Checked by Claude. Rendering in a real browser on Windows and a first-time reader check remain open.
