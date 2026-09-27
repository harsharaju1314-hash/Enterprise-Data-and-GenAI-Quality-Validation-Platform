"""
AI Guardrails & Safety Filter Module
Protects against Prompt Injection, PII Leaks, Out-of-Scope Queries, and Database Schema Exfiltration.
"""

import re
from typing import Dict, Any

class AIGuardrails:
    INJECTION_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"disregard (all )?prior rules",
        r"you are now (a|an)",
        r"system prompt",
        r"jailbreak",
        r"override system instructions",
        r"act as an unrestricted ai"
    ]

    SENSITIVE_PATTERNS = [
        r"drop table",
        r"dump (all )?(database|tables|passwords|credentials)",
        r"credit card number",
        r"social security",
        r"admin password",
        r"select \* from"
    ]

    OUT_OF_SCOPE_PATTERNS = [
        r"weather",
        r"forecast",
        r"write a poem",
        r"stock price",
        r"recipe",
        r"who is the president"
    ]

    @classmethod
    def inspect_prompt(cls, prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower().strip()

        # 1. Prompt Injection
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, p_lower, re.IGNORECASE):
                return {
                    "is_safe": False,
                    "guardrail_type": "PROMPT_INJECTION",
                    "reason": f"Detected prompt injection pattern: '{pattern}'",
                    "safe_response": "I am unable to process this instruction. I operate strictly within enterprise policy guidelines."
                }

        # 2. Database Schema / Sensitive Exfiltration
        for pattern in cls.SENSITIVE_PATTERNS:
            if re.search(pattern, p_lower, re.IGNORECASE):
                return {
                    "is_safe": False,
                    "guardrail_type": "SENSITIVE_DATA_RESTRICTION",
                    "reason": "Direct database schemas, raw security credentials, and PII are restricted by the Enterprise Data Access Policy.",
                    "safe_response": "Access Denied: Inquiries regarding direct database schemas, raw security credentials, or plain text PII are restricted by the Enterprise Data Access Policy."
                }

        # 3. Out of Scope Queries
        for pattern in cls.OUT_OF_SCOPE_PATTERNS:
            if re.search(pattern, p_lower, re.IGNORECASE):
                return {
                    "is_safe": False,
                    "guardrail_type": "OUT_OF_SCOPE",
                    "reason": "Query is outside enterprise policy and operational domain.",
                    "safe_response": "This query is outside the scope of Enterprise Operations & Policy Assistance."
                }

        return {
            "is_safe": True,
            "guardrail_type": "NONE",
            "reason": "Prompt passed all safety guardrails.",
            "safe_response": None
        }
