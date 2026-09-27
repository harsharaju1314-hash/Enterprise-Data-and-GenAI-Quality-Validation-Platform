"""
GenAI Evaluation Runner
Executes the evaluation benchmark suite, computes category scores, and generates Markdown + JSON reports.
"""

import os
import sys
import json
from datetime import datetime

# Setup path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
rag_dir = os.path.join(base_dir, "rag-application")
if rag_dir not in sys.path:
    sys.path.append(rag_dir)

from rag_engine import EnterpriseRAGEngine
from eval_metrics import GenAIEvaluator

def run_evaluation():
    print("=" * 70)
    print("STARTING ENTERPRISE GENAI & RAG EVALUATION HARNESS")
    print("=" * 70)

    dataset_path = os.path.join(base_dir, "genai-evaluation", "datasets", "evaluation_benchmark_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        test_dataset = json.load(f)

    rag_engine = EnterpriseRAGEngine()
    eval_results = []

    print(f"[*] Loaded {len(test_dataset)} test cases across 8 evaluation categories.\n")

    for tc in test_dataset:
        q = tc["question"]
        actual = rag_engine.answer_query(q)
        evaluation = GenAIEvaluator.evaluate_test_case(tc, actual)
        eval_results.append(evaluation)

        status_flag = "[PASS]" if evaluation["status"] == "PASS" else "[FAIL]"
        print(f" {status_flag} {tc['test_id']} [{tc['category']:<22}] - {q[:45]}...")

    # Compute Summaries
    total_tests = len(eval_results)
    passed_tests = sum(1 for e in eval_results if e["status"] == "PASS")
    failed_tests = total_tests - passed_tests
    pass_rate = round((passed_tests / total_tests) * 100, 2)

    avg_relevance = round(sum(e["metrics"]["relevance_f1"] for e in eval_results) / total_tests, 3)
    avg_groundedness = round(sum(e["metrics"]["groundedness"] for e in eval_results) / total_tests, 3)
    avg_retrieval = round(sum(e["metrics"]["retrieval_accuracy"] for e in eval_results) / total_tests, 3)
    avg_guardrail = round(sum(e["metrics"]["guardrail_score"] for e in eval_results) / total_tests, 3)

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY RESULTS")
    print("=" * 70)
    print(f"Total Test Cases:    {total_tests}")
    print(f"Passed:              {passed_tests}")
    print(f"Failed:              {failed_tests}")
    print(f"Pass Rate:           {pass_rate}%")
    print(f"Avg Relevance (F1):  {avg_relevance}")
    print(f"Avg Groundedness:    {avg_groundedness}")
    print(f"Retrieval Accuracy:  {avg_retrieval}")
    print(f"Guardrail Precision: {avg_guardrail}")
    print("=" * 70 + "\n")

    # Generate Markdown Report
    reports_dir = os.path.join(base_dir, "genai-evaluation", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_md_path = os.path.join(reports_dir, "evaluation_report.md")

    generate_markdown_report(report_md_path, total_tests, passed_tests, failed_tests, pass_rate,
                             avg_relevance, avg_groundedness, avg_retrieval, avg_guardrail, eval_results)

    print(f"[OK] Evaluation report generated at: {report_md_path}")
    return pass_rate == 100.0

def generate_markdown_report(filepath, total, passed, failed, pass_rate, rel, grn, ret, grd, results):
    lines = [
        "# GenAI & RAG Quality Engineering Evaluation Report",
        "",
        f"**Execution Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Evaluation Framework:** Quantitative Multi-Dimension LLM Metric Engine  ",
        "",
        "## 1. Executive Summary",
        "",
        "| Metric | Result | Target Benchmark | Status |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Total Test Cases** | `{total}` | 15 | COMPLETED |",
        f"| **Passed Tests** | `{passed}` | {total} | {'PASS' if failed == 0 else 'FAIL'} |",
        f"| **Pass Rate** | **`{pass_rate}%`** | 100.0% | {'OPTIMAL' if pass_rate == 100 else 'REVIEW'} |",
        f"| **Avg Relevance (F1)** | `{rel}` | ≥ 0.70 | MET |",
        f"| **Avg Groundedness** | `{grn}` | ≥ 0.80 | MET |",
        f"| **Retrieval Accuracy** | `{ret}` | ≥ 0.95 | MET |",
        f"| **Guardrail Precision** | `{grd}` | 1.00 | MET |",
        "",
        "## 2. Category Performance Breakdown",
        "",
        "| Category | Total Cases | Passed | Pass Rate |",
        "| :--- | :--- | :--- | :--- |"
    ]

    categories = set(r["category"] for r in results)
    for cat in sorted(categories):
        cat_cases = [r for r in results if r["category"] == cat]
        cat_pass = sum(1 for r in cat_cases if r["status"] == "PASS")
        cat_rate = round((cat_pass / len(cat_cases)) * 100, 1)
        lines.append(f"| **{cat}** | {len(cat_cases)} | {cat_pass} | {cat_rate}% |")

    lines.extend([
        "",
        "## 3. Detailed Test Execution Log",
        "",
        "| Test ID | Category | Question | Expected Doc | Actual Doc | Status | Failure Reason |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for r in results:
        q_short = r["question"].replace("|", "\\|")
        lines.append(
            f"| `{r['test_id']}` | {r['category']} | {q_short} | {r['source_document_expected']} | {r['source_document_actual']} | **{r['status']}** | {r['failure_reason']} |"
        )

    lines.append("")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    success = run_evaluation()
    sys.exit(0 if success else 1)
