# v0.5 validation record

[English](validation-v0.5.en.md) | [日本語](validation-v0.5.ja.md)

Work date: October 1, 2026 (Japan time). This app-development record covers verification and packaging automation, separately from formal research evaluations.

## Method

- 34 application tests: commit, rejection, no change, authority, old data, history, restart, and related behavior.
- 3 packaging tests: altered-source rejection, exact ZIP bytes and exclusion of unlisted files, unsafe/duplicate path rejection.
- UI logic: actual JavaScript with a minimal DOM substitute and real local HTTP server.
- Checksums: every listed release source file.

Model responses are mocked; no paid API or API key is used. Browser rendering and operation on the user's device are outside these CI checks.

## Results

Local Linux/Python 3.12 passed all four check groups. Retained sources: [report](observations/ci-v0.5-local/ci-report.json), [app tests](observations/ci-v0.5-local/app-tests.log), [packaging tests](observations/ci-v0.5-local/release-tests.log), and [UI log](observations/ci-v0.5-local/ui-logic.log).

The first local run began before the checksum manifest was updated and correctly failed on mismatched source files. The [initial report](observations/ci-v0.5-local/initial-ci-report.json) and [failure log](observations/ci-v0.5-local/initial-checksum-failure.log) are preserved. All checks passed after updating the manifest.

[GitHub Actions run #1](https://github.com/iseyan/M-Anchor-App/actions/runs/36743819362) succeeded for source commit `6a986b396fd1cba895e959ddc9982db9054b379b`. The [API receipt](observations/2026-10-01-ci-v0.5.json) records jobs and artifacts.

| Job | Result |
| --- | --- |
| Linux / Python 3.10 | 34 app tests, 3 packaging tests, UI logic, checksums passed |
| Linux / Python 3.13 | Same checks passed |
| Windows / Python 3.13 | Same checks passed |
| Package | ZIP creation, content verification, and artifact upload succeeded |

The documentation commit `790ec8dfb74ac5229d3c779ae9b53b7ba454944b` also passed all jobs in [run #2](https://github.com/iseyan/M-Anchor-App/actions/runs/36744155328).

These results describe hosted runners. They do not establish browser rendering on the user's Windows device, real-model behavior, or safety for arbitrary inputs. The uploaded ZIP was checked within the job before upload; it was not independently downloaded and compared by the reviewer.

## Change scope

v0.5 changed the app and screen version to 0.5 and added verification/packaging automation. Gate rules, formal core, client, model bridge, execution records, and data format were retained from v0.4.

The ZIP distributes source. It does not provide an executable, AWS deployment, or autonomous periodic model calls. See [v0.5.1](validation-v0.5.1.md) for the later language update.
