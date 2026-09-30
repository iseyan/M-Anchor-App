# M-Anchor App

Check AI-generated record updates before committing them to an authoritative store. This local prototype preserves unresolved candidates unless admitted evidence and deterministic update rules support a change.

AIの記録更新案を正本への保存前に検査するローカル試作版です。認可済み証拠と更新規則が変更を支持しない限り、未決の候補を保持します。

**Model proposes; deterministic layer commits.**  
**モデルは提案し、決定論的な層が保存を確定する。**

## Current version / 現在の版

**v0.5.1 — English-first bilingual interface and documentation.** English appears first in the app, including decisions, history, errors, and example requests. Japanese remains alongside it. API field names, stored proposals, and historical evidence retain their original format. GitHub Actions verifies Linux and Windows builds and creates the source ZIP.

**v0.5.1 — 英語を主とする英日併記版。** 画面・判定・履歴・エラー・依頼文の例は英語を先に、日本語を併記します。API項目名・保存された提案・過去の証拠記録は原形式を保持します。Linux・Windowsの検証とソースZIPの作成はGitHub Actionsで実行します。

| Documentation / 資料 | English | 日本語 |
| --- | --- | --- |
| Purpose and scope / 概要と適用範囲 | [Overview](docs/overview.en.md) | [概要](docs/overview.ja.md) |
| Demonstration / 実演 | [Demo guide](docs/demo-guide.en.md) | [デモ手順](docs/demo-guide.ja.md) |
| Python client, API, records / 接続と記録 | [Integration](docs/integration.en.md) | [接続仕様](docs/integration.ja.md) |
| Automation and future AWS work / 自動化とAWS計画 | [Automation plan](docs/automation-plan.en.md) | [自動化計画](docs/automation-plan.ja.md) |
| Decisions and evidence / 判断と証拠 | [Development log](docs/development-log.en.md) | [開発記録](docs/development-log.ja.md) |
| Current validation / 今回の検証 | [v0.5.1 validation](docs/validation-v0.5.1.md) | 同じ資料に併記 |
| Earlier CI validation / 以前のCI検証 | [v0.5 validation](docs/validation-v0.5.en.md) | [v0.5検証](docs/validation-v0.5.ja.md) |
| Earlier observations and plan / 過去の観察と計画 | [Evidence guide](docs/evidence-guide.md) | 同じ資料に併記・原記録へリンク |
| Release history / 変更履歴 | [Changelog](CHANGELOG.md) | 同じ資料に併記 |

## Run on Windows / Windowsで使う

Requires Python 3.10 or later and the `py` launcher. No additional pip packages are needed. This is a source distribution; Python is not bundled.

Python 3.10以上と `py` ランチャーが必要です。追加のpipインストールは不要です。Pythonを同梱しないソース配布版です。

1. Extract the app ZIP. / アプリのZIPを展開します。
2. Double-click **`start.cmd`**. / **`start.cmd`** をダブルクリックします。
3. The browser opens after the server is ready and connects automatically. / サーバー起動後にブラウザが開き、自動接続します。
4. Use **“Test the gate without the model API / APIを使わずにGateを確かめる”** first. / まず固定デモのボタンで確認します。

Keep the launch window open. Press Ctrl+C there to stop. Running the same `start.cmd` again retains the saved records and history.

起動ウィンドウは開いたままにします。終了はCtrl+Cです。同じ `start.cmd` で再起動すると、保存済みの正本と履歴を引き継ぎます。

Use **`start-fresh-demo.cmd`** for a new demonstration. It creates a separate folder under `demo-runs/` and preserves previous data. The local port may change at each launch.

新しい実演には **`start-fresh-demo.cmd`** を使います。`demo-runs/` に別フォルダを作り、以前のデータを残します。接続先のポート番号は起動ごとに変わることがあります。

A page reload clears the keys held in page memory. Open “Connect manually / 手動で接続する” and enter the keys from `credentials.json` in the data folder shown by the launcher. To reconnect automatically, stop and relaunch the app.

ページの再読込でメモリ中のキーは消えます。起動ウィンドウに表示されたデータフォルダの `credentials.json` を使い、手動で接続できます。自動接続をやり直す場合は、アプリを停止して再起動します。

## Keep existing data / 旧版のデータを引き継ぐ

1. Stop the older app with Ctrl+C. / 旧版をCtrl+Cで停止します。
2. Extract the new ZIP into a separate folder. / 新版を別フォルダへ展開します。
3. Before its first normal launch, copy the old `data` folder into the new `m-anchor-app/data`. Keep the original as a backup. / 新版の通常起動前に、旧版の `data` を新版の `m-anchor-app/data` へコピーし、元データを保管します。
4. Open the new `start.cmd`. / 新版の `start.cmd` を開きます。

For a differently named data folder: / 別名のデータフォルダを使う場合：

```powershell
py -3 app\launcher.py --data "path-to-existing-data"
```

The data format is shared by v0.4, v0.5, and v0.5.1. Earlier data gains execution-metadata tables without inventing missing dates or model IDs. Existing cases, evidence, decisions, and connection keys are retained. Initialization never overwrites an existing store; incomplete folders cause an error.

v0.4・v0.5・v0.5.1のデータ形式は共通です。それ以前のデータには実行情報用の表を追加しますが、未記録の日時やモデルIDは補完しません。案件・証拠・判定・接続キーは保持します。既存ストアを初期化で上書きせず、不完全なフォルダはエラーとして停止します。

## Connect a model / 実モデルを接続する

Select a case and enter an OpenAI API key, a model ID available to that key, and your request. Each run makes one API call, then submits the exact proposal through the dedicated Python client. Your request and case context are sent to OpenAI and API charges apply. Both English and Japanese requests are accepted; the example text is bilingual and editable.

案件を選び、OpenAI APIキー・利用可能なモデルID・依頼文を入力します。1回のAPI呼出しで得た提案を、専用Pythonクライアントでそのまま提出します。依頼と案件情報はOpenAIへ送信され、料金が発生します。英語・日本語の依頼を使用でき、併記された例文は編集できます。

The API key is excluded from model input and database records. Raw proposals are retained in audit history. Failed API calls are not retried automatically. If the saving outcome is unclear, refresh state and history before submitting again.

APIキーはモデル入力やDBに保存しません。提案原文は監査履歴に残します。API失敗時に自動再試行は行いません。保存結果が不明な場合は、再提出の前に正本と履歴を更新してください。

## Validation and scope / 検証と適用範囲

The [v0.5.1 validation record](docs/validation-v0.5.1.md) distinguishes local checks, hosted CI, and unverified behavior. The suite contains 34 application tests, 3 packaging tests, and a UI logic check. Model responses are mocked; CI makes no paid model calls. Earlier user-supplied demo records are indexed in the [evidence guide](docs/evidence-guide.md).

[v0.5.1検証記録](docs/validation-v0.5.1.md)でローカル確認・CI・未確認事項を区別します。アプリ34件、配布処理3件、UIロジックを検査します。モデル応答は模擬し、CIで有料APIは使いません。過去の利用者側記録は[証拠ガイド](docs/evidence-guide.md)から確認できます。

Protection covers case records in this local store. The app does not establish evidence truth, control external tools, or isolate processes that already have direct access to the database. Evidence admission is configured during initialization. See the integration guide before considering a business connection.

保護対象はこのローカルストア内の案件記録です。証拠内容の真偽判定、外部ツールの制御、DBへ直接アクセスできるプロセスの隔離は行いません。証拠認可は初期化時に設定します。業務接続の検討には接続仕様を参照してください。

## Development / 開発

```sh
python3 app/launcher.py
python3 -m unittest discover -s app -v
python3 scripts/check_ui.py
python3 scripts/ci.py
python3 scripts/build_release.py --output dist
```

The UI logic check needs Node.js. CI and packaging record their results and check file hashes. / UIロジックの確認にはNode.jsが必要です。CIと配布処理は結果を記録し、ファイルのハッシュを照合します。

## Download from GitHub / GitHubから配布物を取得する

1. Open [Actions](https://github.com/iseyan/M-Anchor-App/actions/workflows/verify-package.yml) and choose a successful run. / Actionsで成功した実行を選びます。
2. Download `m-anchor-app-package-<number>` from Artifacts. / Artifactsから同名のファイルを取得します。
3. Extract it to find the app ZIP, its SHA256, and `build-info.json`. / 展開するとアプリのZIP・SHA256・作成記録が入っています。
4. Extract the app ZIP and open `start.cmd`. / アプリのZIPをもう一度展開し、`start.cmd` を開きます。

Logs are in `verification-<OS>-py<version>`. Artifacts are configured for 14-day retention; GitHub sign-in may be required. Executable packaging and distribution licensing remain future work. This version adds no LICENSE file.

ログは `verification-<OS>-py<version>` にあります。Artifactsの保持期間は14日で、取得にGitHubログインが必要な場合があります。実行ファイル化と配布ライセンスの確定は今後の作業です。この版でLICENSEは追加していません。

Related project / 関連プロジェクト: [M-Anchor Framework](https://github.com/iseyan/m-anchor-framework)
