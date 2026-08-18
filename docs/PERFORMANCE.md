# Performance Considerations

## Current target: 10,000 employees
- All employee listing is server-paginated (default 25, maximum controlled by backend).
- Filtering/searching happen in the database; the browser never receives the full data set.
- Indexes cover business key, department, country, job level, normalized salary, and common combinations.
- Aggregates use database `COUNT`, `SUM`, and `AVG`; only median materializes one salary column.
- Seed/import uses `bulk_create(..., batch_size=1000)`.
- Detail/history queries prefetch only the required relation when useful.

## Expected bottlenecks before compute capacity
1. Unbounded searches and expensive wildcard scans as employee count grows.
2. Repeated dashboard aggregates at much larger datasets.
3. Very large CSV files processed synchronously.
4. Cross-region database latency if UI/API/data are deployed far apart.

## Growth strategy
Measure before adding infrastructure. Likely progression: query analysis/index tuning → PostgreSQL trigram/full-text search if needed → cached/materialized reporting → async import jobs → read replicas. Microservices are not the first scaling tool.
