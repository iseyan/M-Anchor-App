# Zenodo公開準備と登録

[English](zenodo-upload-guide.md)

2026年10月1日作成。この作業ではZenodoの下書き・公開・リリースタグ・アプリDOIを作成していません。所有者がアプリと同梱資料のApache-2.0による配布を選択し、登録用の資料と配布物を整えています。

## 入力する情報

| 項目 | 値 |
| --- | --- |
| 種類 | Software |
| 題名 | 英語で登録する場合は[英語版掲載文](zenodo-description.md)の題名を使用。日本語題名は[日本語版掲載文](zenodo-description.ja.md)を参照 |
| 著者 | Ise（公開名：iseyan） |
| 所属・ORCID | 本人から指定されるまで空欄 |
| 版 | 1.0.0。資料改訂はソースコミットでも識別 |
| 公開日 | 実際に公開する日 |
| 説明 | [作成済み掲載文](zenodo-description.ja.md)を転記 |
| キーワード | prompt injection; prompt attacks; deterministic gate; record integrity; AI agents; evidence admission; candidate preservation; M-Anchor |
| リポジトリ | https://github.com/iseyan/M-Anchor-App |
| 言語 | Python。画面にはJavaScriptも使用 |
| ライセンス | **Apache License 2.0（Apache-2.0）**。[本文](../../LICENSE)を同梱 |
| DOI | アプリ固有の既存DOIがなければ新規取得 |

著者表記はフレームワークの既存引用情報に合わせています。同フレームワークのDOI `10.5281/zenodo.22918471` は別記録のもので、アプリのDOIではありません。関連プロジェクトとしてリンクし、その評価版アーカイブが同梱コード全バイトの直接の出所だとは断定しません。

## ファイル

- `scripts/build_release.py` で作成した **ソースZIPを一つ** アップロードします。アプリソース・英日手順・引用情報・発表文・原観察記録を含みます。
- ZIPのSHA256ファイルと `build-info.json` を添付します。技術説明PDFは英語版 `m-anchor-app-v1-publication-note.en.pdf` と日本語版 `m-anchor-app-v1-publication-note.ja.pdf` を、圧縮せず個別に添付できます。
- 旧V1と今回の資料改訂ZIPは同じアプリ1.0.0でもハッシュが違うため、対象を明記します。

ZenodoのSoftware Heritage手動保存経路では圧縮ソースファイルを一つにします。CIのArtifactsは保持期間で失効するため恒久的アーカイブではありません。公開後に実際の保存状態を確認します。[資料1、4]

## 最終設定と公開

1. **ZenodoでApache License 2.0を選びます。** LICENSE・NOTICEを同梱し、`CITATION.cff` に `Apache-2.0` を指定しています。初期値のCC-BY 4.0ではなく、アプリと同梱資料の配布条件に合わせてください。別プロジェクトであるフレームワークのライセンスやDOIは変更しません。
2. 新規アップロードでSoftwareを選び、ファイル・題名・説明を入力します。
3. 必要ならDOIを予約し、実際に割り当てられたアプリDOIを記載します。予約は公開と異なります。内容が変わればZIPを再作成して下書きを差し替えます。
4. 著者・権利・ハッシュ・適用範囲・版を確認して公開し、版固有のDOIとURLをリポジトリに残します。

後でGitHubから自動保存する場合は、リリース作成前にZenodoでリポジトリを有効にします。引用情報にはApache-2.0を指定し、未発行のアプリDOIは省いています。保存後に実際のアプリDOIを引用情報へ記録してください。今回の準備で別形式のZenodo JSONは不要です。[資料4、5]

## 公式資料

2026年10月1日確認：

1. [ソフトウェアの手動アップロード](https://help.zenodo.org/docs/github/archive-software/manual-upload/)
2. [ライセンスと権利](https://help.zenodo.org/docs/deposit/describe-records/licenses/)
3. [DOIの予約](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
4. [GitHubリリースの保存](https://help.zenodo.org/docs/github/archive-software/github-upload/)
5. [CITATION.cffによる引用情報](https://help.zenodo.org/docs/github/describe-software/citation-file/)
