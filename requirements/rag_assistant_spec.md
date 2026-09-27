# GenAI & RAG Knowledge Assistant Specification

## 1. System Architecture
```text
User Query
    ↓
AI Guardrails Safety Layer (Injection / PII / Scope Validation)
    ↓
Context Retriever (Vector Chunks / Approved Markdown Documents)
    ↓
Grounded LLM Generator (Constrained to Retrieved Context)
    ↓
Evaluation & Verification Framework (Relevance, Groundedness, Security)
    ↓
User Response with Evidence Citations
```

## 2. Approved Knowledge Base Documents
1. `Customer Support Policy.md`
2. `Data Access Policy.md`
3. `Escalation Policy.md`
4. `Refund Policy.md`
5. `Service Request Policy.md`

## 3. GenAI Quality Engineering Testing Pillars
- **Functional Correctness**: Responses precisely convey policy facts (e.g. refund approval limits, SLA windows).
- **Relevance**: Answers directly resolve the question asked without extraneous fluff.
- **Groundedness / Faithfulness**: All factual assertions are strictly backed by retrieved policy context.
- **Hallucination Prevention**: Explicit refusal on topics outside approved knowledge base.
- **Retrieval Precision & Recall**: Ensuring the most relevant section chunks are fetched.
- **Prompt Variations**: Robustness against lexical and syntactic query variations.
- **Guardrail Effectiveness**: Complete interception of jailbreaks, prompt injections, and database exfiltration attempts.
- **Factual Consistency**: Stable, deterministic responses across equivalent query phrasings.
