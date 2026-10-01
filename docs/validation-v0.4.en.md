# v0.4 validation record

[日本語](validation-v0.4.ja.md)

Work date: October 1, 2026 (Japan time). Target: the local M-Anchor App prototype. This is separate from formal research evaluation.

This is an English translation of the [dated Japanese record](validation-v0.4.ja.md); statements about unperformed work refer to that original review.

## Results

All 34 automated tests passed on Linux / Python 3.12 in 15.934 seconds ([test log](validation-v0.4-tests.txt)). The actual UI JavaScript also passed checks with a minimal DOM substitute and real HTTP server ([UI log](validation-v0.4-ui.txt)).

Model responses were replaced in the tests. The checks verified model-route record retention, not live-model generation quality. No paid API call was made.

| Area | Method and result |
| --- | --- |
| Commit, rejection, no change | Existing state, version, hash, and evidence-admission tests passed |
| Persistent execution metadata | After a mocked model update and another fixed demo, stop and recreate the HTTP server; confirm original model metadata, proposal, decision, and readback remain in JSON |
| Decision correspondence | Repeated identical proposals have separate IDs. Concurrent submissions link one commit and one rejection to their own execution records |
| Atomicity | Deliberately fail an INSERT into executions with a SQLite trigger; confirm case update, audit, and execution records all roll back |
| Migration | Recreate the old schema without execution tables. Add the tables while preserving all old audit columns and records; missing old metadata remains null and new metadata can be appended |
| Submission route | Distinguish fixed demo, manual, and client API. Agent keys cannot call admin routes or claim a model route using arbitrary headers |
| Internal ticket | Verify binding to case and proposal bytes, single use, and expiry rejection |
| Raw bytes | Malformed and invalid-UTF-8 proposals can be recovered from Base64 with matching SHA256 |
| Full export | For 103 database entries, the screen list contains 100 and JSON contains all 103 |
| Readback record | Normal results are matched; cases without an identifiable state, such as malformed proposals, are not_applicable. An interrupted unrecorded readback is null, not verified |
| Secrets | Ordinary key fields and the model-request API key are excluded from export. Only the four designated model metadata fields are accepted |
| UI logic | Automatic connection, case selection, three decisions, past-entry details, complete export, and unchanged export content after viewing details |

## Changes to decision handling

Execution tables and atomic storage were added to the gate's Store, and audit_id was added to responses. The gate file as a whole changed. The syntax trees of `_parse_proposal`, `_validate_authority`, and `_evaluate`, responsible for proposal interpretation, evidence authority, and candidate transitions, matched the previous implementation.

The formal core `app/vendor/python_v0.1/m_anchor_minimal.py` retained SHA256 `0f9551e8d00cd4408441944d9067cfe9bce7d5653019a5af27738fb5895f58c9`.

## Unverified or outside scope

- v0.4 launch, actual browser rendering, and new live-API records on the user's Windows environment. These automated checks ran on Linux.
- Migration recreated the old schema; it did not directly operate on the user's database.
- Signed provenance, tamper resistance, and isolation from programs with OS-level access to write the database.
- Large-history load, power-loss, and media-failure testing. Fault injection covered SQL errors and unrecorded readback states.
- API failures before a model response are not decision-history entries because no proposal exists.
- GitHub Actions execution and AWS deployment or continuous operation were not performed in this work.

## Run the checks

```sh
python3 -m unittest discover -s app -v
python3 scripts/check_ui.py
```

The app needs no additional pip dependencies. UI logic checks use Node.js. Real-browser demonstration steps are in the [demo guide](demo-guide.en.md).
