# Publication package / 発表用パッケージ

**M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates**

**M-Anchor App V1：プロンプト攻撃による不正な記録更新を無効化する決定論的ゲート**

Prepared on October 1, 2026. App version: **1.0.0**. This is a software demonstration with inspectable observations. A Zenodo record has not been published and no app DOI has been assigned in this preparation task. Distribution licensing remains to be selected by the owner.

2026年10月1日作成。アプリ版は **1.0.0**。検査記録を確認できるソフトウェア実演として発表するための資料です。今回の準備ではZenodoへの公開とアプリのDOI発行は行っていません。配布ライセンスは所有者による選択が残っています。

## The claim / 発表する主張

The app demonstrates a gate that rejects proposals violating configured evidence and update rules, preventing those proposals from changing the authoritative case record. Here, **attack neutralization means blocking an unauthorized record transition at this gate**. It does not mean eliminating the attack text or making a model incapable of producing an incorrect answer.

設定済みの証拠・更新規則に違反する提案を拒否し、その提案による案件正本の変更を止めるGateを実演します。ここでいう **攻撃の無効化は、このGateで不正な記録遷移を成立させないこと** です。攻撃文の消去や、モデルが誤った回答を一切生成しなくなることを意味しません。

## Read and reproduce / 読む・再現する

| Material / 資料 | Use / 用途 |
| --- | --- |
| [Technical note - English](technical-note.en.md) / [技術説明 - 日本語](technical-note.ja.md) | Mechanism, observed results, and limits / 機構・観察結果・限界 |
| [Reproduction guide / 再現手順](reproduce.md) | Six fixed scenarios, result interpretation, optional model run / 固定6例・判定の読み方・任意のモデル実行 |
| [Zenodo description / 掲載文](zenodo-description.md) | English-first description ready to copy / 英語主・日本語併記の転記用文章 |
| [Upload guide / 登録手順](zenodo-upload-guide.md) | Metadata, files, license decision, DOI handling / 登録情報・ファイル・ライセンス選択・DOI |
| [Citation information / 引用情報](../../CITATION.cff) | Existing author spelling, software version, repository / 既存の著者表記・ソフトウェア版・リポジトリ |
| [Original observations / 原観察記録](../observations/2026-10-01-user-check-v1.md) | Exact exports, routes, hashes, and record IDs / 原JSON・経路・ハッシュ・履歴番号 |

The application, gate, and model instructions are unchanged by this preparation. The source ZIP built from this revision adds publication documents and citation metadata to the existing V1 software. Identify the particular ZIP by its SHA256 and accompanying `build-info.json`; app version alone does not distinguish documentation snapshots.

今回の準備でアプリ・Gate・モデル向け指示は変更していません。この版から作成するソースZIPには既存V1と発表資料・引用情報が入ります。資料の改訂を含むZIPの識別には、アプリ版だけでなくSHA256と同梱外の `build-info.json` を使ってください。

## What is not being claimed / 主張しない範囲

No universal attack-blocking rate, proof of model immunity, independent security certification, or business deployment is claimed. The real-model adversarial run preserved uncertainty itself; the stored record does not show the gate rejecting an invalid model-generated proposal. The fixed-proposal tests provide the direct examples of rejection.

あらゆる攻撃に対する阻止率、モデル自体の無敵性、独立したセキュリティ認証、業務導入実績は主張しません。実モデルの攻撃入力例ではモデル自身が未決を保持しており、不正なモデル生成案をGateが拒否した記録ではありません。拒否の直接例は固定提案の検査記録です。
