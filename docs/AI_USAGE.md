# AI-Assisted Development Log

## Intent
AI was used as an engineering accelerator, not an authority. Product scope, architecture, data correctness, security boundaries, and acceptance criteria were explicitly reviewed by the developer.

## Good uses of AI in this assessment
- Generate alternative requirement interpretations and identify ambiguities.
- Challenge architecture choices for a 10,000-employee workload.
- Scaffold repetitive Django/Next.js structures.
- Suggest edge cases for salary validation, CSV parsing, pagination, and aggregation.
- Review code for duplicated rules, unsafe money handling, N+1 behavior, and missing tests.
- Improve documentation clarity and demo structure.

## Verification workflow
For AI-proposed code:
1. Read the diff before accepting it.
2. Reduce unnecessary abstractions/dependencies.
3. Verify money operations use `Decimal` and multi-currency aggregates are normalized.
4. Add or update deterministic tests for the behavior.
5. Run backend tests and Python compilation; run frontend lint/build in a fully installed environment.
6. Keep commits small enough that a reviewer can follow the evolution.

## Example prompts / instructions
- "Turn this vague HR salary-management brief into one page of MVP requirements. Identify assumptions and deliberately excluded scope."
- "For 10,000 employees, challenge whether microservices/caching are justified. Prefer the simplest architecture that meets the load."
- "Review this Django model for financial-data correctness, especially Decimal use, audit history, and mixed currencies."
- "Generate edge-case tests for CSV employee salary import. Do not test framework internals."
- "Review this employee-list API for client-side over-fetching, unstable pagination, and unsafe ordering fields."

## Examples of AI suggestions intentionally rejected
- Adding Kafka/Redis/Celery without a measured asynchronous workload.
- Summing local salaries across INR/USD/GBP/EUR as one number.
- Adding an LLM chatbot simply because the role mentions AI.
- Adding broad authentication claims without implementing production-grade SSO/RBAC.

## Disclosure
The final submission should list the actual AI products used by the candidate during implementation (for example ChatGPT/Codex/Cursor/Claude) and retain any relevant prompt transcripts if Incubyte requests them.
