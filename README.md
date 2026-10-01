# M-Anchor App

[日本語](README.ja.md)

Protect case records from unauthorized AI updates. M-Anchor App V1 lets you try adversarial inputs, inspect the resulting proposals, and verify what the gate actually saved. Unresolved candidates are retained unless admitted evidence supports a permitted change.

**Model proposes; deterministic layer commits.**  

## Publication materials

**M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates**

The [publication package](docs/publication/README.md) includes a technical note, reproduction steps, evidence mapping, Zenodo description, and upload instructions. Here, neutralization means blocking an unauthorized record transition at the gate. It does not mean preventing every incorrect model output. The app and included project materials are distributed under Apache-2.0. A Zenodo DOI for the app has not yet been assigned.

## Current version

**V1 / 1.0.0 — Record protection against prompt attacks.** Four attack scenarios and two controls can run as fixed proposals without an API, or as editable inputs through the existing model connection. The screen separates input, proposal, gate decision, and the read-back record. Model inputs are now saved with each submitted proposal. The app interface remains English-first with Japanese alongside it. Documentation is supplied as separate English and Japanese files.

Start with the [V1 guide](docs/v1-guide.md). The release remains a local source distribution.

| Document | Link |
| --- | --- |
| Purpose and scope | [Read](docs/overview.en.md) |
| Demonstration | [Read](docs/demo-guide.en.md) |
| Python client, API, records | [Read](docs/integration.en.md) |
| Automation and future AWS work | [Read](docs/automation-plan.en.md) |
| Decisions and evidence | [Read](docs/development-log.en.md) |
| Current validation | [Read](docs/validation-v1.md) |
| Scenarios and trace | [Read](docs/v1-guide.md) |
| Earlier observations and plan | [Read](docs/evidence-guide.md) |
| Release history | [Read](CHANGELOG.md) |

## Run on Windows

Requires Python 3.10 or later and the `py` launcher. No additional pip packages are needed. This is a source distribution; Python is not bundled.

1. Extract the app ZIP.
2. Double-click **`start.cmd`**.
3. The browser opens after the server is ready and connects automatically.
4. Select a Scenario and use **“Run fixed proposal (no API)”** first.

Keep the launch window open. Press Ctrl+C there to stop. Running the same `start.cmd` again retains the saved records and history.

Use **`start-fresh-demo.cmd`** for a new demonstration. It creates a separate folder under `demo-runs/` and preserves previous data. The local port may change at each launch.

A page reload clears the keys held in page memory. Open “Connect manually” and enter the keys from `credentials.json` in the data folder shown by the launcher. To reconnect automatically, stop and relaunch the app.

## Keep existing data

1. Stop the older app with Ctrl+C.
2. Extract the new ZIP into a separate folder.
3. Before its first normal launch, copy the old `data` folder into the new `m-anchor-app/data`. Keep the original as a backup.
4. Open the new `start.cmd`.

For a differently named data folder:

```powershell
py -3 app\launcher.py --data "path-to-existing-data"
```

V1 retains the existing database layout and adds optional exercise fields inside execution metadata. Data from v0.4–v0.5.1 can be retained. Earlier data gains execution-metadata tables without inventing missing dates or model IDs. Existing cases, evidence, decisions, and connection keys are retained. Initialization never overwrites an existing store; incomplete folders cause an error.

## Connect a model

Select a case and enter an OpenAI API key, a model ID available to that key, and your request. Each run makes one API call, then submits the exact proposal through the dedicated Python client. Your request and case context are sent to OpenAI and API charges apply. Both English and Japanese requests are accepted; the example text is bilingual and editable.

The API key is excluded from model input and database records. Raw proposals and V1 model inputs are retained in audit history and included in JSON exports. Do not paste secrets into the input. Failed API calls are not retried automatically. If the saving outcome is unclear, refresh state and history before submitting again.

## Validation and scope

The [V1 validation record](docs/validation-v1.md) distinguishes local checks, hosted CI, and unverified behavior. The suite contains 40 application tests, 3 packaging tests, and a UI logic check. Model responses are mocked; CI makes no paid model calls. Earlier user-supplied demo records are indexed in the [evidence guide](docs/evidence-guide.md).

Protection covers case records in this local store. The app does not establish evidence truth, control external tools, or isolate processes that already have direct access to the database. Evidence admission is configured during initialization. See the integration guide before considering a business connection.

## Development

```sh
python3 app/launcher.py
python3 -m unittest discover -s app -v
python3 scripts/check_ui.py
python3 scripts/ci.py
python3 scripts/build_release.py --output dist
```

The UI logic check needs Node.js. CI and packaging record their results and check file hashes.

## Download from GitHub

1. Open [Actions](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml) and choose a successful run.
2. Download `m-anchor-app-package-<number>` from Artifacts.
3. Extract it to find the app ZIP, its SHA256, and `build-info.json`.
4. Extract the app ZIP and open `start.cmd`.

Logs are in `verification-<OS>-py<version>`. Artifacts are configured for 14-day retention; GitHub sign-in may be required. Executable packaging remains future work. Distribution terms are given below.

## License

Copyright 2026 Ise (iseyan). This distribution, including its source code, project documentation, and included observation records, is licensed under the [Apache License 2.0](LICENSE), except where otherwise stated. Commercial use, modification, and redistribution are permitted under its terms. See [NOTICE](NOTICE) for attribution. The separate linked M-Anchor Framework repository and external materials are not relicensed by this declaration.

Redistribution must meet the license's notice and change-marking conditions. The software is provided without warranties as specified in the license; this is not an additional usage restriction. Trademark rights are not granted except as the license provides.

Related project: [M-Anchor Framework](https://github.com/iseyan/m-anchor-framework)
