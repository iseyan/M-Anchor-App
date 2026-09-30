# v0.5.1 validation / v0.5.1 検証記録

Work date: October 1, 2026 (Japan time). This release makes English primary while retaining Japanese in the interface and documentation. It is an app-development check, separate from formal research evaluation.

作業日：2026年10月1日（日本時間）。英語を主とし、日本語を併記する画面・資料への更新です。正式な研究評価とは別のアプリ開発上の確認です。

## Change scope / 変更範囲

- English-first headings, decisions, state labels, history, errors, and editable example requests; the page language is English, with Japanese marked on static companion text. / 見出し・判定・状態・履歴・エラー・編集可能な例文を英語優先で併記。ページの主言語を英語とし、静的な補助文に日本語を指定。
- English overview, demonstration, integration, automation, development, and v0.5 validation guides paired with Japanese files. Bilingual README, changelog, and evidence index. / 主要資料に日本語版と対になる英語版を追加し、README・変更履歴・過去の証拠案内を併記。
- Bilingual messages for malformed manual JSON and missing case IDs. / 手動JSONの形式不備と案件ID不足も併記で表示。
- App version 0.5.1; observation schema remains v2. / アプリ版は0.5.1、記録スキーマはv2を継続。

Gate rules, formal core, model bridge, Python client, record implementation, and original observation files are checked against the v0.5 source hashes. Stored proposals and technical reason codes are not translated. The English/Japanese example request is a changed model input; no claim is made that its real-model output is identical to the older Japanese-only request.

Gate・形式核・モデル接続・Pythonクライアント・記録処理・過去の観察ファイルはv0.5のハッシュと照合します。保存された提案原文と理由コードは翻訳しません。併記された例文はモデル入力の変更であり、旧来の日本語のみの依頼と実モデルの出力が同じになるとは主張しません。

## Local results / ローカルの結果

Environment: Linux, Python 3.12.14, Node.js 24.19.0. / 環境：Linux、Python 3.12.14、Node.js 24.19.0。

| Check / 検査 | Result / 結果 | Evidence / 記録 |
| --- | --- | --- |
| Application / アプリ | 34 passed / 34件通過 | [Log](observations/ci-v0.5.1-local/app-tests.log) |
| Packaging / 配布処理 | 3 passed / 3件通過 | [Log](observations/ci-v0.5.1-local/release-tests.log) |
| UI logic / 画面ロジック | Passed / 通過 | [Log](observations/ci-v0.5.1-local/ui-logic.log) |

The UI check runs the actual JavaScript against a minimal DOM substitute and a real local HTTP server. It checks English-first paired labels, automatic connection, explicit case selection, invalid manual JSON, fixed rejection/commit/no-change, a mocked model route, past-entry details, export history, and exclusion of key inputs.

UI確認は実JavaScript・最小限のDOM代替・実HTTPサーバーを使います。英語優先の併記、自動接続、案件選択、手動JSONの形式不備、固定案の三判定、模擬モデル経路、過去履歴、全履歴出力、キー入力値の除外を確認します。

Release packaging also verifies the source manifest and all ZIP entries. HTML nesting, unique IDs, and local documentation links are checked during preparation. The source manifest is updated after documentation is complete; it does not automatically accept mismatched source files.

配布処理ではソース一覧とZIP内の全ファイルを照合します。準備時にHTMLの入れ子、ID重複、資料内リンクも確認します。資料完成後にチェックサム一覧を更新し、不一致のソースを自動的に許容する処理は設けません。

## Hosted CI / GitHub Actions

The existing workflow will verify Linux/Python 3.10 and 3.13, Windows/Python 3.13, and then package successful source. Execution results will be linked here after the code commit runs.

既存のワークフローでLinux/Python 3.10・3.13、Windows/Python 3.13を検証し、成功したソースを梱包します。コードのコミット後に実行結果をここへ記録します。

[Actions runs / 実行一覧](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)

## Limits / 未確認事項

No paid model API is called. Real-model responses to the bilingual prompts, full browser rendering, screen-reader behavior, and the user's Windows browser layout have not been verified by these local checks. CI is runner verification, not a user-device observation. Historical JSON remains evidence only for its original version and scope.

有料モデルAPIは呼び出していません。併記した依頼文への実モデル応答、実ブラウザ描画、読み上げ動作、利用者のWindowsブラウザでのレイアウトは、このローカル確認の範囲外です。CIはランナーでの検証であり、利用者端末での観察とは区別します。過去のJSONは元の版と確認範囲の証拠として保持します。
