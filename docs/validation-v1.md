# V1 validation / V1検証記録

Version: 1.0.0. Work date: October 1, 2026 (Japan time). This is a local record-protection release, separate from formal research evaluation.

版：1.0.0。作業日：2026年10月1日（日本時間）。ローカルの記録保護アプリの検証であり、正式な研究評価とは別に扱います。

## What changed / 変更内容

Four synthetic attack scenarios and two controls were added through an admin-only catalog/run API. The model route optionally accepts a scenario ID and saves exact input text plus SHA256 in `execution.exercise`. The existing one-use ticket binds that observation to case and proposal bytes. Input, proposal source, gate decision, and independent readback are shown together in the bilingual interface.

管理用の一覧・実行APIを通じ、人工的な攻撃4種類と対照2種類を追加しました。モデル経路は任意のシナリオIDを受け付け、入力原文とSHA256を `execution.exercise` に保存します。一回限りのチケットで案件と提案原文に結び付け、画面は入力・提案の経路・Gate判定・独立した再読込を英日併記で示します。

Gate rules, formal core, provider-request implementation, and Python client remain byte-identical to v0.5.1. Exercise metadata does not grant authority. The observation schema remains v2 with optional fields, and the SQLite layout is unchanged. Missing historical inputs remain missing.

Gate規則・形式核・提供元への要求処理・Pythonクライアントはv0.5.1と同一バイト列です。演習情報は権限を与えません。出力は任意項目を加えたv2を継続し、SQLite構成は共通です。過去に残していない入力を補完しません。

## Local checks / ローカル検査

Environment: Linux, Python 3.12.14, Node.js 24.19.0. All model outputs in these tests are mocks. No API key is required and no paid model API is called.

環境：Linux、Python 3.12.14、Node.js 24.19.0。試験のモデル応答はすべて模擬です。APIキーは不要で、有料APIは呼び出していません。

| Check / 検査 | Result / 結果 | Evidence / 記録 |
| --- | --- | --- |
| Application / アプリ | 40 passed / 40件通過 | [Log](observations/ci-v1-local/app-tests.log) |
| Packaging / 配布処理 | 3 passed / 3件通過 | [Log](observations/ci-v1-local/release-tests.log) |
| UI logic / 画面ロジック | Passed / 通過 | [Log](observations/ci-v1-local/ui-logic.log) |

The six added application checks cover admin-only scenario routes and strict payloads; preservation of full state/evidence authority for all four attacks; positive and no-change controls; exact input/proposal linkage through a real server restart; invalid scenario/case rejection before model generation; and rollback when exercise recording fails. The existing ticket check also verifies that later mutation of the source exercise object does not change its bound copy.

追加した6件は、管理用経路と厳格な入力、攻撃4種類での全状態・証拠認可の保持、正当更新・変更なしの対照、実サーバー再起動後の入力と提案の対応、不正なシナリオ・案件指定の生成前拒否、演習記録に失敗した場合のロールバックを確認します。既存のチケット試験では、元の演習オブジェクトを後から変更しても保存用の複製に影響しないことも確認します。

The UI check executes the actual JavaScript with a minimal DOM substitute and real local HTTP. It covers all six fixed scenarios, mocked model input, past-entry switching, JSON export, key-field exclusion, and an API failure displayed as unverified without adding a false rejection entry. Raw input is displayed using textContent, not inserted as HTML.

UI確認は実JavaScript・最小限のDOM代替・実HTTPを用い、固定シナリオ6種類、模擬モデル入力、過去履歴の切替え、JSON出力、キー欄の除外、API失敗を未確認と表示して偽の拒否履歴を作らないことを確認します。入力原文はHTMLとして挿入せず、textContentで表示します。

Packaging tests use a small synthetic fixture version; actual V1 packaging separately checks every source-manifest hash and ZIP entry. HTML nesting, unique IDs, and local documentation links are also inspected during preparation.

配布処理の試験は小さな人工的な版の素材を使い、V1の実際の梱包では別途ソース一覧の全ハッシュとZIP内の全項目を照合します。準備時にHTML構造、ID重複、資料内リンクも確認します。

## Hosted checks / GitHub Actions

[Run #5](https://github.com/iseyan/M-Anchor-App/actions/runs/36791415008) succeeded for source commit `8c5f7c86fe78067c43b01b3c05e3ef28a11fa470`. All three verification environments and the packaging job completed successfully. The [API receipt](observations/2026-10-01-ci-v1.json) records jobs and artifacts.

[実行 #5](https://github.com/iseyan/M-Anchor-App/actions/runs/36791415008)はコミット `8c5f7c86fe78067c43b01b3c05e3ef28a11fa470` で成功しました。三つの検証環境と配布ジョブがすべて成功し、[API受領記録](observations/2026-10-01-ci-v1.json)に結果と成果物を保存しました。

| Environment / 環境 | Result / 結果 |
| --- | --- |
| Linux / Python 3.10 | 40 app tests, 3 packaging tests, UI logic and checksums passed / 40件・3件・UI・チェックサム通過 |
| Linux / Python 3.13 | Same checks passed / 同上 |
| Windows / Python 3.13 | Same checks passed / 同上 |
| Packaging / 配布 | ZIP built, verified and uploaded / ZIP作成・照合・保存に成功 |

The ZIP is verified inside the packaging job before upload. The reviewer did not independently download the uploaded artifact. A later documentation commit triggers another run, shown in Actions.

ZIPは配布ジョブ内でアップロード前に照合しています。確認者がアップロード後の成果物を独立してダウンロードしたものではありません。記録追加後のコミットも別の実行を起こし、Actionsで確認できます。

[Actions runs / 実行一覧](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml)

## User observation received later / 後から受領した利用者側の観察

The [October 1 user observation](observations/2026-10-01-user-check-v1.md) retains a cumulative 20-entry export: 18 fixed proposals and two model-route no-change results. Exact input/proposal correspondence, state hashes, history continuity, and readbacks matched. The HOLD model output preserved uncertainty; UPDATE was already Version 2. A model-generated Version 1→2 commit is still unobserved in that export. These user observations are separate from the mocked automated checks above.

[10月1日の利用者側観察](observations/2026-10-01-user-check-v1.md)に、固定18件・モデル経由の変更なし2件を含む累積20件の出力を保持した。入力・提案・状態ハッシュ・履歴のつながり・再読込が一致した。HOLDではモデル出力が未決を保持し、UPDATEは実行前からVersion 2だった。この出力ではモデル生成案によるVersion 1→2の保存は未確認である。利用者側の観察と、上記の模擬モデルによる自動検査を区別する。

## What these automated results do not establish / 自動検査の確認範囲の限界

Fixed proposals test the gate even when the proposed update is invalid; they do not test model resistance. Mocked model calls test application integration, not live-model robustness. No attack detection rate, universal jailbreak protection, external-tool control, or indirect-injection integration is claimed. Full browser rendering and operation of V1 on the user's device remain unverified by these automated checks.

固定提案は不正な更新案に対するGateを試すもので、モデルの耐性は試していません。模擬モデルは接続処理を検査し、実モデルの堅牢性を評価しません。攻撃検出率、万能なジェイルブレイク防止、外部ツールの制御、間接インジェクションの接続検証は主張しません。実ブラウザ描画と利用者端末でのV1操作は、この自動検査の確認範囲外です。

V1 records inputs that reach the gate through the model route. An API error before proposal submission is shown on screen but has no gate-history entry. Key input fields are excluded; secrets pasted into request/proposal text would still be recorded. See [V1 guide](v1-guide.md).

V1はモデル経路でGateまで届いた提案の入力を記録します。提案前のAPIエラーは画面に表示しますが、Gateの履歴はありません。キー入力欄は除外し、依頼文・提案文へ貼り付けた秘密情報は記録されます。[V1手順](v1-guide.md)を参照してください。
