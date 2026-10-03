import os
import subprocess
import sys


def run_step(description, command):
  print("\n" + "=" * 70)
  print(f"  RUNNING: {description}")
  print("=" * 70)
  result = subprocess.run(command, shell=True)
  if result.returncode != 0:
    print(f"\n❌ Error encountered during: {description}")
    sys.exit(result.returncode)


def main():
  print("🚀 STARTING MEESHO RESELLER PIPELINE END-TO-END EXECUTION")

  # Step 1: Generate Dataset & SQLite Database
  run_step(
      "Part 1 - Synthetic Dataset Generation", "python data/generate_dataset.py"
  )

  # Step 2: Run SQL Queries & Export CSV Artifacts
  run_step("Part 1 - SQL Analytics Execution", "python part1_sql/run_queries.py")

  # Step 3: Run Growth Engine Unit Tests
  run_step(
      "Part 2 - Python Growth Engine Unit Tests",
      "python part2_engine/test_growth_engine.py",
  )

  print("\n" + "=" * 70)
  print("🎉 PIPELINE EXECUTION SUCCESSFUL! All artifacts generated & tested.")
  print("=" * 70 + "\n")


if __name__ == "__main__":
  main()