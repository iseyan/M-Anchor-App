# 接続と保護境界

[English](integration.en.md) | [日本語](integration.ja.md)

## 専用Pythonクライアント

`app/client.py` の `AnchorClient` が、状態取得と提案提出を担当する。接続先は起動ウィンドウのAddress、エージェントキーは当該データフォルダのcredentials.jsonで確認する。

以下はリポジトリのルートから実行する接続例である。`raw_json` にはモデルが返した文字列をそのまま渡す。

```python
import os
import sys
sys.path.insert(0, 'app')
from client import AnchorClient

client = AnchorClient(
    os.environ['ANCHOR_AGENT_TOKEN'],
    os.environ['ANCHOR_BASE_URL'],
)
context = client.state('DEMO-HOLD')
# contextをモデルに渡して提案文raw_jsonを得る。
# raw_jsonは修復・項目差し替えをせず、そのまま提出する。
# result = client.propose('DEMO-HOLD', raw_json.encode('utf-8'))
```

| API | 権限 | 内容 |
| --- | --- | --- |
| `GET /v1/cases/{id}` | agent_token | 状態と当該案件の認可済み証拠・解釈を取得 |
| `POST /v1/cases/{id}/proposals` | agent_token | 生JSONの更新案を提出 |
| `GET /admin/scenarios` | admin_token | 攻撃4種類と対照2種類の一覧 |
| `POST /admin/scenario-run` | admin_token | モデルを使わず選んだ固定提案を提出 |
| `GET /admin/cases` | admin_token | 全案件と証拠設定を取得 |
| `POST /admin/demo-run` | admin_token | 指定デモの固定案をサーバーで生成してGateへ提出 |
| `POST /admin/cases/{id}/proposals` | admin_token | 手動編集した生JSONを同じGateへ提出 |
| `GET /admin/history/{id}` | admin_token | 提案原文と実行情報を含む一件の詳細 |
| `GET /admin/history` | admin_token | 最新100件の判定履歴を取得 |
| `GET /admin/report` | admin_token | 一貫したDBスナップショットから全件の確認記録（v2）を取得 |
| `GET /admin/info` | admin_token | 版とデータの表示名を取得 |
| `POST /admin/model-run` | admin_token | 1回のモデル生成とクライアント経由の提案提出 |

HTTP 200は検査結果を受信したことを意味する。保存可否は `decision` で読む。

| decision | 意味 |
| --- | --- |
| commit | 更新を保存した |
| reject | 規則に合わない提案を拒否した |
| no_commit | 変更不要などにより保存状態を変更しなかった |
| undetermined | 保存結果を確定できない。正本・履歴を再取得する |

## 起動時の自動接続

`launcher.py` は、ローカルサーバーの起動をHTTPで確認してからブラウザを開く。起動ごとに一度だけ使える、120秒で失効するランダムな起動用チケットを生成する。

チケットはURLのフラグメントで画面に渡し、画面は直ちにアドレスバーから除去する。フラグメントはHTTPリクエストのURLに送られない。同一Originから `POST /launch-session` にチケットを提示すると、このページのメモリへ管理キーとエージェントキーを受け取る。使用済み・期限切れ・不一致のチケットは拒否する。

この処理は起動時の接続操作を省くためのもので、Gateの検査や証拠認可を変更しない。通常の管理キーやAPIキーをURL、HTML本文、ブラウザの永続ストレージへ埋め込まない。起動用チケットも有効な間は接続権限を持つため、URLを共有する仕組みではない。

## データと権限

正本と監査は `state.sqlite3`、アプリの接続キーは `credentials.json` に保持する。APIキーはファイルやDBに保存しない。通常起動では `data/`、新しいデモでは `demo-runs/` 内の個別フォルダを使う。

モデルに渡すのは案件状態・認可済み証拠と解釈・依頼文・提案形式の指示である。モデルへ管理キー、エージェントキー、DBパス、シェルや外部ツールは渡さない。API呼出しには `store:false` を指定しているが、提供元のすべての保持条件をこの指定だけで決定するものではない。

サーバーは127.0.0.1で待ち受け、Host・Origin・役割別キーを検査する。同じOS権限でDBや接続キーファイルを直接読み書きできるプログラムに対する隔離機能はない。業務システムへの接続では、正本の書込み権限とモデル側の実行権限の配置を設計する必要がある。

稼働中の証拠追加・撤回、候補復元、外部ツール実行、暗号化保存、監査ログの保存上限・ローテーションは現在の版にはない。hashは整合性検査用で、書込み権限を持つ相手による改ざんに対する電子署名ではない。

## 確認記録の扱い

`/admin/report` はSQLiteのbackup機能でメモリ内に一貫したコピーを作り、そこから正本・証拠設定・履歴を読む。原ストアの更新は行わない。現行方式はDB全体をメモリへ複製するため、小規模なローカルデモを想定する。

v0.4の出力schemaは `m-anchor-app-observation/v2`。`history` の各項目には従来の判定に加えて次を含む。

| 項目 | 内容 |
| --- | --- |
| id | DB内で一意の履歴番号。提出応答のaudit_idと対応 |
| execution.source | live_model / fixed_scenario / fixed_demo / manual / agent_api |
| execution.received_at_utc | サーバーがGateへ渡す直前の時刻。commit完了時刻ではない |
| execution.app_version | 受け付けたアプリの版 |
| execution.submitted_case_id | 提出先案件。提案が不正でも提出先は残る |
| execution.model_metadata | 提供元のmodel、response_id、input_tokens、output_tokens。該当しなければnull |
| execution.exercise | V1の任意の演習情報とモデル入力原文。後述 |
| proposal_text | UTF-8として読める原文。不正なUTF-8ならnull |
| proposal_base64 | 提案の生バイト。復号後のSHA256がraw_sha256と対応 |
| readback | status（matched / mismatch / not_applicable）とchecked_at_utc |

`execution` がnullなら実行情報は未記録。旧履歴の日時やモデルIDを推測しない。`readback` がnullなら未記録、または保存後の再読込記録までに処理が中断した状態で、一致確認済みとは扱わない。`matched` は記載の時刻に観察した一致を意味する。

正本の更新、従来のauditへの判定・生バイト、追加のexecutionsへの実行情報は、一つのSQLiteトランザクションに保存する。実行情報を保存できなければ、正本と判定の保存も取り消す。独立した再読込結果はその後の観察として別に追記する。

モデル経路では、サーバー内の生成処理が返した情報のうち四項目だけを採用する。ランダムな一回限りのチケットを使い、提案の生バイトのSHA256と提出先案件に結び付け、専用Pythonクライアントで通常のGate APIへ提出する。チケットはメモリ内で60秒間有効。APIの呼出元が `source=live_model` と自己申告しても、モデル経路としては記録しない。

固定デモは管理用APIが決まった提案を生成し、手動提出も管理用APIを通る。どちらもGateの規則を迂回できない。外部の専用Pythonクライアントによる通常の提出はagent_apiとなり、AI生成か人の入力かまでは識別しない。

これらはサーバーの処理経路を示す説明記録であり、モデル提供元による電子署名や、改ざん不能な証明ではない。テストでモデル応答を置き換えた場合も同じ処理経路を通るので、模擬実行であることを検証資料とモデルIDに明示する。キー入力欄は実行記録に保存しない。V1からモデル経路の依頼文も提案とともに原文のまま保存するため、依頼文に貼り付けた秘密情報は記録に含まれる。旧版では依頼文は保持していない。

JSON出力は全件をメモリに載せる小規模デモ向けの方式。画面上の100件制限で古い記録を切り捨てない。大量データ向けの分割出力や保持期限は未実装である。

## V1の演習情報

`GET /admin/scenarios` は攻撃4種類と対照2種類を返す。`POST /admin/scenario-run` は `{"scenario_id":"authority_override"}` のように一項目だけ受け付け、サーバー側で対象を選び、固定提案を同じGateへ提出する。モデルを呼ばず、編集した入力文も実行しない。

`POST /admin/model-run` は従来の四項目に任意の `scenario_id` を追加でき、省略時は `custom` となる。定義済みシナリオと案件が一致しない場合、未知のID、呼出元が付加した演習情報は生成前に拒否する。シナリオ名は選択した演習であり、入力に対する信頼された判定ではない。

`execution.exercise` はschema `m-anchor-exercise/v1`、scenario_id、category、英日title、mode、input_text、input_sha256、input_origin、input_sent_to_modelを持つ。モデル経路では入力原文とハッシュをチケットで案件・提案に結び付ける。固定シナリオでは入力項目はnull、input_sent_to_modelはfalse。modeはmodel_requestまたはfixed_proposal。模擬応答を用いる試験も同じ経路を使い、提供元が署名した証明とは扱わない。

演習情報は観察用であり、証拠認可・規則変更・正本更新を許可しない。旧記録や他の経路では存在しない場合がある。既存の実行JSONに保存するためDB構造の変更はない。生成が失敗して提案が届かなければGateの履歴は作らず、画面にエラーを表示する。

[V1手順](v1-guide.md)に適用範囲と入力文の保存を説明する。
