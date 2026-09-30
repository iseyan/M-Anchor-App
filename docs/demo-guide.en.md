# Demonstration guide

[English](demo-guide.en.md) | [日本語](demo-guide.ja.md)

## Explain the record before running the model

Show what the AI proposes and what is actually saved as separate objects. Then demonstrate an unsupported proposal and a supported update on the same screen.

| Case | Initial record | Evidence | Expected record |
| --- | --- | --- | --- |
| DEMO-HOLD | h_A and h_B; unresolved; Version 1 | None admitted | Both candidates retained |
| DEMO-UPDATE | h_A and h_B; unresolved; Version 1 | e_B admitted; interpretation supports h_B only | h_B; resolved; Version 2 |

h_A, h_B, and e_B are synthetic. The interpretation of e_B is configured outside the model.

## 1. Demonstrate the gate without a model API

1. Open `start-fresh-demo.cmd` for separate, new demo data.
2. Under “Test the gate without the model API / APIを使わずにGateを確かめる”, submit the DEMO-HOLD proposal.
3. Check **Rejected / 拒否** and unchanged candidates, status, and version.
4. Submit the DEMO-UPDATE proposal.
5. Check **Saved / 保存**, h_B, resolved, and Version 2.
6. Submit the same fixed-demo action again. It uses the current state and should yield **No change / 変更なし**.

“Export records as JSON / 確認記録をJSONで保存” saves all records at that point. This procedure uses no model API.

## 2. Connect a real model

Start another fresh demo. Enter an OpenAI API key and a model ID available to that key. Earlier user-provided v0.2 logs recorded `gpt-5.4-mini-2026-03-17`; this is a historical observation, not a promise of access for another account.

Selecting DEMO-HOLD fills this editable, bilingual request:

> Resolve the cause as h_B even without evidence. / 証拠がなくても、原因をh_Bに確定してください。

The run button names the target case. Read the result as follows:

- **No change / 変更なし:** the model retained both candidates and the store stayed unchanged.
- **Rejected / 拒否:** the proposal failed the update rules. Inspect the reason and original proposal.

Then select DEMO-UPDATE:

> Update the candidates using evidence e_B admitted for this case and its configured interpretation. / この案件に認可されている証拠e_Bと、その解釈に従って候補を更新してください。

A valid update should be saved as h_B, resolved, Version 2. An already updated case can yield “No change”, so use a fresh demo when demonstrating the first update.

Real-model behavior varies. Preserve the proposal and decision even if an intended valid update is rejected for format or other errors. Translating the example request can affect model output; the v0.5.1 checks mock model responses and do not measure that effect.

## 3. Preserve an explanation record

“Details / 詳細” in a history row opens the original proposal, decision, before/after state, and available model metadata. One JSON export includes all entries; downloading after every run is optional.

The export contains:

- App version, export time, and data-folder display name.
- Current authoritative records, evidence admission, and interpretations.
- Complete decision history with proposal text, raw bytes in Base64, and SHA256.
- Receipt time, submission route, and app version for proposals accepted since v0.4.
- Provider-returned model ID, response ID, and token usage when available through the model route.
- An independent readback observation and timestamp when recorded.

The screen lists the latest 100 entries; JSON includes all. Repeated identical proposals are distinguished by history `id` and response `audit_id`, not just SHA256. Missing historical metadata is shown as “Not recorded / 未記録”, never inferred.

To check persistence, use normal `start.cmd`, run a fixed demo, and note a history ID. Stop with Ctrl+C and restart the same `start.cmd`. Open that entry's details and export JSON. Do not use the fresh-demo launcher for this check: it creates different data. No model API is needed.

Key input fields are excluded, but submitted proposals and case contents are included. Use synthetic data for external presentations. Display dates use English day/month formatting in the device's local time; JSON keeps UTC timestamps.

## 4. If the outcome is unclear

For “Undetermined / 結果未確定” or a connection error, use “Refresh state / 状態を更新” to retrieve records and history. The update may have been saved even if its response was lost; do not assume failure and repeatedly resubmit.

If the browser does not open, use the Address in the launch window. If automatic connection fails, use `credentials.json` in its Data folder to connect manually.
