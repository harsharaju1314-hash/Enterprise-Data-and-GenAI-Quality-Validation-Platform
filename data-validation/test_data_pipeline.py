"""
Pytest Test Suite for Data Pipeline Quality Validation
"""

import os
import pytest
from data_quality_engine import DataQualityEngine

@pytest.fixture(scope="module")
def dq_engine():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.join(base_dir, "data-pipeline", "enterprise_analytics.db")
    return DataQualityEngine(db_path)

def test_completeness_checks(dq_engine):
    results = dq_engine.validate_completeness()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Completeness failures: {failures}"

def test_accuracy_checks(dq_engine):
    results = dq_engine.validate_accuracy()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Accuracy failures: {failures}"

def test_consistency_checks(dq_engine):
    results = dq_engine.validate_consistency()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Consistency failures: {failures}"

def test_uniqueness_checks(dq_engine):
    results = dq_engine.validate_uniqueness()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Uniqueness failures: {failures}"

def test_validity_checks(dq_engine):
    results = dq_engine.validate_validity()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Validity failures: {failures}"

def test_timeliness_checks(dq_engine):
    results = dq_engine.validate_timeliness()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Timeliness failures: {failures}"

def test_source_to_target_reconciliation(dq_engine):
    results = dq_engine.validate_reconciliation()
    failures = [r for r in results if r["status"] != "PASS"]
    assert len(failures) == 0, f"Reconciliation failures: {failures}"
