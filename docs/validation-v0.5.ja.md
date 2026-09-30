# v0.5 検証記録

[English](validation-v0.5.en.md) | [日本語](validation-v0.5.ja.md)

作業日：2026年10月1日（日本時間）。対象はM-Anchor Appの検証・配布自動化。正式な研究評価とは別の開発記録である。

## 検証構成

- アプリの34試験：保存・拒否・変更なし、権限、旧版データ、履歴、再起動など。
- 配布処理の3試験：改変されたソースの拒否、ZIP内のバイト保持と不要ファイルの除外、不正・重複パスの拒否。
- UIロジック：実JavaScriptと最小限のDOM代替・実HTTPサーバーを使用。
- チェックサム：梱包対象の全ファイルを照合する。

実モデルの応答は模擬する。有料モデルAPIを呼ばず、APIキーを設定しない。UIの実ブラウザ描画や利用者端末での操作は、このCIの対象に含めない。

## 実行結果

ローカルのLinux/Python 3.12で、アプリ34件・配布処理3件、UIロジック、ソースチェックサムが通過した。元の[検証JSON](observations/ci-v0.5-local/ci-report.json)と[アプリ試験ログ](observations/ci-v0.5-local/app-tests.log)、[配布処理ログ](observations/ci-v0.5-local/release-tests.log)、[UIログ](observations/ci-v0.5-local/ui-logic.log)を保存した。

初回はチェックサム一覧の更新より先に検証を開始し、一覧と変更済みファイルの不一致を検出して失敗した。[初回結果](observations/ci-v0.5-local/initial-ci-report.json)と[失敗ログ](observations/ci-v0.5-local/initial-checksum-failure.log)も残す。一覧を更新した後、全検査が通過した。

GitHub Actionsの[初回実行 #1](https://github.com/iseyan/M-Anchor-App/actions/runs/36743819362)も成功した。対象ソースは `6a986b396fd1cba895e959ddc9982db9054b379b`。GitHub APIから取得した[結果と成果物の記録](observations/2026-10-01-ci-v0.5.json)を保存した。

| 実行環境・処理 | 結果 |
| --- | --- |
| Linux / Python 3.10 | アプリ34件・配布処理3件、UI、チェックサムを通過 |
| Linux / Python 3.13 | 同上 |
| Windows / Python 3.13 | 同上 |
| 配布ジョブ | ZIPの作成・内容照合・Artifactsへの保存が成功 |

CIの結果はランナー上の確認である。利用者のWindows端末のブラウザ描画、実モデルの応答、あらゆる入力への安全性まで検証したものではない。GitHub上のZIPのバイト列は確認者が別途ダウンロードして再照合したものではなく、アップロード前のジョブ内で照合している。記録追加後の実行は、Actionsの一覧から確認できる。

[Actionsの実行一覧](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)

## 変更範囲

app/server.pyのAPP_VERSIONと画面の版表示を0.5へ更新する。Gate、形式核、クライアント、モデル接続、実行記録とデータ形式はv0.4から引き継ぐ。

ZIPはソース配布。実行ファイル化、AWS配備、実モデルの自律的な定期呼出しはこの版には含めない。
