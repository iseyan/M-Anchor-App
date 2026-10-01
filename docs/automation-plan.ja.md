# 開発の自動化とAWS接続の計画

[English](automation-plan.en.md)

記録日：2026年10月1日（日本時間）。利用者からのGitHub Actions・AWS活用の質問を、今後の設計として整理する。当初は未実装の計画として記載した。v0.5では開発の自動化を実装し、AWSでの運用は引き続き計画として分ける。

## 二つの自動化

| 対象 | 担当する仕組み | M-Anchorで行う処理 |
| --- | --- | --- |
| 開発・検証・配布 | GitHub Actions | 更新後のテスト、配布物の作成、検証ログの保存 |
| アプリの運用 | AWSなどの実行基盤 | 案件の定期取得、モデルへの提案依頼、Gateへの提出、結果保存 |

GitHub Actionsは、リポジトリのイベントや手動操作・スケジュールを起点にジョブを実行できる。AWSのFargateは継続稼働するコンテナの選択肢となり、EventBridge SchedulerはECSタスクを定期起動できる。両者は組み合わせられる。

## v0.5：検証・梱包の自動化

`Verify and package` ワークフローを追加した。mainへのpush、pull request、手動実行を起点とする。

| 処理 | 構成 |
| --- | --- |
| 検証環境 | Linux/Python 3.10・3.13、Windows/Python 3.13、Node.js 24 |
| 検証 | アプリの34試験、配布処理の3試験、UIロジック、ソースチェックサム |
| 失敗時 | 配布ジョブを開始せず、得られたログを保存 |
| 配布時 | 全環境の成功後、同じソースコミットからZIPを作成して内容を照合 |
| 提出変更の扱い | pull requestでは検証のみ。pushと手動実行でZIPを作成 |
| 記録 | 環境・実行ID・コミット・各検査結果をJSONに残す |
| 保持 | Artifactsを14日間保存 |

ワークフローのリポジトリ権限はcontentsの読取りのみ。外部Actionは取得時点の公式リリースのコミットSHAへ固定し、checkout後の認証情報保持を無効にする。APIキーなどの追加Secretsは要求しない。モデルの応答は試験用に置き換える。

`scripts/ci.py` と `scripts/build_release.py` はローカルでも同じ処理を実行する。`SHA256SUMS.txt` が梱包対象を定める。ファイルを変更・追加した開発者は、対象一覧とチェックサムを合わせて更新する。CIが不一致を自動修復して通す処理は設けない。

Windowsの自動改行変換でハッシュが変わらないよう、リポジトリはファイルを生バイトで保持する。配布用ZIPのファイル順・時刻・属性は固定する。同じ梱包環境では同じ入力から同じZIPを生成できるが、異なる圧縮ライブラリ間のバイト一致までは保証しない。

設定と実際の実行結果は区別する。実行結果は[検証記録](validation-v0.5.ja.md)と[Actions](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)から確認する。

## AWSで継続運用する場合

構成案は、モデルへ提案を依頼する処理、Gateを実行するAPI、正本を保存するDBを分離するものとする。

- モデル側の処理には、対象案件の読取りと提案提出の権限だけを渡す。
- Gate側のサービスが正本の更新を担い、判定・実行情報と同じトランザクションで保存する。
- 定期実行には一意の実行IDを設け、再送・タイムアウトで同じ処理が重複しない方式を作る。
- 実行回数・費用の上限、停止操作、障害時の確認経路を画面に用意する。

現行のHTTPサーバー・固定キー・ローカルSQLiteをそのまま公開サーバーとして配備する計画ではない。クラウド化する段階で、利用者認証、案件ごとのアクセス権、TLS、秘密情報管理、DBの排他・永続化・バックアップを実装する。企業接続先と運用頻度が決まった段階で、常時稼働と定期起動のどちらを採用するか、費用と一緒に判断する。

v0.4の実行記録は、この設計で各処理の提案と判定を追えるようにするための基礎となる。

## 参照した公式資料

- [GitHub Actionsの概要](https://docs.github.com/en/actions/get-started/understand-github-actions)
- [ワークフローの起動イベント](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [AWSのサーバーレスサービス選定](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/choosing-aws-serverless-service.html)
- [EventBridge SchedulerからECSタスクを起動](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/tasks-scheduled-eventbridge-scheduler.html)

V1は同じワークフローでアプリ40件、配布処理3件、拡張したUIシナリオを確認する。[V1検証](validation-v1.ja.md)を参照。
