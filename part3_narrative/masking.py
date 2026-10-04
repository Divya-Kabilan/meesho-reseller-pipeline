def alias_for(reseller_id: str) -> str:
  """Converts RS019 -> ALIAS-19."""
  return f"ALIAS-{reseller_id[3:]}"


def fill_prompt_template(
    category: str,
    mom_pct: float,
    previous_revenue: float,
    current_revenue: float,
    month: str,
) -> str:
  """Fill the Part 3 stakeholder alert template without inventing figures."""
  pct_text = f"{mom_pct:.2f}"
  return (
      f"ALERT [{month}]: {category} revenue changed by {pct_text}% MoM "
      f"(from INR {previous_revenue:.2f} to INR {current_revenue:.2f}). "
      "Held for regional manager approval."
  )


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
  """Returns False if any raw reseller name appears verbatim in text."""
  for name in reseller_names:
    if name in text:
      return False
  return True


# --- Unit Verification Tests ---
if __name__ == "__main__":
  # 1. Test alias generator
  assert alias_for("RS019") == "ALIAS-19", (
      f"Expected ALIAS-19, got {alias_for('RS019')}"
  )
  assert alias_for("RS006") == "ALIAS-06", (
      f"Expected ALIAS-06, got {alias_for('RS006')}"
  )

  # 2. Test PII leak detection
  raw_names = [
      "Mumbai Reseller 1",
      "Mumbai Reseller 4",
      "Hyderabad Reseller 6",
      "Lucknow Reseller 6",
      "Jaipur Reseller 5",
  ]

  masked_narrative = (
      "Top spender ALIAS-19 in West region generated INR 75,295.09 in spend."
  )
  unmasked_narrative = (
      "Top spender Mumbai Reseller 1 in West region generated INR 75,295.09 in"
      " spend."
  )

  assert assert_no_raw_names_leak(masked_narrative, raw_names) is True
  assert assert_no_raw_names_leak(unmasked_narrative, raw_names) is False

  print("✅ All masking & PII guardrail tests passed successfully!")