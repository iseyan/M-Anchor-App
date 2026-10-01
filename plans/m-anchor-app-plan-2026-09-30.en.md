# M-Anchor App — development and distribution plan

[日本語](m-anchor-app-plan-2026-09-30.ja.md)

September 30, 2026 (Japan time). Status at that date: basic operation of local prototype v0.2 checked; preparing simpler operation for a small distribution.

English translation of the [original Japanese plan](m-anchor-app-plan-2026-09-30.ja.md). This is a dated plan, not a statement that later work was already complete.

## 1. Name and purpose

The project is named **M-Anchor App**. The prototype interface at the time was named Anchor Control; the next distribution would align its name and explanation.

The aim is to inspect AI-generated record-update proposals and save only updates meeting defined conditions. Unsupported resolution must not discard unresolved candidates, while admitted evidence can support a permitted update.

The principle is **Model proposes; deterministic layer commits.** The model proposes; validation and persistence governed by rules outside the model decide whether the update is allowed.

## 2. Initial distribution scope

Use one connection method, a dedicated Python client, and one operation, case-record updates. The current model connection is the OpenAI Responses API; the user supplies an API key and model ID.

Run a local server on Windows and operate it through a browser. Authoritative records reside in local SQLite. The prototype requires Python but no additional pip installation.

Protection covers records in this store. Evidence admission and interpretation are configured outside the model. External-tool control, evidence-truth assessment, and general evaluation of an entire conversation are outside the initial scope.

## 3. Implementation

| Part | Role |
| --- | --- |
| Browser interface | Connection, case selection, proposal request, decision and history display |
| Model bridge | Provide case state and admitted evidence/interpretations; request an update proposal |
| Dedicated Python client | Read state and submit the model's proposal to the API |
| Gate and store | Validate proposals and persist permitted changes and audit records |

The two main client APIs are:

- `GET /v1/cases/{id}`: obtain current state and the evidence/interpretations admitted for that case.
- `POST /v1/cases/{id}/proposals`: submit a proposal.

Do not give the model an admin key, direct database access, shell, or external tools. Submit returned proposal text without JSON repair or replacement of fields.

## 4. Update rules to preserve

- Validate case ID, referenced version/hash, and proposal structure.
- A model's claim of approval does not change evidence admission or update authority.
- Reject candidate removal unsupported by admitted evidence and external interpretation. Preserve candidates when no evidence applies.
- Rejection and no change do not advance the record state, version, or hash.
- Save permitted changes, then read the authoritative record through a separate database connection to check the result.

Evidence admission and interpretation in the initial release are limited to initialization configuration. No UI approval path bypasses these rules.

This boundary applies to updates through the app. The prototype does not isolate programs able to write the database directly using the same OS user's permissions.

## 5. Observations available at the time

| Operation | Result | Material |
| --- | --- | --- |
| Submit a fixed unsupported-resolution proposal | DEMO-HOLD rejected; both candidates, version, and hash retained | Decision JSON and readback |
| Submit a fixed admitted-evidence update | DEMO-UPDATE changes to h_B, Version 1 to 2 | Decision JSON and readback |
| Process the case without evidence through a live model | DEMO-HOLD retains both candidates, unresolved, Version 1; no_commit / no_state_change | Model metadata and decision JSON |
| Operate an admitted-evidence update through a live model | DEMO-UPDATE shows h_B, resolved, Version 2 | User's case list after the operation |

The supplied live-model log names `gpt-5.4-mini-2026-03-17`. Eighteen development tests, including HTTP routes and mocked model responses, also passed.

These are basic app checks on two synthetic cases. Distinguish a model returning a valid no-change proposal from the gate rejecting an invalid proposal. Keep these development observations separate from existing research evaluations.

## 6. Next implementation and distribution work

First simplify operation so a user can launch the app and inspect a result without editing code.

1. **Launch and connection:** wait for server readiness before opening the page, reduce manual key setup, and show connection status.
2. **Case selection:** explain the uncertainty-preservation and valid-update cases; make the target clear immediately before execution.
3. **Result display:** distinguish Saved, Rejected, and No change, with concise reasons and before/after state. Show Undetermined if a transport failure leaves the outcome unknown.
4. **Repeat demonstrations:** distinguish updated and unused cases; create new test data without overwriting existing data.
5. **Distribution:** align name, launch instructions, environment requirements, API usage conditions, and license. Exclude user keys and databases. Consider executable packaging after these operational changes.

Additional connectors, multiple agents, evidence addition/revocation during operation, and external-tool writes are later extensions.

## 7. Initial release goal

Users should be able to launch, connect, select a case, run, and inspect results without editing Python. Unsupported resolution must leave the record unchanged; admitted-evidence updates must be saved and inspectable after restart.

Show operation and results concisely. Put proposal contents, evidence, before/after state, version, and hash in expandable details. Preserve the record-write path and evidence-admission boundary as features are added.
