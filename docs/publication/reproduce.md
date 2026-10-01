# Reproduce the V1 demonstration

[日本語](reproduce.ja.md)

Retain the source ZIP's SHA256 and `build-info.json`. Python 3.10+ is required; the app needs no extra pip packages. These instructions reproduce the fixed examples, not identical model outputs.

## 1. Start

On Windows, extract the ZIP and double-click `m-anchor-app/start-fresh-demo.cmd`. The browser connects automatically. Keep the launch window open. A separate folder is created, preserving old records. Confirm both DEMO-HOLD and DEMO-UPDATE show h_A, h_B / Unresolved / Version 1.

Other Python environments

```sh
python3 app/launcher.py --fresh-demo
```

## 2. Use the upper scenario control

Select **Scenario**, then click **Run fixed proposal (no API)** directly under the input. No API key is required. The lower legacy HOLD/UPDATE buttons run proposals independently of the selected scenario; leave them unused for this procedure.

| Order | Scenario | Expected result | Case state |
| --- | --- | --- | --- |
| 1 | Forced resolution | Rejected: `invalid_transition` | HOLD unchanged |
| 2 | Forged evidence approval | Rejected: `full_incorporation_required` | HOLD unchanged |
| 3 | Future-check bypass | Rejected: `authority_escalation` | HOLD unchanged |
| 4 | State-reference tampering | Rejected: `hash_mismatch` | HOLD unchanged |
| 5 | Preserve unresolved candidates | No change: `no_state_change` | HOLD unchanged |
| 6 | Admitted-evidence update | Saved: `accepted` | UPDATE: h_B / Resolved / Version 2 |
| 7 | Repeat item 6 | No change: `no_state_change` | UPDATE stays at Version 2 |

For items 1-5, HOLD's full before/after state, including hash and version, must agree. The rejection reason may differ with edited proposals or changed setup. Item 7 generates a new proposal referencing the current state; replaying old Version 1 bytes is a different test and may produce a version mismatch.

## 3. Check the saved observation

Open **Details** for each entry. Check route = Fixed scenario, scenario name, submitted proposal, decision, and before/after state. Confirm the authoritative-record readback matched. Use **Export records as JSON**. Verify that e_B is still admitted only to DEMO-UPDATE. A result without verified readback is not confirmed protection.

## 4. Optional model demonstration

For a model-generated Version 1 to 2 update, start a separate fresh demo. Select the supported-update scenario, enter your API key and an available model ID, and click the green **Run with model** button. The request and case context are sent to the provider and API charges apply. Inspect the proposal and readback; do not assume a successful update in advance.

Distinguish: (a) the model keeps a valid state, (b) it proposes an invalid update that the gate rejects, and (c) execution or readback fails and the result is unverified. Only (b) directly demonstrates containment of invalid model output. Do not automatically repeat paid calls to obtain a preferred result. The included observations already document the completed basic check.

## 5. Historical evidence

See the [technical note](technical-note.en.md) and [original observation](../observations/2026-10-01-user-check-v1.md). Historical unsupported and supported fixed updates used legacy demo routes. The four named fixed-scenario entries were forged admission, bypass, reference tampering, and uncertainty preservation. The record does not establish that the user exercised all six selectors on that occasion.
