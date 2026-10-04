

# Executive Summary: Reseller Performance & Growth Analysis

## 1. Regional Performance Breakdown (Q2 2026)

Based on verified SQL query aggregations across 900 orders and 24 resellers:

- **North Region:** Generated **INR 337,125.46** across **238 orders**, leading overall revenue performance.
- **West Region:** Generated **INR 333,106.33** across **231 orders**, closely trailing North.
- **South Region:** Generated **INR 316,736.68** across **221 orders**.
- **East Region:** Generated **INR 275,098.45** across **210 orders**.

---

## 2. Category Growth & Anomaly Detection Analysis

Using our Python Growth-Detection Engine with an **8.0% growth anomaly threshold**:

### May vs. April Performance
- **Ethnic Wear:** Increased by **+77.10%** (INR 104,520.77 to INR 185,107.61) — **FLAGGED**
- **Western Wear:** Decreased by **-23.60%** (INR 104,323.86 to INR 79,703.11) — **FLAGGED**
- **Kids Wear:** Decreased by **-23.48%** (INR 53,046.33 to INR 40,591.24) — **FLAGGED**
- **Home & Kitchen:** Decreased by **-9.25%** (INR 60,555.77 to INR 54,954.54) — **FLAGGED**
- **Beauty & Personal Care:** Decreased by **-12.75%** (INR 40,733.91 to INR 35,542.11) — **FLAGGED**

*Key Observation:* May experienced a massive seasonal shift toward **Ethnic Wear** ahead of summer festival demand, pulling purchasing volume away from other categories.

### June vs. May Performance
- **Ethnic Wear:** Decreased by **-58.74%** (INR 185,107.61 to INR 76,378.02) — **FLAGGED**
- **Western Wear:** Rebounded by **+11.97%** (INR 79,703.11 to INR 89,240.23) — **FLAGGED**
- **Kids Wear:** Rebounded by **+23.90%** (INR 40,591.24 to INR 50,293.44) — **FLAGGED**
- **Home & Kitchen:** Surged by **+42.59%** (INR 54,954.54 to INR 78,358.55) — **FLAGGED**
- **Beauty & Personal Care:** Grew by **+5.67%** (INR 35,542.11 to INR 37,559.07) — **NOT FLAGGED**

*Key Observation:* June saw normalization in Ethnic Wear demand, while Home & Kitchen and Kids Wear experienced strong recovery surges.

---

## 3. Operational Integrity & Audit Insights

1. **Zero-Order Reseller Detection:** Reseller `RS024` was identified with 0 orders. Query auditing confirmed that `COUNT(order_id)` properly evaluates to `0` whereas `COUNT(*)` returns `1` due to standard `LEFT JOIN` outer row retention.
2. **June Delivered AOV:** Average Order Value for delivered orders in June stood at **INR 1,267.69**.
3. **Guardrail Enforcement:** The automated validation script successfully caught negative revenue values, missing category descriptors, and missing numeric entries, preventing corrupted feeds from altering financial reporting.

---

## 4. Strategic Recommendations

1. **Inventory Balancing for Festive/Seasonal Peaks:** Pre-plan supplier inventory for Ethnic Wear in April to prepare for May spikes without inventory shortages in adjacent categories.
2. **Promotional Support for Lags:** Deploy targeted reseller commission incentives for Home & Kitchen during non-peak months to minimize sharp MoM drops.
3. **Reseller Onboarding Intervention:** Engage zero-order resellers like `RS024` through automated starter-kit promotions within 14 days of joining to activate sales pipelines.