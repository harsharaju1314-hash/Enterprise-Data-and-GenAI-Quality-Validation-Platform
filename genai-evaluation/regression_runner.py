"""
GenAI Regression Testing Harness
Runs automated regression checks whenever prompt templates, embedding models, or document chunks change.
"""

import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from run_eval import run_evaluation

def main():
    print("Executing GenAI Regression Test Gate...")
    success = run_evaluation()
    if not success:
        print("[FAIL] GenAI Regression Gate Failed: Detected regressions in accuracy, groundedness, or guardrails.")
        sys.exit(1)
    else:
        print("[PASS] GenAI Regression Gate Passed: All regression benchmark tests validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
