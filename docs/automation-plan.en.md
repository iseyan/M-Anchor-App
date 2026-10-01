# Development automation and future AWS operation

[日本語](automation-plan.ja.md)

Recorded October 1, 2026 (Japan time). Development automation was implemented in v0.5. AWS operation remains a design proposal; no AWS resources have been created for this app.

## Two kinds of automation

| Purpose | Mechanism | Work |
| --- | --- | --- |
| Development, verification, distribution | GitHub Actions | Test changes, package source, retain logs |
| App operation | A future execution platform such as AWS | Fetch cases, request proposals, submit to the gate, record results |

The original plan considered Fargate for a continuously running container and EventBridge Scheduler for periodic ECS tasks. Choosing a deployment model requires a concrete integration and operating frequency.

## Implemented: verification and packaging

`Verify and package` runs on pushes to main, pull requests, and manual dispatch.

| Item | Configuration |
| --- | --- |
| Environments | Linux/Python 3.10 and 3.13; Windows/Python 3.13; Node.js 24 |
| Checks | 34 app tests, 3 packaging tests, UI logic, source checksums |
| Failure | Save available logs; do not begin the packaging job |
| Packaging | After all verification jobs pass, build and verify a ZIP from the same commit |
| Pull requests | Verify only; pushes and manual runs also package |
| Records | Environment, run ID, source commit, and check results in JSON |
| Retention | Artifacts retained for 14 days |

The workflow has read-only `contents` permission. External actions are pinned to the official release commit SHAs obtained during implementation. Checkout credential persistence is disabled. No additional API secrets are required; model responses are mocked.

`scripts/ci.py` and `scripts/build_release.py` run the same process locally. `SHA256SUMS.txt` defines the release inputs. Developers update the manifest when changing or adding files; CI does not silently repair a mismatch.

Repository files retain raw bytes across Windows and Linux. ZIP ordering, timestamps, and attributes are fixed. Repeated builds are reproducible within the same packaging environment; byte identity across different compression libraries is not guaranteed.

Configuration is distinct from execution evidence. See [v0.5 results](validation-v0.5.en.md), [v0.5.1 results](validation-v0.5.1.md), and [Actions](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml).

## Proposed: operation on AWS

Separate the model worker, gate API, and authoritative database.

- Give the model worker only case-read and proposal-submission permissions.
- Let the gate service commit state, decisions, and execution metadata together.
- Give periodic runs unique IDs and define retry/timeout behavior to prevent unintended duplicate processing.
- Provide run/cost limits, a stop control, and a recovery path for uncertain outcomes.

The current loopback server, fixed keys, and SQLite store are not a public-server deployment. A cloud version requires user authentication, case-level access control, TLS, secret management, database concurrency/durability, and backups. Decide continuous versus scheduled execution and cost after selecting one business integration.

The execution records introduced in v0.4 provide a basis for tracing proposals and decisions in that future design.

## Official references used by the original plan

- [GitHub Actions overview](https://docs.github.com/en/actions/get-started/understand-github-actions)
- [Workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [AWS serverless service selection](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/choosing-aws-serverless-service.html)
- [Scheduled ECS tasks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/tasks-scheduled-eventbridge-scheduler.html)

V1 reuses this workflow with 40 application tests, 3 packaging tests, and the extended UI scenario check. See [V1 validation](validation-v1.md).
