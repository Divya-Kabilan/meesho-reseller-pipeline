import csv
from typing import List, Tuple


def mom_growth(previous: float, current: float) -> float:
  """Calculates Month-on-Month growth percentage rounded to 2 decimal places."""
  if previous == 0:
    raise ValueError("Previous value cannot be zero for MoM growth calculation.")
  return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
  """Determines if a growth percentage triggers a threshold alert.

  Returns:
      "flagged": if abs(mom_pct) > threshold
      "not_flagged": if abs(mom_pct) < threshold
      "escalate_exact_boundary": if abs(mom_pct) == threshold exactly
  """
  abs_mom = abs(mom_pct)
  if abs_mom > threshold:
    return "flagged"
  elif abs_mom < threshold:
    return "not_flagged"
  else:
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> Tuple[bool, List[str]]:
  """Validates a monthly category revenue CSV feed for structural and numeric integrity.

  Checks for missing category, missing revenue, non-numeric revenue, and negative revenue.
  Returns (True, []) if valid, or (False, error_messages) if invalid.
  """
  errors = []

  with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    # Line numbers: Header is line 1, first data row is line 2
    for line_num, row in enumerate(reader, start=2):
      month = row.get("month", "").strip()
      category = row.get("category", "").strip()
      revenue_str = row.get("revenue", "").strip()

      # Rule 1: Check missing category
      if not category:
        errors.append(f"line {line_num}: missing category (month={month})")
        continue

      # Rule 2: Check missing revenue
      if revenue_str == "":
        errors.append(f"line {line_num}: missing revenue (category={category})")
        continue

      # Rule 3: Check parseable float
      try:
        revenue_val = float(revenue_str)
      except ValueError:
        errors.append(
            f"line {line_num}: revenue not numeric: {revenue_str!r}"
        )
        continue

      # Rule 4: Check negative revenue
      if revenue_val < 0:
        errors.append(
            f"line {line_num}: negative revenue ({revenue_val}) for"
            f" category={category}"
        )

  if len(errors) == 0:
    return (True, [])
  else:
    return (False, errors)