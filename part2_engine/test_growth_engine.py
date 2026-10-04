import sys
import os
import tempfile

# Set sys.path before importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
from growth_engine import mom_growth, is_flagged, validate_feed


class TestGrowthEngine(unittest.TestCase):

  def setUp(self):
    self.base_dir = os.path.dirname(os.path.abspath(__file__))
    self.corrupted_csv = os.path.join(
        self.base_dir, "fixtures", "corrupted_feed.csv"
    )
    self.valid_csv = os.path.join(
        self.base_dir, "fixtures", "monthly_category_revenue.csv"
    )

  # Test 1: April -> May Ethnic Wear revenue (+77.1%, flagged)
  def test_given_april_may_ethnic_wear_when_evaluated_then_flagged(self):
    prev_rev = 104520.77
    curr_rev = 185107.61
    growth = mom_growth(prev_rev, curr_rev)
    flag_status = is_flagged(growth)

    self.assertEqual(growth, 77.1)
    self.assertEqual(flag_status, "flagged")

  # Test 2: May -> June Beauty & Personal Care (+5.67%, not_flagged)
  def test_given_may_june_beauty_when_evaluated_then_not_flagged(self):
    prev_rev = 35542.11
    curr_rev = 37559.07
    growth = mom_growth(prev_rev, curr_rev)
    flag_status = is_flagged(growth)

    self.assertEqual(growth, 5.67)
    self.assertEqual(flag_status, "not_flagged")

  # Test 3: Synthetic exact boundary condition (8.0%, escalate_exact_boundary)
  def test_given_exact_threshold_boundary_when_evaluated_then_escalate(self):
    prev_rev = 100000.0
    curr_rev = 108000.0
    growth = mom_growth(prev_rev, curr_rev)
    flag_status = is_flagged(growth)

    self.assertEqual(growth, 8.0)
    self.assertEqual(flag_status, "escalate_exact_boundary")

  # Test 4: Corrupted feed fixture validation errors
  def test_given_corrupted_feed_when_validated_then_returns_exact_errors(self):
    is_valid, errors = validate_feed(self.corrupted_csv)

    self.assertFalse(is_valid)
    self.assertEqual(len(errors), 3)

    expected_errors = [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
    self.assertEqual(errors, expected_errors)

  # Extra Check: Valid feed passes with zero errors
  def test_given_valid_feed_when_validated_then_passes(self):
    is_valid, errors = validate_feed(self.valid_csv)
    self.assertTrue(is_valid)
    self.assertEqual(errors, [])

  def test_given_missing_n_orders_when_validated_then_rejected(self):
    csv_text = """month,category,revenue,n_orders
July,Ethnic Wear,98450.00,
"""
    with tempfile.NamedTemporaryFile("w", delete=False, newline="") as tmp:
      tmp.write(csv_text)
      tmp_path = tmp.name

    try:
      is_valid, errors = validate_feed(tmp_path)
      self.assertFalse(is_valid)
      self.assertEqual(errors, ["line 2: missing n_orders (category=Ethnic Wear)"])
    finally:
      os.unlink(tmp_path)


if __name__ == "__main__":
  unittest.main()