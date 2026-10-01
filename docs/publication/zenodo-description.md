# Zenodo description / Zenodo掲載文

Copy the title and description into a Software record and select **Apache License 2.0 (Apache-2.0)** in the license field. The repository includes the license text and attribution notice. No existing app DOI is asserted.

題名と説明をSoftwareの記録に転記し、ライセンス欄では **Apache License 2.0（Apache-2.0）** を選んでください。本文と帰属表示はリポジトリに収録しています。既存のアプリDOIがあるとは主張しません。

## Title / 題名

M-Anchor App V1: A Deterministic Gate for Containing Prompt-Induced Unauthorized Record Updates

## Description - English

M-Anchor App is a local Python application that separates AI-generated proposals from authoritative case-record updates. A deterministic gate checks the referenced state, externally admitted evidence, candidate transitions, and authority requests before saving a change. Its principle is: Model proposes; deterministic layer commits.

The V1 demonstration includes four fixed attack types (unsupported resolution, forged evidence admission, future-check bypass, and state-reference tampering), two controls, an optional model connection, and English/Japanese explanations. Input, proposal, decision, and read-back state can be inspected and exported. The source package includes reproduction instructions, validation records, and two original observation exports containing 20 entries and one entry, respectively.

The fixed observations show rejection of four invalid proposal types and acceptance of a supported update. Three model-route observations record one adversarial input that the model itself answered by preserving uncertainty, one valid no-change proposal, and one supported update saved from Version 1 to Version 2. The adversarial model example is not a gate rejection of an invalid model output.

“Attack neutralization” is limited here to blocking unauthorized case-record transitions at the gate. The app does not prevent all incorrect GPT text, establish evidence truth, control external tools, or demonstrate universal prompt-injection or jailbreak resistance. This is a software demonstration with inspectable evidence, not an independently certified security product. Python 3.10 or later is required; fixed scenarios need no model API key. This distribution is licensed under Apache-2.0, permitting commercial use, modification, and redistribution under its terms. The M-Anchor Framework is a related, separately versioned project.

## 説明 - 日本語

M-Anchor Appは、AIが生成する提案と案件正本の更新を分離するローカルPythonアプリです。決定論的Gateが、参照する状態、外部で認可した証拠、候補遷移、権限要求を検査してから保存します。原則は「モデルは提案し、決定論的な層が保存を確定する」です。

V1では、根拠なしの確定、証拠認可の偽装、今後の検査の迂回、状態参照の改ざんという固定攻撃4種類と対照2種類、任意のモデル接続、英日説明を用意しています。入力・提案・判定・再読込した正本を確認・出力できます。ソース配布物には再現手順、検証記録、20件と1件を含む二つの原観察JSONを収録しています。

固定提案では不正な4種類の拒否と正当更新を確認しました。モデル経由3件は、攻撃入力に対してモデル自身が未決を保持した例、正当な変更なしの例、Version 1から2への正当な保存例です。攻撃入力のモデル例を「Gateが不正なモデル出力を拒否した例」とは扱いません。

ここでの「攻撃の無効化」は、Gateで不正な案件記録遷移を成立させない範囲に限ります。GPTのあらゆる誤文の生成防止、証拠の真偽判定、外部ツールの制御、プロンプトインジェクションやジェイルブレイク全般への耐性を実証したものではありません。検査可能な証拠を伴うソフトウェア実演であり、独立した認証を受けた製品ではありません。Python 3.10以上が必要で、固定例にAPIキーは不要です。この配布物はApache-2.0で許諾し、その条件の下で商用利用・改変・再配布が可能です。関連するM-Anchor Frameworkとは版番号を分けています。
