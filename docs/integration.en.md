# Integration and protection boundary

[English](integration.en.md) | [日本語](integration.ja.md)

## Dedicated Python client

`AnchorClient` in `app/client.py` retrieves case state and submits proposals. Use the Address shown by the launcher and the agent key in the selected data folder's `credentials.json`.

Run this example from the repository root. Pass the model's response as `raw_json` without repairing or replacing its fields.

```python
import os
import sys
sys.path.insert(0, 'app')
from client import AnchorClient

client = AnchorClient(
    os.environ['ANCHOR_AGENT_TOKEN'],
    os.environ['ANCHOR_BASE_URL'],
)
context = client.state('DEMO-HOLD')
# Give context to the model to obtain raw_json.
# Submit the original response without repair or field replacement:
# result = client.propose('DEMO-HOLD', raw_json.encode('utf-8'))
```

| API | Key | Purpose |
| --- | --- | --- |
| `GET /v1/cases/{id}` | agent_token | Case state and its admitted evidence/interpretations |
| `POST /v1/cases/{id}/proposals` | agent_token | Submit raw JSON |
| `GET /admin/scenarios` | admin_token | Six synthetic attack/control scenarios |
| `POST /admin/scenario-run` | admin_token | Submit the selected fixed proposal, without a model call |
| `GET /admin/cases` | admin_token | All cases and evidence settings |
| `POST /admin/demo-run` | admin_token | Generate and submit a fixed demo proposal on the server |
| `POST /admin/cases/{id}/proposals` | admin_token | Submit manually edited raw JSON through the same gate |
| `GET /admin/history/{id}` | admin_token | One entry, including raw proposal and execution metadata |
| `GET /admin/history` | admin_token | Latest 100 decisions |
| `GET /admin/report` | admin_token | Full v2 export from a consistent database snapshot |
| `GET /admin/info` | admin_token | App version and data display name |
| `POST /admin/model-run` | admin_token | One model generation followed by Python-client submission |

HTTP 200 means a check result was received. Read `decision` to determine what happened to the record.

| decision | UI | Meaning |
| --- | --- | --- |
| commit | Saved / 保存 | Update committed |
| reject | Rejected / 拒否 | Proposal rejected under the rules |
| no_commit | No change / 変更なし | Stored state unchanged |
| undetermined | Undetermined / 結果未確定 | Outcome not confirmed; refresh state and history |

## Automatic connection at launch

`launcher.py` waits for an HTTP response from the local server before opening the browser. It generates a random, single-use launch ticket valid for 120 seconds.

The ticket travels in the URL fragment and is immediately removed from the address bar. Fragments are not part of HTTP request URLs. A same-origin `POST /launch-session` exchanges the ticket for the admin and agent keys, kept in page memory. Expired, reused, or mismatched tickets are rejected.

This convenience does not change gate rules or evidence authority. Normal keys are not embedded in URLs, HTML, or persistent browser storage. The launch ticket itself grants connection access while valid, so its URL is not a sharing mechanism.

## Data and authority

`state.sqlite3` holds records and audits; `credentials.json` holds app connection keys. The model API key is not saved to files or the database. Normal launches use `data/`; fresh demos use separate folders under `demo-runs/`.

The model receives case state, admitted evidence and interpretations, the request, and proposal-format instructions. It receives no admin/agent keys, database path, shell, or external tools. Requests specify `store:false`; that flag alone does not determine all provider retention terms.

The server binds to 127.0.0.1 and checks Host, Origin, and role-specific keys. It does not isolate programs that can already read or write the database and key files using the same OS permissions. A business integration must place model permissions and authoritative-store write permissions accordingly.

This version has no runtime evidence admission/revocation, candidate restoration, external tool execution, encrypted storage, or audit retention/rotation policy. Hashes check consistency; they are not signatures against an actor with write access.

## Explanation records

`/admin/report` uses SQLite backup to make a consistent in-memory copy and reads records, evidence configuration, and history from it. It does not update the source store. Copying the full database into memory is intended for a small local demo.

The output schema remains `m-anchor-app-observation/v2` in V1 (1.0.0). Each history entry includes:

| Field | Meaning |
| --- | --- |
| id | Unique history number, corresponding to response audit_id |
| execution.source | live_model / fixed_scenario / fixed_demo / manual / agent_api |
| execution.received_at_utc | Server time immediately before gate processing, not commit completion |
| execution.app_version | Receiving app version |
| execution.submitted_case_id | Target case, retained even for an invalid proposal |
| execution.model_metadata | Provider model, response_id, input_tokens, output_tokens; otherwise null |
| execution.exercise | Optional V1 scenario and exact model-input record; see below |
| proposal_text | Original UTF-8 text, or null for invalid UTF-8 |
| proposal_base64 | Raw bytes; decoded SHA256 matches raw_sha256 |
| readback | status (matched / mismatch / not_applicable) and checked_at_utc |

Null `execution` means metadata was not recorded. Dates and model IDs are not reconstructed. Null `readback` means missing information or interruption before the separate readback record; it is not a successful verification. `matched` means a match was observed at the stated time.

State updates, audit decisions/raw bytes, and execution metadata are committed in one SQLite transaction. A failure to save execution metadata rolls back the state and decision as well. Independent readback is a later observation recorded separately.

The model route accepts four metadata fields from the server's generation process. A random, single-use in-memory ticket binds them to the exact proposal SHA256 and target case for 60 seconds. The dedicated client submits to the normal gate API. A caller's claim of `source=live_model` does not create model provenance.

Fixed demos and manual submissions use separate admin routes, all subject to the same gate. Ordinary external client submissions are `agent_api`; their authorship as AI or human is not identified.

These records describe the server's processing route. They are not provider signatures or tamper-proof evidence. Tests that replace model responses still use that route and explicitly identify the mock in logs/model IDs. Key input fields are not saved. Since V1, model-route input text is saved exactly alongside the proposal, so secrets pasted into the request would be recorded. Older versions did not retain this input.

The UI's 100-entry display limit does not remove old exported records. Large-data pagination and retention are not implemented. English/Japanese presentation never translates saved proposal bytes, JSON field names, reason codes, or hashes.

## V1 exercise metadata

`GET /admin/scenarios` lists four attack scenarios and two controls. `POST /admin/scenario-run` accepts exactly `{"scenario_id":"authority_override"}` (or another listed ID), chooses its target on the server, and submits a fixed proposal through the unchanged gate. It never calls a model and does not execute edited input text.

`POST /admin/model-run` accepts the existing four fields and optional `scenario_id`. Omission means `custom`. Named scenarios must match their configured case; unknown IDs, mismatched targets, or caller-supplied exercise objects fail before model generation. This label describes a selected exercise, not a trusted judgment about input.

V1 saves optional `execution.exercise` with schema `m-anchor-exercise/v1`, `scenario_id`, `category`, bilingual `title`, `mode`, `input_text`, `input_sha256`, `input_origin`, and `input_sent_to_model`. For model requests, the exact text and hash are bound to case/proposal bytes through the single-use ticket. For fixed scenarios, input fields are null and input_sent_to_model is false. Mode is `model_request` or `fixed_proposal`. Fields describe the server route, including an explicitly mocked route in tests; they are not provider-signed attestations.

Exercise metadata is observational only. It cannot admit evidence, modify gate rules, or authorize a state transition. Old entries and other routes can lack it. The existing SQLite execution JSON stores the additional fields without a database-schema change. If a model call fails before proposal submission, no gate-history entry is created; the UI shows an error and no protection verdict.

See the [V1 guide](v1-guide.md) for scope and the changed input-retention behavior.
