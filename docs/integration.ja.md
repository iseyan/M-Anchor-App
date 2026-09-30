# 接続と保護境界

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
| `GET /admin/cases` | admin_token | 全案件と証拠設定を取得 |
| `GET /admin/history` | admin_token | 最新100件の判定履歴を取得 |
| `GET /admin/report` | admin_token | 一貫したDBスナップショットから確認記録を取得 |
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

ブラウザのJSON出力では、さらにそのページの直近の実行情報を付ける。これは第三者への説明や再現の補助となる観察記録であり、署名された監査証明ではない。`observed_at_utc` はブラウザで結果を受け取った時刻で、commit時刻ではない。DBの履歴には現在、モデルID・生成元・commit時刻を恒久保存していない。
