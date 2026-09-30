# 開発の自動化とAWS接続の計画

記録日：2026年10月1日（日本時間）。利用者からのGitHub Actions・AWS活用の質問を、今後の設計として整理する。以下は未実装の計画であり、v0.4の動作確認に含めない。

## 二つの自動化

| 対象 | 担当する仕組み | M-Anchorで行う処理 |
| --- | --- | --- |
| 開発・検証・配布 | GitHub Actions | 更新後のテスト、配布物の作成、検証ログの保存 |
| アプリの運用 | AWSなどの実行基盤 | 案件の定期取得、モデルへの提案依頼、Gateへの提出、結果保存 |

GitHub Actionsは、リポジトリのイベントや手動操作・スケジュールを起点にジョブを実行できる。AWSのFargateは継続稼働するコンテナの選択肢となり、EventBridge SchedulerはECSタスクを定期起動できる。両者は組み合わせられる。

## 次の小さな実装単位

まず、APIキーを使わない自動テストと配布ZIPの作成をGitHub Actionsで動かす。LinuxとWindowsでPythonのテストを実行し、通過したソースからZIPとチェックサムを作り、検証ログと共に成果物にする。実モデルの定期呼出しはこの段階には含めない。

v0.4にはローカル用の `scripts/build_release.py` を用意した。チェックサムで確認したファイルだけを梱包するため、この処理をCIから再利用できる。

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
