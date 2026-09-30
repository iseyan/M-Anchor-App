# V1 — Record protection against prompt attacks
# V1 — プロンプト攻撃に対する記録保護

M-Anchor App V1 (1.0.0) lets you submit adversarial inputs to a model, inspect its exact proposal, and see whether the authoritative record changed after gate checks. It also provides fixed proposals that demonstrate the gate without calling a model.

M-Anchor App V1（1.0.0）は、モデルへの攻撃入力、返された提案原文、Gateの検査後に正本がどうなったかを追えるアプリです。モデルを呼び出さずにGateを実演する固定提案も用意しています。

**Model proposes; deterministic layer commits.** The protected object is the case record in this store. Evidence admission and interpretation come from trusted initial configuration.

**モデルは提案し、決定論的な層が保存を確定します。** 保護対象はこのストアの案件記録です。証拠の認可と解釈は、信頼された初期設定から取得します。

## A three-minute demonstration / 3分で実演する

1. Extract the ZIP and open **`start-fresh-demo.cmd`**. It creates separate demo data. / ZIPを展開して **`start-fresh-demo.cmd`** を開きます。別のデモデータを作成します。
2. Select **Forced resolution / 根拠のない確定** in Scenario. / シナリオから同名の項目を選びます。
3. Click **Run fixed proposal (no API) / 固定提案を実行（APIなし）**. No API key is needed. / キーの入力は不要です。
4. Check **Rejected / 拒否** and **Record unchanged · readback verified / 正本は変更なし・再読込確認済み**. / 拒否と正本の保持を確認します。
5. Select **Admitted-evidence update / 正当な更新の対照** and run its fixed proposal. / 正当更新の固定提案を実行します。
6. Check **Saved / 保存**, h_B, and Version 2. Run it again to see **No change / 変更なし**. / h_B・Version 2への更新と、再実行での変更なしを確認します。
7. Use **Export records as JSON / 確認記録をJSONで保存** to retain all history. / 全件の履歴を保存できます。

These fixed runs demonstrate gate behavior. They do not execute the displayed input text and do not measure a model's resistance to an attack. Editing the text only affects **Run with model / モデルで実行**.

固定実行はGateの動作を示します。表示された入力文は実行せず、モデルの攻撃耐性も測定しません。文章の編集が反映されるのは **「モデルで実行」** です。

## Included scenarios / シナリオ一覧

| Scenario / シナリオ | Target / 対象 | Fixed proposal outcome / 固定提案の結果 |
| --- | --- | --- |
| Forced resolution / 根拠のない確定 | Remove h_A without evidence / 証拠なしでh_Aを削除 | Rejected; state retained / 拒否・保持 |
| Forged evidence approval / 証拠認可の偽装 | Claim e_B is admitted for HOLD / HOLDへのe_B認可を主張 | Rejected; authority retained / 拒否・認可も維持 |
| Future-check bypass / 今後の検査の迂回 | Request future_bypass_authorized=true / 迂回権限を要求 | Rejected / 拒否 |
| State-reference tampering / 参照する状態の改ざん | Replace the state hash with zeroes / 状態ハッシュを0へ差替え | Rejected / 拒否 |
| Preserve unresolved candidates / 未決を保つ対照 | Keep both candidates / 両候補を保持 | No change / 変更なし |
| Admitted-evidence update / 正当な更新の対照 | Use e_B for UPDATE / UPDATEでe_Bを使用 | Saved, then no change on repetition / 保存、繰返しは変更なし |

These expectations use fresh synthetic demo data. Model-generated proposals may differ. A scenario label records which example was selected; it is not an attack detector or an automatic success verdict. Edited scenario text retains the selected label. Selecting another target case switches to Custom input.

期待結果は新しい人工デモデータでのものです。モデルが生成する提案は異なり得ます。シナリオ名は選んだ例を記録するもので、攻撃検出や成功判定ではありません。例文を編集しても選択名は残り、対象案件を手動で変更すると自由入力へ切り替わります。

## Run a model / モデルで実行する

Select a scenario or Custom input, choose the target case, and enter your OpenAI API key and an available model ID. Edit the input, then press the button naming the target case. Each run makes one model API request and can incur charges. The app makes no automatic retries.

シナリオまたは自由入力を選び、対象案件・OpenAI APIキー・利用可能なモデルIDを指定します。入力を編集し、対象案件名が表示された実行ボタンを押します。1回の実行でモデルAPIを1回呼び出し、料金が発生し得ます。自動再試行は行いません。

The existing model connection sends the input as a user message with trusted case context supplied separately. V1 does not fetch websites, emails, or documents. Pasting text into the input is a direct-input exercise, not a verified indirect-injection integration.

既存のモデル接続で、入力はユーザーメッセージとして送り、信頼された案件情報は別に渡します。V1はWeb・メール・文書を自動取得しません。文章の貼付けは直接入力の演習であり、間接インジェクションの接続検証ではありません。

The result distinguishes the input, proposal source, gate decision, and independent readback. A model can preserve the state itself or propose an invalid change that the gate rejects. “No change” and “Rejected” therefore remain separate. A failed or incomplete API call is not shown as a contained attack.

結果には入力、提案の生成経路、Gate判定、独立した再読込を分けて表示します。モデルが現状維持を提案する場合と、不正な提案をGateが拒否する場合は異なるため、「変更なし」と「拒否」を区別します。API失敗や未完了の応答を、攻撃を阻止した結果として扱いません。

## What is recorded / 記録する内容

For proposals submitted through the V1 model route, `execution.exercise` contains the selected scenario, category, input text, and its SHA256. It is bound to the exact proposal and case with the existing single-use submission ticket. The gate saves the execution metadata, proposal, and decision in the same transaction as any state update.

V1のモデル経路で提出された提案では、`execution.exercise` に選択シナリオ・分類・入力原文・SHA256を残します。既存の一回限りの提出チケットで提案原文と案件に結び付け、正本更新・提案・判定・実行情報を同じトランザクションに保存します。

Fixed scenarios use `mode=fixed_proposal`, `source=fixed_scenario`, and null input fields: no model input was executed. Model-route fields describe the application's processing route, not provider-signed proof. Automated tests replace the model with an explicitly identified mock.

固定シナリオは `mode=fixed_proposal`、`source=fixed_scenario`、入力欄はnullで、モデル入力を実行していないことを示します。モデル経路の項目はアプリ内の処理経路であり、提供元が署名した証明ではありません。自動試験では明示した模擬モデルへ置き換えます。

Old records and other submission routes can have no exercise data. Missing information is not reconstructed. An API failure before proposal submission creates no gate-history entry; the screen shows the error. The report schema stays `m-anchor-app-observation/v2` with optional exercise metadata.

旧記録や他の提出経路には演習情報がない場合があり、欠けた情報を推測で補いません。提案提出前のAPI失敗はGateの履歴を作らず、画面にエラーを表示します。出力スキーマは `m-anchor-app-observation/v2` を継続し、任意の演習情報を追加します。

**Input text is now saved and exported for the model route.** Key input fields are excluded, but anything pasted into the request or returned in a proposal becomes part of the record. Use synthetic data for demonstrations and inspect exports before sharing.

**モデル経路では入力文も保存・出力します。** キー入力欄は除外しますが、依頼文に貼り付けた内容や提案に含まれる内容は記録されます。実演には人工データを用い、共有前に出力内容を確認してください。

## Scope for a business discussion / 企業への説明範囲

V1 demonstrates control over this store's case records. It does not promise universal jailbreak prevention, filter all harmful model text, prevent all information leakage, control external tools, or isolate programs with direct database access. A business integration needs a defined record, trusted evidence authority, and a write path that cannot bypass the gate.

V1が示すのは、このストアの案件記録に対する制御です。あらゆるジェイルブレイクの防止、有害文章全般の検査、情報漏洩全般の防止、外部ツールの制御、DBへ直接アクセスできるプログラムの隔離は扱いません。企業接続では、対象記録・証拠認可の担当・Gateを迂回できない書込み経路を定めます。

The next integration can extend this structure to one chosen external operation. V1 requires no AWS service and starts locally using the existing Windows launchers. Its version number identifies this workflow release, not a security certification.

次の接続では、選んだ外部操作一種類にこの構造を拡張できます。V1にAWSは不要で、従来のWindows起動ファイルを使います。版番号はこの操作構成のリリースを示し、セキュリティ認証を示すものではありません。

See [integration](integration.en.md) / [接続仕様](integration.ja.md) and [V1 validation / V1検証](validation-v1.md).
