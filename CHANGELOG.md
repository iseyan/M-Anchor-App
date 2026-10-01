# Changelog

[日本語](CHANGELOG.ja.md)

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
