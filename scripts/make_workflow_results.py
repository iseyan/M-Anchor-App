"""Rebuild app/workflow-results.json from the frozen aggregate reports of M-Anchor-challenge.

  python scripts/make_workflow_results.py --challenge PATH_TO/M-Anchor-challenge

Not part of CI: it needs a checkout of the other repository. Counts are copied from the frozen
reports (Experiment 2: report-final.json, Experiment 3: report3.json); nothing is recomputed here.
To recompute them from episode data, use scripts/verify_workflow_results.py.
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
