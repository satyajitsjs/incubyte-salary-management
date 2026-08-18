# Trade-offs and Deliberate Decisions

| Decision | Chosen approach | Why | Upgrade path |
|---|---|---|---|
| Architecture | Modular monolith | 10k rows do not justify distributed systems | Split reporting/import only after measured need |
| Backend | Django + DRF | Strong relational/domain primitives, mature testing, fast delivery | Async workers for genuinely long jobs later |
| Database | PostgreSQL deploy; SQLite local | Real relational deployment plus zero-config review | Managed PostgreSQL HA/read replicas if needed |
| Reporting currency | Persist normalized USD + FX snapshot | Avoid invalid mixed-currency sums; preserves auditability | Versioned finance-approved FX table |
| Salary history | Immutable append-only row on salary change | Simple audit trail and interview discussion value | Full event/audit model with actor/approval IDs |
| Median | Exact in-process median of one selected column | 10k values is small and database-portable | PostgreSQL percentile/materialized reporting |
| CSV import | Validate-all then transactional batch insert | No partial corruption; clear failures | Background job for very large files |
| Authentication | Not simulated | Synthetic assessment data only; fake auth can mislead | OIDC/SSO + RBAC before real data |
| LLM feature | Excluded | Deterministic reporting is safer and sufficient for stated need | NL-to-approved-query layer if clarified |
| Caching | None | Adds invalidation complexity with little benefit at current scale | Cache measured hot aggregate endpoints |

## What I would build next
1. SSO + least-privilege HR roles and actor-aware audit logs.
2. Finance-owned FX rate table with effective dates.
3. CSV preview/dry-run UI and export.
4. Salary change approval workflow if policy requires it.
5. Observability: structured logs, request metrics, tracing, error reporting.
6. Accessibility and end-to-end browser tests.
