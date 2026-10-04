import csv
import json
import os
import sys

# Add parent directory to path to import part2_engine
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed
from part3_narrative.masking import fill_prompt_template

MONTH_ORDER = ["April", "May", "June"]
PREVIOUS_MONTH = {"May": "April", "June": "May", "July": "June"}


def load_category_revenues(
    csv_path: str, month: str | None = None
) -> dict[str, float]:
  """Load revenue by category for one month, or for an entire multi-month feed."""
  category_rev = {}
  with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      row_month = (row.get("month") or "").strip()
      if month is not None and row_month and row_month != month:
        continue
      category = (row.get("category") or "").strip()
      revenue_value = (row.get("revenue") or "").strip()
      if not category or not revenue_value:
        continue
      category_rev[category] = float(revenue_value)
  return category_rev


def draft_message(
    category: str, mom_pct: float, prev_rev: float, curr_rev: float, month: str
) -> str:
  return fill_prompt_template(
      category=category,
      mom_pct=mom_pct,
      previous_revenue=prev_rev,
      current_revenue=curr_rev,
      month=month,
  )


def run(
    month: str, previous_month_csv: str, current_month_csv: str
) -> dict:
  # Subtask 1: Validate incoming current month feed
  is_valid, errors = validate_feed(current_month_csv)

  # Subtask 2: Hard Stop if invalid
  if not is_valid:
    return {
        "run_month": month,
        "validation_status": "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "hard_stop",
    }

  prev_month = PREVIOUS_MONTH.get(month)
  if prev_month is None:
    raise ValueError(f"Unsupported month for comparison: {month}")

  prev_data = load_category_revenues(previous_month_csv, prev_month)
  curr_data = load_category_revenues(current_month_csv, month)

  if not prev_data:
    raise ValueError(f"No data found for previous month: {prev_month}")

  if not curr_data:
    raise ValueError(f"No data found for current month: {month}")

  flagged = []
  suppressed = []
  escalated = []

  # Subtask 3 & 4: Compute growth & classify
  for cat, curr_rev in curr_data.items():
    if cat not in prev_data:
      continue
    prev_rev = prev_data[cat]
    growth = mom_growth(prev_rev, curr_rev)
    status = is_flagged(growth)

    if status == "flagged":
      flagged.append({
          "category": cat,
          "mom_pct": growth,
          "previous_revenue": prev_rev,
          "current_revenue": curr_rev,
          "drafted": False,
          "message": None,
          "abs_growth": abs(growth),
      })
    elif status == "escalate_exact_boundary":
      escalated.append(cat)

  flagged.sort(key=lambda x: x["abs_growth"], reverse=True)

  final_flagged = []
  for idx, item in enumerate(flagged):
    item.pop("abs_growth", None)
    if idx < 3:
      item["drafted"] = True
      item["message"] = draft_message(
          item["category"],
          item["mom_pct"],
          item["previous_revenue"],
          item["current_revenue"],
          month,
      )
      final_flagged.append(item)
    else:
      suppressed.append(item["category"])

  return {
      "run_month": month,
      "validation_status": "valid",
      "validation_errors": [],
      "flagged_categories": final_flagged,
      "suppressed_categories": suppressed,
      "escalated_categories": escalated,
      "action_taken": "drafted_and_held_for_approval",
  }


if __name__ == "__main__":
  # Test May Run
  may_result = run(
      "May",
      "part1_sql/output/monthly_category_revenue.csv",
      "part1_sql/output/monthly_category_revenue.csv",
  )
  print(json.dumps(may_result, indent=2))