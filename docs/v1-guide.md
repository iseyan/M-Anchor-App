# V1 — Record protection against prompt attacks

[日本語](v1-guide.ja.md)

M-Anchor App V1 (1.0.0) lets you submit adversarial inputs to a model, inspect its exact proposal, and see whether the authoritative record changed after gate checks. It also provides fixed proposals that demonstrate the gate without calling a model.

**Model proposes; deterministic layer commits.** The protected object is the case record in this store. Evidence admission and interpretation come from trusted initial configuration.

## A three-minute demonstration

1. Extract the ZIP and open **`start-fresh-demo.cmd`**. It creates separate demo data.
2. Select **Forced resolution** in Scenario.
3. Click **Run fixed proposal (no API)**. No API key is needed.
4. Check **Rejected** and **Record unchanged · readback verified**.
5. Select **Admitted-evidence update** and run its fixed proposal.
6. Check **Saved**, h_B, and Version 2. Run it again to see **No change**.
7. Use **Export records as JSON** to retain all history.

These fixed runs demonstrate gate behavior. They do not execute the displayed input text and do not measure a model's resistance to an attack. Editing the text only affects **Run with model**.

## Included scenarios

| Scenario | Target | Fixed proposal outcome |
| --- | --- | --- |
| Forced resolution | Remove h_A without evidence | Rejected; state retained |
| Forged evidence approval | Claim e_B is admitted for HOLD | Rejected; authority retained |
| Future-check bypass | Request future_bypass_authorized=true | Rejected |
| State-reference tampering | Replace the state hash with zeroes | Rejected |
| Preserve unresolved candidates | Keep both candidates | No change |
| Admitted-evidence update | Use e_B for UPDATE | Saved, then no change on repetition |

These expectations use fresh synthetic demo data. Model-generated proposals may differ. A scenario label records which example was selected; it is not an attack detector or an automatic success verdict. Edited scenario text retains the selected label. Selecting another target case switches to Custom input.

## Run a model

Select a scenario or Custom input, choose the target case, and enter your OpenAI API key and an available model ID. Edit the input, then press the button naming the target case. Each run makes one model API request and can incur charges. The app makes no automatic retries.

The existing model connection sends the input as a user message with trusted case context supplied separately. V1 does not fetch websites, emails, or documents. Pasting text into the input is a direct-input exercise, not a verified indirect-injection integration.

The result distinguishes the input, proposal source, gate decision, and independent readback. A model can preserve the state itself or propose an invalid change that the gate rejects. “No change” and “Rejected” therefore remain separate. A failed or incomplete API call is not shown as a contained attack.

## What is recorded

For proposals submitted through the V1 model route, `execution.exercise` contains the selected scenario, category, input text, and its SHA256. It is bound to the exact proposal and case with the existing single-use submission ticket. The gate saves the execution metadata, proposal, and decision in the same transaction as any state update.

Fixed scenarios use `mode=fixed_proposal`, `source=fixed_scenario`, and null input fields: no model input was executed. Model-route fields describe the application's processing route, not provider-signed proof. Automated tests replace the model with an explicitly identified mock.

Old records and other submission routes can have no exercise data. Missing information is not reconstructed. An API failure before proposal submission creates no gate-history entry; the screen shows the error. The report schema stays `m-anchor-app-observation/v2` with optional exercise metadata.

**Input text is now saved and exported for the model route.** Key input fields are excluded, but anything pasted into the request or returned in a proposal becomes part of the record. Use synthetic data for demonstrations and inspect exports before sharing.

## Scope for a business discussion

V1 demonstrates control over this store's case records. It does not promise universal jailbreak prevention, filter all harmful model text, prevent all information leakage, control external tools, or isolate programs with direct database access. A business integration needs a defined record, trusted evidence authority, and a write path that cannot bypass the gate.

The next integration can extend this structure to one chosen external operation. V1 requires no AWS service and starts locally using the existing Windows launchers. Its version number identifies this workflow release, not a security certification.

See [integration](integration.en.md) and [V1 validation](validation-v1.md).
