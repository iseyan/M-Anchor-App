# Evidence guide / 過去の記録の案内

This English-first index explains earlier Japanese planning and observation records. Original files and JSON bytes are retained as received. A summary does not add evidence that was absent from the source.

過去の日本語の計画・観察記録を英語優先で案内します。原ファイルとJSONは受領時の形式で保持します。要約によって、元資料にない証拠を補うことはありません。

| Record / 記録 | What it supports / 確認できること | Limits / 限界 |
| --- | --- | --- |
| [Original plan, 2026-09-30](../plans/m-anchor-app-plan-2026-09-30.ja.md) | One Python client, case-record updates, external gate, and a small distribution. / 専用Pythonクライアント、案件更新、外部Gate、小さな配布版の方針。 | A dated plan, not a test result. / 計画であり検証結果ではない。 |
| [v0.3 local validation](validation-v0.3.ja.md) | 25 app tests and UI logic passed on Linux/Python 3.12. / Linuxで25件とUIロジックを通過。 | DOM substitute, not browser rendering. / DOM代替であり実ブラウザ描画ではない。 |
| [v0.3 user history](observations/2026-10-01-user-check-v0.3.ja.md) | Reported HOLD/no change, UPDATE/saved, HOLD/rejected. / 変更なし・保存・拒否の一覧を受領。 | A table does not establish complete execution provenance. / 一覧だけでは完全な実行来歴は確認できない。 |
| [v0.3 export receipt](observations/2026-10-01-export-receipt-v0.3.ja.md) | State hashes, retained state, a supported update, and the latest proposal matched. / 状態ハッシュ、保持、正当更新、直近提案の対応を確認。 | Model metadata for entries 1–2 was absent. / 履歴1・2のモデル情報は含まれない。 |
| [v0.4 local validation](validation-v0.4.ja.md) | 34 tests: restart, migration, rollback, full export beyond 100 entries; UI logic. / 再起動・移行・ロールバック・100件超出力を含む34件とUI確認。 | Mocked models; not a paid API run. / モデル応答は模擬。 |
| [v0.4 export receipt and repeat demo](observations/2026-10-01-export-receipt-v0.4.ja.md) | Fixed Rejected → Saved → No change runs, proposal/hash correspondence, readbacks, and reproduction in separate data. / 固定案三判定、原文・ハッシュ・再読込と別データでの再実演。 | Separate data is not proof of restarting the same store; no model API was used. / 別データは同一ストアの再起動の証拠ではなく、実モデルは使用していない。 |
| [V1 user observation](observations/2026-10-01-user-check-v1.md) | 18 fixed runs and two model-route no-change results; exact input/proposal linkage, hashes and readbacks matched. / 固定18件・モデル経由の変更なし2件、入力・提案・ハッシュ・再読込の対応を確認。 | The model kept HOLD unresolved; UPDATE was already Version 2. A new model-generated commit remains unobserved in this export. / モデルがHOLDの未決を保持し、UPDATEは更新済み。モデル生成案による新規保存は未確認。 |
| [V1 model commit follow-up](observations/2026-10-01-user-check-v1.md) | A separate model-route entry saved UPDATE from Version 1 to 2, using admitted e_B, with matched readback. / 別出力のモデル経由1件で、認可済みe_BによるVersion 1→2の保存と再読込一致を確認。 | Both exports say `data`; directory identity and launch/reset method are not established. / 両出力の表示はdataであり、ディレクトリの同一性や起動・初期化方法は未確認。 |

Raw exports / 元JSON：

- [v0.3 export](observations/records/m-anchor-app-record-2026-09-30T15-21-20-696Z.json) — SHA256 `c9e660b47877436077f134fbf6fe38a61d49e82630854a12da309686ebd26ab8`
- [v0.4 export](observations/records/m-anchor-app-record-2026-09-30T15-54-38-638Z.json) — SHA256 `6da483dcd78aca642ccec25418f6bde5695016a7e0cd59a40b8b64706cd54917`
- [v0.4 fresh-demo export](observations/records/m-anchor-app-record-2026-09-30T16-07-47-577Z.json) — SHA256 `cf47d468693c56b6eaf747b7bb93e0cb92dcdab9546e88e26bfab96fceaf14a5`
- [V1 cumulative export, 20 entries / V1累積出力20件](observations/records/m-anchor-app-record-2026-10-01T01-01-50-675Z.json) — SHA256 `098377b4761f2d118e5fdb46ebd1e7550bfa15a13493c1aa706f11b13e1692d8`
- [V1 model commit export, one entry / V1モデル保存出力1件](observations/records/m-anchor-app-record-2026-10-01T01-22-01-406Z.json) — SHA256 `c3f0f0adbe7f8374c4587a47121a3ee271636f26177c87b7b10c34587a3fd3b6`

Receipt times may be expressed in Japan time; JSON timestamps use UTC. App observations do not replace formal research evaluation. / 受領記録には日本時間、JSONにはUTCを使います。アプリの観察は正式な研究評価を代替しません。
