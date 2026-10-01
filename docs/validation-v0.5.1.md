# v0.5.1 validation

[日本語](validation-v0.5.1.ja.md)

Work date: October 1, 2026 (Japan time). This release makes English primary while retaining Japanese in the interface and documentation. It is an app-development check, separate from formal research evaluation.

## Change scope

- English-first headings, decisions, state labels, history, errors, and editable example requests; the page language is English, with Japanese marked on static companion text.
- English overview, demonstration, integration, automation, development, and v0.5 validation guides paired with Japanese files. Bilingual README, changelog, and evidence index.
- Bilingual messages for malformed manual JSON and missing case IDs.
- App version 0.5.1; observation schema remains v2.

Gate rules, formal core, model bridge, Python client, record implementation, and original observation files are checked against the v0.5 source hashes. Stored proposals and technical reason codes are not translated. The English/Japanese example request is a changed model input; no claim is made that its real-model output is identical to the older Japanese-only request.

## Local results

Environment: Linux, Python 3.12.14, Node.js 24.19.0.

| Check | Result | Evidence |
| --- | --- | --- |
| Application | 34 passed | [Log](observations/ci-v0.5.1-local/app-tests.log) |
| Packaging | 3 passed | [Log](observations/ci-v0.5.1-local/release-tests.log) |
| UI logic | Passed | [Log](observations/ci-v0.5.1-local/ui-logic.log) |

The UI check runs the actual JavaScript against a minimal DOM substitute and a real local HTTP server. It checks English-first paired labels, automatic connection, explicit case selection, invalid manual JSON, fixed rejection/commit/no-change, a mocked model route, past-entry details, export history, and exclusion of key inputs.

Release packaging also verifies the source manifest and all ZIP entries. HTML nesting, unique IDs, and local documentation links are checked during preparation. The source manifest is updated after documentation is complete; it does not automatically accept mismatched source files.

## Hosted CI / GitHub Actions

[Run #3](https://github.com/iseyan/M-Anchor-App/actions/runs/36746901627) succeeded for source commit `b9dc3ccd2cd7f8c86e3781af03bea6307b488639`. Linux/Python 3.10 and 3.13, Windows/Python 3.13, and the packaging job all completed successfully. Each verification environment ran the 34 app tests, 3 packaging tests, UI logic, and source checksums. The [API receipt](observations/2026-10-01-ci-v0.5.1.json) records job results and artifacts.

The archive is checked in the packaging job before upload; the uploaded ZIP was not separately downloaded and compared by the reviewer. Later documentation commits trigger their own runs, available in the Actions list.

[Actions runs](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)

## Limits

No paid model API is called. Real-model responses to the bilingual prompts, full browser rendering, screen-reader behavior, and the user's Windows browser layout have not been verified by these local checks. CI is runner verification, not a user-device observation. Historical JSON remains evidence only for its original version and scope.
