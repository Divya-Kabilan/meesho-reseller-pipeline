# Meesho Reseller Performance & Growth Analytics Pipeline

An end-to-end, fully offline analytics pipeline designed to process reseller sales data, execute audited SQL aggregations, detect Month-on-Month (MoM) growth anomalies through a guarded Python engine, enforce masking policies, and run a human-in-the-loop agent workflow.

---

## 📁 Repository Structure

```text
meesho-reseller-pipeline/
├── main.py                         # Master orchestration runner
├── README.md                       # Comprehensive project documentation
├── data/
│   ├── generate_dataset.py         # Seeded dataset generator script
│   ├── meesho_reseller.db          # Generated SQLite database instance
│   ├── orders.csv                  # Raw order transactions (900 rows)
│   └── resellers.csv               # Reseller profiles (24 rows)
├── part1_sql/
│   ├── queries.sql                 # Pure SQL query suite
│   ├── run_queries.py              # SQL runner & CSV artifact exporter
│   └── output/                     # Output CSVs & SQL README
├── part2_engine/
│   ├── growth_engine.py            # MoM growth & feed validation engine
│   ├── test_growth_engine.py       # Pytest/Unittest suite
│   └── fixtures/                   # Test CSV fixtures (clean & corrupted)
├── part3_narrative/
│   ├── prompt_pack.md              # Stakeholder prompt templates
│   ├── narrative_report.md         # Worked narratives, self-scoring & chart rationale
│   └── masking.py                  # PII & reseller name masking functions
└── part4_agent/
    ├── agent_spec.md               # Agentic workflow specification
    └── mock_agent_runner.py        # Mock agent runner emitting structured JSON