# Publication package

[日本語](README.ja.md)

**M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates**

Prepared on October 1, 2026. App version: **1.0.0**. This is a software demonstration with inspectable observations. A Zenodo record has not been published and no app DOI has been assigned in this preparation task. The owner has selected **Apache-2.0** for this distribution, including its project documentation and observations. See [LICENSE](../../LICENSE) and [NOTICE](../../NOTICE).

## The claim

The app demonstrates a gate that rejects proposals violating configured evidence and update rules, preventing those proposals from changing the authoritative case record. Here, **attack neutralization means blocking an unauthorized record transition at this gate**. It does not mean eliminating the attack text or making a model incapable of producing an incorrect answer.

## Read and reproduce

| Material | Use |
| --- | --- |
| [Technical note - English](technical-note.en.md) | Mechanism, observed results, and limits |
| [Reproduction guide](reproduce.md) | Six fixed scenarios, result interpretation, optional model run |
| [Zenodo description](zenodo-description.md) | English description ready to copy |
| [Upload guide](zenodo-upload-guide.md) | Metadata, files, Apache-2.0, DOI handling |
| [Citation information](../../CITATION.cff) | Existing author spelling, software version, repository |
| [Original observations](../observations/2026-10-01-user-check-v1.md) | Exact exports, routes, hashes, and record IDs |

The application, gate, and model instructions are unchanged by this preparation. The source ZIP built from this revision adds publication documents and citation metadata to the existing V1 software. Identify the particular ZIP by its SHA256 and accompanying `build-info.json`; app version alone does not distinguish documentation snapshots.

## What is not being claimed

No universal attack-blocking rate, proof of model immunity, independent security certification, or business deployment is claimed. The real-model adversarial run preserved uncertainty itself; the stored record does not show the gate rejecting an invalid model-generated proposal. The fixed-proposal tests provide the direct examples of rejection.
