# Zenodo preparation and upload

[日本語](zenodo-upload-guide.ja.md)

Prepared October 1, 2026. No Zenodo draft, publication, release tag, or app DOI was created in this task. The owner has selected Apache-2.0 for the app and included project materials; the package is prepared for deposit.

## Metadata

| Field | Value |
| --- | --- |
| Resource type | Software |
| Title | M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates |
| Creator | Ise; public alias: iseyan |
| Affiliation and ORCID | Omit unless supplied by the author |
| Version | 1.0.0; identify the documentation snapshot by source commit |
| Publication date | Actual deposit publication date |
| Description | Copy [the prepared description](zenodo-description.md) |
| Keywords | prompt injection; prompt attacks; deterministic gate; record integrity; AI agents; evidence admission; candidate preservation; M-Anchor |
| Repository | https://github.com/iseyan/M-Anchor-App |
| Programming language | Python; JavaScript for the interface |
| License | **Apache License 2.0 (Apache-2.0)**; see [LICENSE](../../LICENSE) |
| DOI | Obtain a new app DOI unless an app-specific DOI already exists |

The author spelling follows the framework's existing `CITATION.cff`. Its DOI `10.5281/zenodo.22918471` belongs to a different record, not this app. Link the framework as a related project without asserting that its archived evaluation release is the exact source of every vendored byte.

## Files

- Upload **one source ZIP** built by `scripts/build_release.py`. It contains Python source, English/Japanese instructions, citation metadata, publication text, and original observations.
- Add the ZIP SHA256 file and `build-info.json`. Attach the English briefing `m-anchor-app-v1-publication-note.en.pdf` and Japanese briefing `m-anchor-app-v1-publication-note.ja.pdf` as separate uncompressed files.
- The old V1 ZIP and this documentation snapshot share app version 1.0.0 but have different package hashes. Identify the chosen snapshot explicitly.

Zenodo's Software Heritage manual archival route requires a single compressed source file. CI artifacts expire after the configured retention period and are not a permanent archive. Check actual archival status after publication. [Sources 1, 4]

## Finalize and publish

1. **Select Apache License 2.0 in Zenodo.** LICENSE and NOTICE are included, and `CITATION.cff` declares `Apache-2.0`. Use these terms for this app distribution and its project materials instead of the form's default CC-BY 4.0. The linked framework repository is a separate project; do not change its license or DOI through this deposit. [Source 2]
2. Create a new upload, select **Software**, add the files, and paste the prepared title and description.
3. Reserve a DOI if needed in the files before publication. Reservation is not publication. Add only the actually assigned app DOI to citation metadata; rebuild and replace the draft ZIP if its contents changed. Do not invent a DOI or reuse the framework DOI. [Source 3]
4. Review creators, rights, hashes, scope, and version, then publish. Retain the record's version DOI and URL in the repository.

For later automatic GitHub archiving, enable the repository in Zenodo before creating the intended release. The `CITATION.cff` supplies citation fields and Apache-2.0 licensing, and omits the unassigned app DOI. After archiving, record the actual app DOI in the citation metadata. A separate Zenodo JSON metadata file is unnecessary for this preparation. [Sources 4, 5]

## Official instructions

Checked October 1, 2026

1. [Upload software manually](https://help.zenodo.org/docs/github/archive-software/manual-upload/)
2. [Licenses and rights](https://help.zenodo.org/docs/deposit/describe-records/licenses/)
3. [Reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
4. [Archive a release from GitHub](https://help.zenodo.org/docs/github/archive-software/github-upload/)
5. [CITATION.cff](https://help.zenodo.org/docs/github/describe-software/citation-file/)
