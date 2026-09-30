# Changelog / 変更履歴

## v0.5.1 — 2026-10-01 (Japan time / 日本時間)

- Present app headings, decisions, history, errors, and editable example requests in English first, followed by Japanese.  
  見出し・判定・履歴・エラー・編集可能な依頼文の例を英語優先の英日併記に変更。
- Add paired English documentation and a bilingual guide to original historical evidence.  
  英語版の主要資料と、過去の原記録を案内する英日併記資料を追加。
- Update existing UI checks to exercise both languages; show a bilingual error for invalid manual JSON.  
  既存のUI確認を両言語に対応し、手動JSONの形式エラーも併記で表示。
- Keep gate rules, stored proposal bytes, API field names, and observation schema unchanged.  
  Gate規則・保存された提案原文・API項目名・記録スキーマを保持。

## v0.5 — 2026-10-01(Japan time / 日本時間)

- Added GitHub Actions verification on Linux/Python 3.10 and 3.13 and Windows/Python 3.13.  
  GitHub ActionsでLinux/Python 3.10・3.13、Windows/Python 3.13を検証する構成を追加。
- Run app tests, UI logic, packaging tests, and source checksums.  
  既存のアプリ試験、UIロジック、配布処理の試験、ソースのチェックサムを確認。
- Package successful push/manual runs after all environments pass; verify pull requests without packaging.  
  全環境が通過したpush・手動実行から配布ZIPを作成。PRでは検証まで行う。
- Retain logs, verification JSON, ZIP, SHA256, and build records with source commits as artifacts.  
  実行ごとのログ・検証JSON、ZIP・SHA256・ソースコミットを含む作成記録をArtifactsに保存。
- Check every ZIP entry and reject altered inputs or unsafe packaging paths.  
  ZIP内の全ファイルを照合し、入力の改変や不正な梱包パスを拒否。
- Preserve repository file bytes across Windows and Linux.  
  WindowsとLinuxでリポジトリのファイルバイトを保持する設定を追加。
- Update the displayed app version to 0.5; retain v0.4 gate rules and record format.  
  アプリの版表示を0.5へ更新。v0.4の判定規則と記録形式を継続。

## v0.4 — 2026-10-01(Japan time / 日本時間)

- Persist route, server receipt time, app version, and model metadata with each decision.  
  各判定に、提出経路・サーバー受信日時・アプリ版・モデル利用情報を同時保存。
- Bind model metadata to the case and proposal SHA256 using an internal single-use ticket.  
  モデル情報は、内部の一回限りのチケットで案件と提案のSHA256に結び付ける。
- Use distinct admin routes for fixed demos and manual submissions; all routes use the same gate.  
  固定デモの生成と手動提出に管理用経路を設け、外部クライアントAPIと区別。すべて同じGateで検査。
- Add past-entry details, persisted readback observations, and complete JSON export (schema v2).  
  過去履歴の詳細表示、再読込結果の記録、全件JSON出力（schema v2）を追加。
- Distinguish repeated proposals by audit_id and export raw bytes in Base64.  
  同一提案の繰返しもaudit_idで区別。生バイトをBase64でも出力。
- Preserve old history and use null for metadata that was never recorded.  
  旧履歴は保持し、当時の未記録情報はnullとして扱う。
- Pass 34 tests and UI logic; record plans for later GitHub Actions and AWS work.  
  34件のテストとUIロジック確認を完了。GitHub Actions・AWSは今後の構成計画を記録。

## v0.3 — 2026-09-30

### Operation / 操作

- Use M-Anchor App consistently as the interface name.  
  画面名をM-Anchor Appへ統一。
- Add a launcher that opens the browser after checking server readiness.  
  サーバーの起動を確認してからブラウザを開くランチャーを追加。
- Add automatic connection with a single-use launch ticket.  
  一回限りの起動用チケットによる自動接続を追加。
- Start with no case selected and show the target on the run button.  
  対象案件を未選択で開始し、実行ボタンにも案件名を表示。
- Show Saved, Rejected, No change, and before/after candidates, status, and version.  
  保存・拒否・変更なしと、更新前後の候補・状態・Versionを表示。
- Submit fixed demos in one click without a model API.  
  固定デモをAPIなし・1ボタンで提出できるよう変更。
- Start fresh demos without deleting previous data.  
  以前のデータを残したまま新しいデモを起動できるよう変更。

### Records and explanation / 記録と説明

- Export records, evidence settings, history, and the latest page execution metadata as JSON.  
  正本・証拠設定・履歴・ページ内の直近実行情報をJSONで保存。
- Add overview, demo guide, integration/boundary documentation, and development/validation records.  
  概要、デモ手順、接続仕様、保護境界、検証・開発記録を追加。
- Keep gate, formal core, model bridge, and Python client byte-identical to v0.2.  
  Gate、形式核、モデル接続処理、Pythonクライアントはv0.2と同じバイト列を維持。

## v0.2 — 2026-09-30

- Add single-request proposal generation via the OpenAI Responses API.  
  OpenAI Responses APIによる一回の提案生成を追加。
- Submit unmodified model output to the gate via the dedicated Python client.  
  モデル出力を修復せず、専用Pythonクライアント経由でGateへ提出。
- Display proposal text, gate decision, and model usage.  
  提案文、Gate判定、モデル利用情報を表示。
- Observe uncertainty retention and a supported-update outcome using a real API on the user’s Windows environment.  
  利用者のWindows環境で実API経由の未決保持と、正当更新の操作結果を確認。

## v0.1 — 2026-09-30

- Connect the existing gate and formal core to a local HTTP API, SQLite store, and browser UI.  
  既存Gate・形式核にローカルHTTP API、SQLiteストア、ブラウザ画面を接続。
- Check unsupported-resolution rejection and admitted-evidence updates with fixed proposals.  
  固定案による根拠なし確定の拒否と、認可済み証拠による更新を確認。
