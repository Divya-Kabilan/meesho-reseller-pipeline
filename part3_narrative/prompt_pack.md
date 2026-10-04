# Prompt Pack: Flagged Category Narrative Draft

## Trigger
A category is routed into this prompt only when `is_flagged(category_mom_pct)` returns `"flagged"` for the current month versus the previous month.

## Input list
- `{month}`: current reporting month, e.g. "May"
- `{prev_month}`: prior month, e.g. "April"
- `{category}`: category name, e.g. "Ethnic Wear"
- `{previous_revenue}`: verified revenue for the previous month
- `{current_revenue}`: verified revenue for the current month
- `{mom_pct}`: verified month-on-month percentage change
- `{status}`: the flag status, e.g. "flagged"
- `{region}`: region or summary scope in the current view, if relevant
- `{reseller_alias}`: coded alias for any reseller mention, never a raw name

## Prompt
Use the following template:

"You are writing a Meesho category-manager update for {month} compared with {prev_month}.\n\nContext: Measure {category} performance across the business for {prev_month} versus {month}.\n\nInsight: The verified revenue moved from {previous_revenue} to {current_revenue}, a {mom_pct}% change. This is a fact and must stay exactly aligned with the supplied values.\n\nImplication: Based on that fact, recommend one specific action for category operations, e.g. review inventory, marketing spend, or supplier coverage. Label this recommendation as a hypothesis if it is a causal interpretation and not a proven fact.\n\nStructure the answer as: Context → Insight → Implication. Keep the tone appropriate for a regional manager, not a data engineer. Never mention any number that is not one of the supplied placeholders. Never mention a reseller by raw name; use only the alias format ALIAS-XX when reseller references are required."

## Checklist
Before the draft is used, validate all of the following:
1. Every numeric value in the draft matches one of the supplied placeholders exactly, with no invented figures.
2. Every claim is labeled as either a fact or a hypothesis; no unsupported causal statements are presented as proven results.
3. The recommendation is specific and actionable, not vague (for example: "reallocate inventory to protect stockouts" rather than "look into it").
4. Any reseller reference uses only the coded alias format, never a raw reseller name.
5. The response follows the required Context → Insight → Implication structure.
6. The narrative is written for a regional manager audience and avoids technical implementation language.
