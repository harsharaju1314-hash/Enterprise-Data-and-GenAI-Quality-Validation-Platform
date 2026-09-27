"""
Run Reconciliation and Data Quality Suite CLI
Executes the data quality engine and prints structured reconciliation reports.
"""

import os
import sys
import json
from data_quality_engine import DataQualityEngine

def main():
    print("=" * 70)
    print("ENTERPRISE DATA PIPELINE QUALITY VALIDATION & RECONCILIATION")
    print("=" * 70)
    
    engine = DataQualityEngine()
    results = engine.run_all_validations()
    
    summary = results["summary"]
    print(f"\nExecution Summary:")
    print(f"Total Checks: {summary['total_checks']}")
    print(f"Passed:       {summary['passed']}")
    print(f"Failed:       {summary['failed']}")
    print(f"Pass Rate:    {summary['pass_rate_pct']}%\n")
    
    print("-" * 70)
    print(f"{'DIMENSION':<18} | {'CHECK NAME':<40} | {'STATUS'}")
    print("-" * 70)
    
    for dimension, checks in results["details"].items():
        for check in checks:
            name = check["check_name"]
            status = check["status"]
            print(f"{dimension:<18} | {name:<40} | {status}")
            
    print("=" * 70)
    if summary["failed"] > 0:
        print("[!] Validation completed with failures.")
        sys.exit(1)
    else:
        print("[OK] All Source-to-Target and Data Quality Validations PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
