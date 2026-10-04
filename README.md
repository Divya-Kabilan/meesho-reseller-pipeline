# Meesho Reseller Performance & Growth Analytics Pipeline

This project is a fully offline Meesho reseller monitoring pipeline. It uses a fixed seeded dataset, SQL aggregations, a guarded Python growth engine, masking checks, and a mock human-in-the-loop agent. There is no API key, no paid service, and no network dependency required.

## Workflow overview
- Part 1: generate the reseller/order dataset and compute SQL outputs.
- Part 2: validate the feed and compute month-on-month growth logic.
- Part 3: enforce masking and document the narrative prompt pack.
- Part 4: run the agent workflow with guardrails and hard-stop validation.

## How to regenerate the dataset
Run:

```bash
python data/generate_dataset.py
```

This creates:
- `data/resellers.csv`
- `data/orders.csv`
- `data/meesho_reseller.db`

## How to run each part in order
1. Generate dataset

```bash
python data/generate_dataset.py
```

2. Run SQL queries and export CSV outputs

```bash
python part1_sql/run_queries.py
```

3. Run growth-engine tests

```bash
python part2_engine/test_growth_engine.py
```

4. Run masking checks

```bash
python part3_narrative/masking.py
```

5. Run the end-to-end pipeline

```bash
python main.py
```

## How the parts connect
- Part 1 → Part 2: the SQL output (`part1_sql/output/monthly_category_revenue.csv`) is the direct feed to the Python growth and validation logic.
- Part 2 → Part 3: the growth engine provides the verified numbers used in narrative prompts and guardrail checks.
- Part 3 → Part 4: the masking policy and prompt pack are used to ensure all drafted messages avoid raw reseller names and only use verified numbers.
- Part 4 integrates all three into a human-in-the-loop agent that validates input, computes MoM changes, drafts messages, and hard-stops on invalid feeds.

## Zero API key requirement
This project runs fully offline using deterministic SQL and Python logic only. No external service, API key, or paid account is required.

## Repository structure
```text
meesho-reseller-pipeline/
├── main.py
├── README.md
├── data/
│   ├── generate_dataset.py
│   ├── meesho_reseller.db
│   ├── orders.csv
│   └── resellers.csv
├── part1_sql/
│   ├── output/
│   ├── queries.sql
│   └── run_queries.py
├── part2_engine/
│   ├── fixtures/
│   ├── growth_engine.py
│   └── test_growth_engine.py
├── part3_narrative/
│   ├── masking.py
│   ├── narrative_report.md
│   └── prompt_pack.md
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
└── .gitignore
```

## References used
- Python standard library documentation for `csv`, `sqlite3`, `subprocess`, and `unittest`.
- This project intentionally avoids any external LLM/API dependency.