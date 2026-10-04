# Part 4: Agentic Workflow Specification

## 1. System Architecture & Components

- **Goal:** Keep Meesho category managers alerted to any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it is released.
- **Tools:**
  - `validate_feed(csv_path)`: Input integrity guardrail.
  - `mom_growth(prev, curr)`: Deterministic MoM % calculator.
  - `is_flagged(mom_pct, threshold)`: Threshold classifier.
  - `prompt_pack`: Template filler for drafting stakeholder alerts.
- **Memory / State:** Holds previous month category revenues to perform delta evaluations on new incoming feeds.
- **Planner:** Sequential workflow execution engine with explicit subtasks 1 through 8.
- **Feedback Loop:** Human-in-the-loop checkpoint (`drafted_and_held_for_approval`) ensuring no communication is auto-sent without explicit sign-off.

---

## 2. Planner — Ordered Subtasks

1. Load the monthly revenue feed and validate the incoming current-month file with `validate_feed`.
2. If validation fails, immediately return `action_taken = "hard_stop"` and surface each validation error.
3. If validation passes, load the previous month and current month category revenue dictionaries.
4. Compute `mom_growth(prev_rev, curr_rev)` for every category that exists in both periods.
5. Classify each category using `is_flagged(mom_pct, threshold=8.0)`.
6. Sort all `flagged` categories by absolute MoM percentage descending and keep only the top 3 for drafting.
7. Draft messages for at most the top 3 categories, while storing the remaining flagged categories in `suppressed_categories`.
8. Capture `escalate_exact_boundary` categories in `escalated_categories` and emit one structured JSON result object for the run.

---

## 2. Guardrails & Stopping Conditions

- **Input Guardrail:** `validate_feed` must evaluate to `(True, [])`. Any failure triggers an immediate `hard_stop`.
- **Action Guardrail:** Messages are generated into a held queue (`drafted = true`); direct communication dispatch is strictly blocked.
- **Output Guardrail:** All numbers in generated messages must trace deterministically to verified SQL/Python metrics.
- **Stopping Conditions:**
  - *Success:* Returns `action_taken = "drafted_and_held_for_approval"`.
  - *Hard Stop:* Returns `action_taken = "hard_stop"` with non-empty `validation_errors`.

---

## 3. Agent-Level Given-When-Then Specifications

1. **GIVEN** April->May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** evaluated by the agent, **THEN** it calculates 77.10% growth, flags the category, and drafts a message.
2. **GIVEN** May->June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** evaluated by the agent, **THEN** it calculates 5.67% growth, marks it `not_flagged`, and does not draft a message.
3. **GIVEN** A revenue pair on the boundary (`prev=100000`, `curr=108000`), **WHEN** evaluated by the agent, **THEN** it returns `escalate_exact_boundary` and routes it to `escalated_categories`.
4. **GIVEN** `corrupted_feed.csv`, **WHEN** processed by the agent, **THEN** it halts execution immediately (`hard_stop`) and surfaces 3 validation error strings.