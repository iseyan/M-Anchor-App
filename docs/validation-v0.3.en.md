# v0.3 validation record

[日本語](validation-v0.3.ja.md)

Target: M-Anchor App v0.3. Date: September 30, 2026. Environment: Linux / Python 3.12; Node.js for UI logic checks.

This is an English translation of the [dated Japanese record](validation-v0.3.ja.md). It preserves the observations and limitations recorded at that time.

## Checks performed

| Method | Result | Scope |
| --- | --- | --- |
| `python3 -m unittest discover -s app -v` | 25 passed (10.760 seconds) | Real HTTP routes, store, role-based authentication, mocked model, launcher |
| `python3 scripts/check_ui.py` | Passed | Actual UI script with a DOM substitute and real HTTP: automatic connection, required case selection, rejection, commit, no change, mocked model route, export correspondence, and key exclusion |
| `node --check` on the UI script | Passed | JavaScript syntax |
| Byte comparison of gate, formal core, model bridge, and client | Identical to v0.2 | Existing validation rules and connection implementation were unchanged |

The 25 tests comprise 18 retained from v0.2 and seven for the new launch and record features. This count is not a count of attacks against a live model.

## Main behavior

- Reject unsupported candidate removal and preserve state.
- Save an admitted-evidence update, reopen the database, and verify the result.
- Do not advance version or hash when no change is needed.
- Commit only one of concurrent proposals referencing the same version.
- Reject cross-case evidence admission, authority escalation, and duplicate JSON keys.
- Reject agent-key access to admin APIs.
- Allow a launch ticket once, with the correct value and same Origin.
- Reject expired or reused launch tickets; do not embed keys in HTML.
- Match exported records to history and exclude connection keys.
- Create a new demo in a separate folder without overwriting existing data.

## Development failure and correction

The first 25-test run included one export-test failure with HTTP 503. The export transaction overlapped the transaction started by `authority_snapshot()` itself.

Export was changed to copy the source store into memory with SQLite backup, then read state and history from that copy. Gate bytes were preserved. All 25 tests passed after the correction.

## Checks not performed

- v0.3 batch launch, automatic connection, browser display, and download on the user's Windows device.
- End-to-end checks in a real browser, including rendering, CSP, fragments, and history handling.
- Paid live-model API calls in v0.3. The connection implementation itself was unchanged from v0.2.
- Long-term operation, large databases, multiple users, and write routes in external business systems.

The development environment had no browser executable; downloading one failed with HTTP 403 under network restrictions. UI logic checks are not treated as equivalent to real-browser checks.

The user's v0.2 observations are recorded separately in the [development log](development-log.en.md).

## Original records

- [Automated test output](validation-v0.3-tests.txt)
- [UI logic output](validation-v0.3-ui.txt)
- Distribution-root `SHA256SUMS.txt`: file integrity checks, not a digital signature.
