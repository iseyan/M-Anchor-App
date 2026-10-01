# V1 validation

[日本語](validation-v1.ja.md)

Version: 1.0.0. Work date: October 1, 2026 (Japan time). This is a local record-protection release, separate from formal research evaluation.

## What changed

Four synthetic attack scenarios and two controls were added through an admin-only catalog/run API. The model route optionally accepts a scenario ID and saves exact input text plus SHA256 in `execution.exercise`. The existing one-use ticket binds that observation to case and proposal bytes. Input, proposal source, gate decision, and independent readback are shown together in the bilingual interface.

Gate rules, formal core, provider-request implementation, and Python client remain byte-identical to v0.5.1. Exercise metadata does not grant authority. The observation schema remains v2 with optional fields, and the SQLite layout is unchanged. Missing historical inputs remain missing.

## Local checks

Environment: Linux, Python 3.12.14, Node.js 24.19.0. All model outputs in these tests are mocks. No API key is required and no paid model API is called.

| Check | Result | Evidence |
| --- | --- | --- |
| Application | 40 passed | [Log](observations/ci-v1-local/app-tests.log) |
| Packaging | 3 passed | [Log](observations/ci-v1-local/release-tests.log) |
| UI logic | Passed | [Log](observations/ci-v1-local/ui-logic.log) |

The six added application checks cover admin-only scenario routes and strict payloads; preservation of full state/evidence authority for all four attacks; positive and no-change controls; exact input/proposal linkage through a real server restart; invalid scenario/case rejection before model generation; and rollback when exercise recording fails. The existing ticket check also verifies that later mutation of the source exercise object does not change its bound copy.

The UI check executes the actual JavaScript with a minimal DOM substitute and real local HTTP. It covers all six fixed scenarios, mocked model input, past-entry switching, JSON export, key-field exclusion, and an API failure displayed as unverified without adding a false rejection entry. Raw input is displayed using textContent, not inserted as HTML.

Packaging tests use a small synthetic fixture version; actual V1 packaging separately checks every source-manifest hash and ZIP entry. HTML nesting, unique IDs, and local documentation links are also inspected during preparation.

## Hosted checks / GitHub Actions

[Run #5](https://github.com/iseyan/M-Anchor-App/actions/runs/36791415008) succeeded for source commit `8c5f7c86fe78067c43b01b3c05e3ef28a11fa470`. All three verification environments and the packaging job completed successfully. The [API receipt](observations/2026-10-01-ci-v1.json) records jobs and artifacts.

| Environment | Result |
| --- | --- |
| Linux / Python 3.10 | 40 app tests, 3 packaging tests, UI logic and checksums passed |
| Linux / Python 3.13 | Same checks passed |
| Windows / Python 3.13 | Same checks passed |
| Packaging | ZIP built, verified and uploaded |

The ZIP is verified inside the packaging job before upload. The reviewer did not independently download the uploaded artifact. A later documentation commit triggers another run, shown in Actions.

[Actions runs](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)

## User observation received later

The [October 1 user observation](observations/2026-10-01-user-check-v1.md) retains a cumulative 20-entry export: 18 fixed proposals and two model-route no-change results. Exact input/proposal correspondence, state hashes, history continuity, and readbacks matched. The HOLD model output preserved uncertainty; UPDATE was already Version 2. A model-generated Version 1→2 commit is still unobserved in that export. These user observations are separate from the mocked automated checks above.

A separate export at 10:22 Japan time subsequently records the missing positive control: model route, admitted e_B, `commit / accepted`, Version 1→2, and matched readback. The observation now retains both original exports and the matched input, proposal and state checks. The planned basic fixed/model checks are complete for these supplied examples; this is not a general robustness claim or a research-stage completion.

## What these automated results do not establish

Fixed proposals test the gate even when the proposed update is invalid; they do not test model resistance. Mocked model calls test application integration, not live-model robustness. No attack detection rate, universal jailbreak protection, external-tool control, or indirect-injection integration is claimed. Full browser rendering and operation of V1 on the user's device remain unverified by these automated checks.

V1 records inputs that reach the gate through the model route. An API error before proposal submission is shown on screen but has no gate-history entry. Key input fields are excluded; secrets pasted into request/proposal text would still be recorded. See [V1 guide](v1-guide.md).
