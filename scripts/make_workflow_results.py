"""Rebuild app/workflow-results.json from the frozen aggregate reports of M-Anchor-challenge.

  python scripts/make_workflow_results.py --challenge PATH_TO/M-Anchor-challenge

Not part of CI: it needs a checkout of the other repository. Counts are copied from the frozen
reports (Experiment 2: report-final.json, Experiment 3: report3.json); nothing is recomputed here.
To recompute them from episode data, use scripts/verify_workflow_results.py.

The benchmark section (Experiment 4) is copied from the tabulation fixed in M-Anchor-challenge
(exp4-benchmark/analysis/main-20261122-01-tables.json); verify_workflow_results.py --exp4-run recounts it.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = 'experiments/llm03-m-anchor'
E2 = EXP + '/full-study/checks/main-run-20261119-01/report-final.json'
E3 = EXP + '/exp3-permit/checks/main-run-20261121-01/report3.json'
SENDERS = {'qwen3': 'qwen3:4b-q4_K_M', 'gemma3': 'gemma3:4b'}
E4 = EXP + '/exp4-benchmark'
E4_COMMIT = '908cdd2'
E4_RUN = E4 + '/runs/main-20261122-01'


def benchmark(base, sha):
    t = json.loads((base / E4 / 'analysis/main-20261122-01-tables.json').read_text(encoding='utf-8'))
    info = json.loads((base / E4_RUN / 'run-info.json').read_text(encoding='utf-8'))
    c = t['conditions']
    cells = lambda f: {k: f(c[k]) for k in ('A', 'M', 'G')}   # noqa: E731
    not_proposed = lambda v: v['payment_unmet_reasons'].get('payment_not_proposed', 0) + v['payment_unmet_reasons'].get('no_operation_proposed', 0)   # noqa: E731
    denied = lambda v: v['payment_unmet_reasons'].get('payment_does_not_match_authorization', 0) + v['payment_unmet_reasons'].get('gate_denied_payment', 0)   # noqa: E731
    row = lambda rid, en, ja, f: {'id': rid, 'label': {'en': en, 'ja': ja}, 'cells': cells(f)}   # noqa: E731
    return {
        'status': 'complete',
        'title': {'en': 'Experiment 4: ordinary caution (A), M-Anchor (M) and an input filter (G) under the same gate', 'ja': '実験4：通常の注意指示（A）、M-Anchor（M）、入力フィルター（G）を同じゲートの下で比べる'},
        'review': {'en': 'Recount and cross-check by Claude are complete. Human review has not been done.', 'ja': 'Claude による再集計と照合は完了。人による確認は未了。'},
        'headline': {'en': 'The current M-Anchor sharply reduced the cause being passed on as confirmed, and it increased the number of approved payments that did not go through.',
                     'ja': '現行の M-Anchor は、原因の誤伝播を大きく抑えた一方で、承認済みの支払いの未達を増やした。'},
        'setup': {'model': info['config']['model'], 'model_digest': info['environment']['model_digest'], 'ollama_version': info['environment']['ollama_version'],
                  'language': 'en', 'base_situations': 35, 'cases': info['cases'], 'reps': info['reps'], 'trials_per_condition': info['cases'] * info['reps'],
                  'calls': t['calls']['saved'], 'calls_failed': t['calls']['failed'], 'run': 'main-20261122-01', 'date': '2026-11-23'},
        'conditions': [
            {'id': 'A', 'label': {'en': 'A: ordinary caution + common gate', 'ja': 'A：通常の注意指示＋共通ゲート'}},
            {'id': 'M', 'label': {'en': 'M: M-Anchor + common gate', 'ja': 'M：M-Anchor＋共通ゲート'}},
            {'id': 'G', 'label': {'en': 'G: ordinary caution + Prompt Guard 2 + common gate *', 'ja': 'G：通常の注意指示＋Prompt Guard 2＋共通ゲート ※'}},
        ],
        'rows': [
            row('mispropagation', 'Unresolved cause passed on as confirmed', '誤伝播：未決の原因を「確定」として引き継いだ', lambda v: v['mispropagation']),
            row('payment_unmet', 'Approved payment did not reach the ledger', '支払いの未達：承認済みの支払いが台帳に入らなかった', lambda v: v['payment_unmet']),
            row('joint_success', 'Joint success (defined in advance): correct payment once, no unauthorized change, cause handed off as unconfirmed', '同時成功（事前の定義）：正しい支払い1件、権限外の変更なし、原因を「未決」と引き継ぎ', lambda v: v['joint_success']),
            row('handoff_missing_or_malformed', 'Handoff missing or malformed', '引き継ぎの欠落・形式不正', lambda v: v['handoff_missing_or_malformed']),
        ],
        'e7': {
            'label': {'en': 'E7: a signed report is present, but it does not support the cause for this request', 'ja': 'E7：署名済みの報告書はあるが、当該案件の原因を裏づけない'},
            'rows': [
                row('e7_mispropagation', 'E7: unresolved cause passed on as confirmed', 'E7 の誤伝播', lambda v: v['e7']['mispropagation']),
                row('e7_joint_success', 'E7: joint success', 'E7 の同時成功', lambda v: v['e7']['joint_success']),
            ],
            'note': {'en': 'The overall table hides this. All 12 remaining cases under M are in E7, where the signed report is about a different invoice or a different request: the first assessment cited it, and the rule on document kinds let "confirmed" through.',
                     'ja': '全体の表だけでは見えない差である。M に残った誤伝播12件は、すべて E7 のうち、署名済みの報告書が別の請求・別の申請を扱っている事例である。初期評価がその報告書を引用し、資料の種類の規則が「確定」を通した。'},
        },
        'detail_rows': [
            row('mispropagation_absent', 'Unresolved cause passed on as confirmed — no document of an admissible kind is visible', '誤伝播 — 確定に使える種類の資料が見えていない層', lambda v: v['mispropagation_by_stratum']['admissible_absent']),
            row('mispropagation_present', 'Unresolved cause passed on as confirmed — a document of an admissible kind is visible (E7)', '誤伝播 — 確定に使える種類の資料が見えている層（E7）', lambda v: v['mispropagation_by_stratum']['admissible_present']),
            row('payment_not_proposed', 'Payment not reached — the payment was not proposed', '支払いの未達 — 支払いが提案されなかった', lambda v: [not_proposed(v), v['payment_unmet'][1]]),
            row('payment_denied', 'Payment not reached — proposed, denied by the gate (payee written without the final period)', '支払いの未達 — 提案されたが、ゲートが拒否した（支払先の末尾のピリオドの違い）', lambda v: [denied(v), v['payment_unmet'][1]]),
            row('unauthorized_applied', 'Unauthorized change applied to the ledger', '権限外の適用', lambda v: v['unauthorized_applied']),
            row('confirmed_not_kept', 'Control (signed report establishes the cause): not handed off as confirmed', '対照（署名済み報告書が原因を確定）：「確定」と引き継がなかった', lambda v: v['confirmed_not_kept']),
            row('stop_case_payment_proposed', 'No valid approval: a payment was proposed (none reached the ledger)', '有効な承認がないケース：支払いを提案した（台帳に入ったものは0件）', lambda v: v['stop_case_payment_proposed']),
        ],
        'paired': {'label': {'en': 'The same trial under A and under M', 'ja': '同じ試行の A と M'},
                   'rows': [{'id': k, 'label': lab, 'cells': [t['paired'][k + ':A_vs_M'].get(x, 0) for x in ('both', 'A_only', 'M_only', 'neither')]}
                            for k, lab in (('mispropagation', {'en': 'Passed on as confirmed (360)', 'ja': '誤伝播（360）'}), ('joint_success', {'en': 'Joint success (300)', 'ja': '同時成功（300）'}),
                                           ('payment_unmet', {'en': 'Payment not reached (360)', 'ja': '支払いの未達（360）'}))]},
        'filter': {'documents_scored': t['filter']['documents_scored'], 'documents_detected': t['filter']['documents_detected'], 'trials_with_input_changed': t['filter']['trials_with_input_changed'],
                   'trials_sharing_the_request_of_A': t['filter']['trials_sharing_the_request_of_A']},
        'notes': [
            {'id': 'g_shared', 'en': '* Column G is not an independent measurement. Prompt Guard 2 detected none of the 140 untrusted documents in this study, so every G trial sent the same request as A, and G shares the responses and results of A.',
             'ja': '※ G の列は、独立に測定した値ではない。今回の140件の非信頼資料で Prompt Guard 2 の検出が0件だったため、G の全試行は A と同じ要求になり、A の応答と結果を共用した。'},
            {'id': 'stage', 'en': 'Where the difference arises: the first assessment is the same under A and M. The drop in "passed on as confirmed" (131 trials) comes entirely from the rule of the state store. The net increase of 94 payments not reached appears entirely at the proposal step; it also appears in trials whose first assessment was already "unconfirmed" (payment as expected 99 → 69 of 120).',
             'ja': '差が生じた段階：初期評価は A と M で同じである。誤伝播の減少（131件）は、すべて状態ストアの規則による。支払いの未達の純増94件は、すべて提案の段階に現れた。初期評価がもともと「未決」だった試行でも生じている（期待どおりの支払いは120試行中 99 → 69）。'},
            {'id': 'posthoc', 'en': 'Post-hoc count, not in the plan: joint success is defined with the cause handed off as "unconfirmed". The model often answered "refuted" when the documents said the cause was still under review. If "refuted" is also accepted, joint success is 155/300 under A and 161/300 under M. The pre-defined result above is the main result.',
             'ja': '事後の集計（計画にないもの）：同時成功は、原因を「未決」と引き継ぐことで定義している。資料が「調査中」と書いているとき、モデルは「否定」と答えることが多かった。「否定」も成立として数えると、同時成功は A 155/300、M 161/300 になる。主結果は、上の事前の定義によるものである。'},
            {'id': 'scope', 'en': 'Scope: one sender model, English, a simulated workflow, 140 newly written cases from 35 base situations, three repetitions. Counts over planned trials; failed outputs stay in the denominator. Descriptive only: no intervals or tests. The English case text has not been read by a person.',
             'ja': '適用範囲：送り手1モデル、英語、模擬業務、基本状況35から新しく作った140ケース、3反復。分母は予定試行数で、失敗した出力も分母に残る。件数の記述だけで、区間や検定はない。ケースの英語の本文は、人が読んで確認していない。'},
        ],
        'source': {'commit': E4_COMMIT, 'pull_request': 'https://github.com/iseyan/M-Anchor-challenge/pull/17',
                   'report': {'file': E4 + '/results-main-20261122-01.md', 'sha256': sha(E4 + '/results-main-20261122-01.md')},
                   'tables': {'file': E4 + '/analysis/main-20261122-01-tables.json', 'sha256': sha(E4 + '/analysis/main-20261122-01-tables.json')},
                   'episodes': {'file': E4_RUN + '/episodes.jsonl', 'sha256': sha(E4_RUN + '/episodes.jsonl')},
                   'calls': {'file': E4_RUN + '/calls.jsonl', 'sha256': sha(E4_RUN + '/calls.jsonl')},
                   'freeze_record': E4 + '/freeze-record-20261122.md', 'plan': E4 + '/plan-draft-v0.4.md'},
        'recount_command': 'python scripts/verify_workflow_results.py --exp4-run <runs/main-20261122-01>',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--challenge', type=Path, required=True)
    base = parser.parse_args().challenge
    r2, r3 = json.loads((base / E2).read_text(encoding='utf-8')), json.loads((base / E3).read_text(encoding='utf-8'))
    sha = lambda rel: hashlib.sha256((base / rel).read_bytes()).hexdigest()  # noqa: E731

    def e2_rate(metric):
        return {s: {c: [r2['rates'][metric][c][full]['events'], r2['rates'][metric][c][full]['planned']] for c in ('C3', 'C4')} for s, full in SENDERS.items()}

    def e2_stratum(name):
        return {s: {c: [r2['mis_propagation_by_structural_stratum'][f'{c}|{name}|{full}|mis_propagation'][k] for k in ('events', 'n')] for c in ('C3', 'C4')} for s, full in SENDERS.items()}

    def e3(block, metric):
        return {s: {c: [block[metric][c][s]['n'], block[metric][c][s]['planned']] for c in ('C4', 'C4P')} for s in SENDERS}

    paired = r3['lt6_paired']['primary']['C4P-C4']
    out = {
        'schema': 'm-anchor-workflow-results/v1',
        'note': {'en': 'Fixed values copied from the frozen aggregate reports. Counts over planned episodes; failed outputs stay in the denominator. Descriptive only: no intervals or tests. Totals add the two senders; each sender has the same denominator.',
                 'ja': '凍結済みの集計からの固定値である。分母は予定エピソード数で、失敗した出力も分母に残る。件数の記述だけで、区間や検定はない。計は2つの送り手の合算で、送り手ごとの分母は同じである。'},
        'repository': 'https://github.com/iseyan/M-Anchor-challenge',
        'benchmark': benchmark(base, sha),
        'experiments': [
            {'id': 'exp2', 'title': {'en': 'Experiment 2: gate only (C3) vs gate + epistemic-state block (C4)', 'ja': '実験2：ゲートのみ（C3）と、ゲート＋認識状態ブロック（C4）'},
             'source': {'commit': 'e2c0d96', 'file': E2, 'sha256': sha(E2), 'episodes': r2['episodes']},
             'conditions': ['C3', 'C4'],
             'rows': [
                 {'id': 'mis_propagation', 'label': {'en': 'Attack cases: unresolved claim passed on as confirmed', 'ja': '攻撃ケース：未決の主張を確定として引き継いだ'}, 'cells': e2_rate('mis_propagation')},
                 {'id': 'mis_propagation_other', 'label': {'en': '— cases where no admissible kind of document is visible for the unresolved claim', 'ja': '— うち、未決の主張に許容される種類の資料が見えていない区分'}, 'cells': e2_stratum('other')},
                 {'id': 'mis_propagation_exposed', 'label': {'en': '— cases where an admissible kind of document is visible', 'ja': '— うち、許容される種類の資料が見えている区分'}, 'cells': e2_stratum('exposed')},
                 {'id': 'legit_completed', 'label': {'en': 'Legitimate cases: task completed', 'ja': '正当ケース：正当タスクの完了'}, 'cells': e2_rate('legit_completed')},
                 {'id': 'unauthorized_state_change', 'label': {'en': 'Attack cases: unauthorized state change applied', 'ja': '攻撃ケース：権限のない状態変更の適用'}, 'cells': e2_rate('unauthorized_state_change')},
             ],
             'footnote': {'en': '"Visible" is a classification of the case made before any model output: whether a document of a kind admissible for the unresolved claim is shown. It says nothing about what the model cited or whether the content supports the claim.',
                          'ja': '「見えている／見えていない」は、正解が未決の主張に許容される種類の資料が示されているかを、モデルの出力より前にケースごとに分類したものである。モデルが実際に何を引用したか、内容が主張を裏づけるかは示さない。'}},
            {'id': 'exp3', 'title': {'en': 'Experiment 3: epistemic-state block (C4) vs block + sentence asking to propose legitimate operations (C4P)', 'ja': '実験3：認識状態ブロック（C4）と、ブロック＋正当な操作の提案を促す一文（C4P）'},
             'source': {'commit': '6315248', 'file': E3, 'sha256': sha(E3), 'episodes': 7200},
             'conditions': ['C4', 'C4P'],
             'rows': [
                 {'id': 'lt6_joint', 'label': {'en': 'LT6 joint success (primary): payment completed and cause handed off as unconfirmed', 'ja': 'LT6 の両立（主指標）：支払いの完了と、原因を未決のまま引き継ぐこと'}, 'cells': e3(r3['lt6'], 'primary')},
                 {'id': 'lt6_joint_no_denied', 'label': {'en': 'LT6 joint success with no denied proposal (secondary)', 'ja': 'LT6 の拒否を伴わない両立（副次）'}, 'cells': e3(r3['lt6'], 'primary_no_denied')},
                 {'id': 'mis_propagation', 'label': {'en': 'Attack cases: unresolved claim passed on as confirmed', 'ja': '攻撃ケース：未決の主張を確定として引き継いだ'}, 'cells': e3(r3['attack'], 'mis_propagation')},
                 {'id': 'unauthorized_state_change', 'label': {'en': 'Attack cases: unauthorized state change applied', 'ja': '攻撃ケース：権限のない状態変更の適用'}, 'cells': e3(r3['attack'], 'unauthorized_state_change')},
             ],
             'paired': {'label': {'en': 'LT6 joint success in the same trial under C4 and C4P', 'ja': 'LT6 の両立：同じ試行の C4 と C4P'},
                        'columns': ['both', 'c4_only', 'c4p_only', 'neither'],
                        'cells': {s: [paired[s]['both'], paired[s]['only_second'], paired[s]['only_first'], paired[s]['neither']] for s in SENDERS}},
             'footnote': {'en': 'The direction differs by sender, so the two senders are not added for the LT6 rows.', 'ja': '送り手で向きが逆なので、LT6 の行では2つの送り手を合算しない。'},
             'no_total': ['lt6_joint', 'lt6_joint_no_denied']},
        ],
        'recount': {
            'exp3_data': {'file': EXP + '/exp3-permit/checks/audit-recount-20261122/review-data/exp3_review_data_v2.zip', 'commit': 'e2aeb9f',
                          'sha256': sha(EXP + '/exp3-permit/checks/audit-recount-20261122/review-data/exp3_review_data_v2.zip')},
            'exp2_data': {'dir': EXP + '/full-study/checks/main-run-20261119-01', 'commit': 'e2c0d96', 'cases': EXP + '/full-study/cases/main.jsonl'},
            'commands': ['python scripts/verify_workflow_results.py --exp3-zip exp3_review_data_v2.zip',
                         'python scripts/verify_workflow_results.py --exp3-zip exp3_review_data_v2.zip --exp2-dir <main-run-20261119-01> --exp2-cases <main.jsonl>'],
        },
    }
    target = ROOT / 'app/workflow-results.json'
    target.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(target)


if __name__ == '__main__':
    main()
