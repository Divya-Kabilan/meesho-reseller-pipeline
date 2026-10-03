# Part 1 SQL - Explanation of Query 4

## Why `COUNT(*)` cannot be used to detect zero-match LEFT JOIN rows

In a SQL `LEFT JOIN`, when a record in the left table (`resellers`) has no matching records in the right table (`orders`), SQL produces a single result row where all columns coming from `orders` are set to `NULL`.

- `COUNT(*)` counts the number of **rows** returned by the join group, regardless of whether column values are `NULL`. Because the unmatched reseller still generates 1 joined row containing `NULL` values for the order fields, `COUNT(*)` evaluates to **1**.
- `COUNT(o.order_id)` specifically counts non-null values in the `order_id` column. Since `o.order_id` is `NULL` for an unmatched reseller, `COUNT(o.order_id)` correctly evaluates to **0**.

Therefore, when identifying unmatched records in a `LEFT JOIN`, using `COUNT(*)` will incorrectly report 1 row instead of 0. `COUNT(order_id)` or checking `WHERE order_id IS NULL` must be used instead.