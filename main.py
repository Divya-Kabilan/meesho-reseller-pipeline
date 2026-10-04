import json
import os
import subprocess
import sys

from part3_narrative.masking import alias_for, assert_no_raw_names_leak
from part4_agent.mock_agent_runner import run as run_agent


def run_step(description, command):
  print("\n" + "=" * 70)
  print(f"  RUNNING: {description}")
  print("=" * 70)
  result = subprocess.run(command, shell=True)
  if result.returncode != 0:
    print(f"\nERROR encountered during: {description}")
    sys.exit(result.returncode)


def main():
  print("STARTING MEESHO RESELLER PIPELINE END-TO-END EXECUTION")

  # 1. Dataset Generation
  run_step("Data Generation", "python data/generate_dataset.py")

  # 2. SQL Execution
  run_step("Part 1 - SQL Business Engine", "python part1_sql/run_queries.py")

  # 3. Growth Engine Unit Tests
  run_step(
      "Part 2 - Python Growth Engine Tests",
      "python part2_engine/test_growth_engine.py",
  )

  # 4. Part 3 Masking Validation
  print("\n" + "=" * 70)
  print("  RUNNING: Part 3 - Masking & Guardrail Validation")
  print("=" * 70)
  assert alias_for("RS019") == "ALIAS-19"
  raw_names = ["Mumbai Reseller 1"]
  assert (
      assert_no_raw_names_leak("Top reseller ALIAS-19", raw_names) is True
  )
  assert (
      assert_no_raw_names_leak("Top reseller Mumbai Reseller 1", raw_names)
      is False
  )
  print("Part 3 Masking & PII Guardrails verified!")

  # 5. Part 4 Agent Scenarios
  print("\n" + "=" * 70)
  print("  RUNNING: Part 4 - Agent Runner Verification")
  print("=" * 70)

  # Corrupted Feed Scenario
  corrupted_res = run_agent(
      "July",
      "part1_sql/output/monthly_category_revenue.csv",
      "part2_engine/fixtures/corrupted_feed.csv",
  )
  assert corrupted_res["validation_status"] == "invalid"
  assert corrupted_res["action_taken"] == "hard_stop"
  assert len(corrupted_res["validation_errors"]) == 3
  print("Part 4 Hard Stop Scenario Verified!")

  # May Scenario
  may_res = run_agent(
      "May",
      "part1_sql/output/monthly_category_revenue.csv",
      "part1_sql/output/monthly_category_revenue.csv",
  )
  assert may_res["validation_status"] == "valid"
  assert [item["category"] for item in may_res["flagged_categories"]] == [
      "Ethnic Wear",
      "Western Wear",
      "Kids Wear",
  ]
  assert set(may_res["suppressed_categories"]) == {
      "Beauty & Personal Care",
      "Home & Kitchen",
  }
  assert len(may_res["flagged_categories"]) == 3
  print("Part 4 May Scenario Verified!")

  # June Scenario
  june_res = run_agent(
      "June",
      "part1_sql/output/monthly_category_revenue.csv",
      "part1_sql/output/monthly_category_revenue.csv",
  )
  assert june_res["validation_status"] == "valid"
  assert [item["category"] for item in june_res["flagged_categories"]] == [
      "Ethnic Wear",
      "Home & Kitchen",
      "Kids Wear",
  ]
  assert june_res["suppressed_categories"] == ["Western Wear"]
  assert "Beauty & Personal Care" not in [
      item["category"] for item in june_res["flagged_categories"]
  ]
  assert "Beauty & Personal Care" not in june_res["suppressed_categories"]
  print("Part 4 June Scenario Verified!")

  print("\n" + "=" * 70)
  print("PIPELINE EXECUTION SUCCESSFUL! All parts verified and ready.")
  print("=" * 70 + "\n")


if __name__ == "__main__":
  main()