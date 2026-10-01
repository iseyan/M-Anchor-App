# Zenodo preparation and upload / Zenodo公開準備と登録

Prepared October 1, 2026. No Zenodo draft, publication, release tag, or app DOI was created in this task. The owner has selected Apache-2.0 for the app and included project materials; the package is prepared for deposit.

2026年10月1日作成。この作業ではZenodoの下書き・公開・リリースタグ・アプリDOIを作成していません。所有者がアプリと同梱資料のApache-2.0による配布を選択し、登録用の資料と配布物を整えています。

## Metadata / 入力する情報

| Field / 項目 | Value / 値 |
| --- | --- |
| Resource type / 種類 | Software |
| Title / 題名 | M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates |
| Creator / 著者 | Ise; public alias / 公開名: iseyan |
| Affiliation and ORCID / 所属・ORCID | Omit unless supplied by the author / 本人から指定されるまで空欄 |
| Version / 版 | 1.0.0; identify the documentation snapshot by source commit / 資料改訂はソースコミットでも識別 |
| Publication date / 公開日 | Actual deposit publication date / 実際に公開する日 |
| Description / 説明 | Copy [the prepared description](zenodo-description.md) / 作成済み掲載文を転記 |
| Keywords / キーワード | prompt injection; prompt attacks; deterministic gate; record integrity; AI agents; evidence admission; candidate preservation; M-Anchor |
| Repository / リポジトリ | https://github.com/iseyan/M-Anchor-App |
| Programming language / 言語 | Python; JavaScript for the interface / 画面にはJavaScriptも使用 |
| License / ライセンス | **Apache License 2.0 (Apache-2.0)**; see [LICENSE](../../LICENSE) / 本文を同梱 |
| DOI | Obtain a new app DOI unless an app-specific DOI already exists / アプリ固有の既存DOIがなければ新規取得 |

The author spelling follows the framework's existing `CITATION.cff`. Its DOI `10.5281/zenodo.22918471` belongs to a different record, not this app. Link the framework as a related project without asserting that its archived evaluation release is the exact source of every vendored byte.

著者表記はフレームワークの既存引用情報に合わせています。同フレームワークのDOIは別記録のもので、アプリのDOIではありません。関連プロジェクトとしてリンクし、その評価版アーカイブが同梱コード全バイトの直接の出所だとは断定しません。

## Files / ファイル

- Upload **one source ZIP** built by `scripts/build_release.py`. It contains Python source, English/Japanese instructions, citation metadata, publication text, and original observations. / 同スクリプトで作成した **ソースZIPを一つ** アップロードします。アプリソース・英日手順・引用情報・発表文・原観察記録を含みます。
- Add the ZIP SHA256 file and `build-info.json`. An English/Japanese briefing PDF may be a separate uncompressed attachment. / SHA256ファイルと作成記録を添付します。説明用英日PDFは圧縮せず別添付にできます。
- The old V1 ZIP and this documentation snapshot share app version 1.0.0 but have different package hashes. Identify the chosen snapshot explicitly. / 旧V1と今回の資料改訂ZIPは同じアプリ1.0.0でもハッシュが違うため、対象を明記します。

Zenodo's Software Heritage manual archival route requires a single compressed source file. CI artifacts expire after the configured retention period and are not a permanent archive. Check actual archival status after publication. [Sources 1, 4]

ZenodoのSoftware Heritage手動保存経路では圧縮ソースファイルを一つにします。CIのArtifactsは保持期間で失効するため恒久的アーカイブではありません。公開後に実際の保存状態を確認します。[資料1、4]

## Finalize and publish / 最終設定と公開

1. **Select Apache License 2.0 in Zenodo.** LICENSE and NOTICE are included, and `CITATION.cff` declares `Apache-2.0`. Use these terms for this app distribution and its project materials instead of the form's default CC-BY 4.0. The linked framework repository is a separate project; do not change its license or DOI through this deposit. [Source 2] / **ZenodoでApache License 2.0を選びます。** LICENSE・NOTICEを同梱し、引用情報に `Apache-2.0` を指定しています。初期値のCC-BY 4.0ではなく、アプリと同梱資料の配布条件に合わせてください。別プロジェクトであるフレームワークのライセンスやDOIは変更しません。
2. Create a new upload, select **Software**, add the files, and paste the prepared title and description. / 新規アップロードでSoftwareを選び、ファイル・題名・説明を入力します。
3. Reserve a DOI if needed in the files before publication. Reservation is not publication. Add only the actually assigned app DOI to citation metadata; rebuild and replace the draft ZIP if its contents changed. Do not invent a DOI or reuse the framework DOI. [Source 3] / 必要ならDOIを予約し、実際に割り当てられたアプリDOIを記載します。予約は公開と異なります。内容が変わればZIPを再作成して下書きを差し替えます。
4. Review creators, rights, hashes, scope, and version, then publish. Retain the record's version DOI and URL in the repository. / 著者・権利・ハッシュ・適用範囲・版を確認して公開し、版固有のDOIとURLをリポジトリに残します。

For later automatic GitHub archiving, enable the repository in Zenodo before creating the intended release. The `CITATION.cff` supplies citation fields and Apache-2.0 licensing, and omits the unassigned app DOI. After archiving, record the actual app DOI in the citation metadata. A separate Zenodo JSON metadata file is unnecessary for this preparation. [Sources 4, 5]

後でGitHubから自動保存する場合は、リリース作成前にZenodoでリポジトリを有効にします。引用情報にはApache-2.0を指定し、未発行のアプリDOIは省いています。保存後に実際のアプリDOIを引用情報へ記録してください。今回の準備で別形式のZenodo JSONは不要です。[資料4、5]

## Official instructions / 公式資料

Checked October 1, 2026 / 2026年10月1日確認：

1. [Upload software manually](https://help.zenodo.org/docs/github/archive-software/manual-upload/)
2. [Licenses and rights](https://help.zenodo.org/docs/deposit/describe-records/licenses/)
3. [Reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
4. [Archive a release from GitHub](https://help.zenodo.org/docs/github/archive-software/github-upload/)
5. [CITATION.cff](https://help.zenodo.org/docs/github/describe-software/citation-file/)
