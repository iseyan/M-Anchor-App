# 過去の記録の案内

[English](evidence-guide.md)

過去の日本語の計画・観察記録を案内します。各文書の英語版は別ファイルで用意しています。原ファイルとJSONは受領時の形式で保持します。要約によって、元資料にない証拠を補うことはありません。

| 記録 | 確認できること | 限界 |
| --- | --- | --- |
| [2026年9月30日の原計画](../plans/m-anchor-app-plan-2026-09-30.ja.md) | 専用Pythonクライアント、案件更新、外部Gate、小さな配布版の方針。 | 計画であり検証結果ではない。 |
| [v0.3ローカル検証](validation-v0.3.ja.md) | Linuxで25件とUIロジックを通過。 | DOM代替であり実ブラウザ描画ではない。 |
| [v0.3利用者側の履歴](observations/2026-10-01-user-check-v0.3.ja.md) | 変更なし・保存・拒否の一覧を受領。 | 一覧だけでは完全な実行来歴は確認できない。 |
| [v0.3出力の受領記録](observations/2026-10-01-export-receipt-v0.3.ja.md) | 状態ハッシュ、保持、正当更新、直近提案の対応を確認。 | 履歴1・2のモデル情報は含まれない。 |
| [v0.4ローカル検証](validation-v0.4.ja.md) | 再起動・移行・ロールバック・100件超出力を含む34件とUI確認。 | モデル応答は模擬。 |
| [v0.4出力の受領と再実演](observations/2026-10-01-export-receipt-v0.4.ja.md) | 固定案三判定、原文・ハッシュ・再読込と別データでの再実演。 | 別データは同一ストアの再起動の証拠ではなく、実モデルは使用していない。 |
| [V1利用者側の観察](observations/2026-10-01-user-check-v1.ja.md) | 固定18件・モデル経由の変更なし2件、入力・提案・ハッシュ・再読込の対応を確認。 | モデルがHOLDの未決を保持し、UPDATEは更新済み。モデル生成案による新規保存は未確認。 |
| [V1モデル保存の追記](observations/2026-10-01-user-check-v1.ja.md) | 別出力のモデル経由1件で、認可済みe_BによるVersion 1→2の保存と再読込一致を確認。 | 両出力の表示は `data`であり、ディレクトリの同一性や起動・初期化方法は未確認。 |

元JSON：

- [v0.3出力](observations/records/m-anchor-app-record-2026-09-30T15-21-20-696Z.json) — SHA256 `c9e660b47877436077f134fbf6fe38a61d49e82630854a12da309686ebd26ab8`
- [v0.4出力](observations/records/m-anchor-app-record-2026-09-30T15-54-38-638Z.json) — SHA256 `6da483dcd78aca642ccec25418f6bde5695016a7e0cd59a40b8b64706cd54917`
- [v0.4新規デモの出力](observations/records/m-anchor-app-record-2026-09-30T16-07-47-577Z.json) — SHA256 `cf47d468693c56b6eaf747b7bb93e0cb92dcdab9546e88e26bfab96fceaf14a5`

- [V1累積出力20件](observations/records/m-anchor-app-record-2026-10-01T01-01-50-675Z.json) — SHA256 `098377b4761f2d118e5fdb46ebd1e7550bfa15a13493c1aa706f11b13e1692d8`

- [V1モデル保存出力1件](observations/records/m-anchor-app-record-2026-10-01T01-22-01-406Z.json) — SHA256 `c3f0f0adbe7f8374c4587a47121a3ee271636f26177c87b7b10c34587a3fd3b6`

受領記録には日本時間、JSONにはUTCを使います。アプリの観察は正式な研究評価を代替しません。
