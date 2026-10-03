import csv
import os
import sqlite3

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "part1_sql", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Query 1: Monthly Revenue by Category
q1_sql = """
SELECT 
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY 
    CASE month 
        WHEN 'April' THEN 1 
        WHEN 'May' THEN 2 
        WHEN 'June' THEN 3 
    END,
    category;
"""
cur.execute(q1_sql)
q1_rows = cur.fetchall()

q1_csv_path = os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv")
with open(q1_csv_path, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["month", "category", "revenue", "n_orders"])
  writer.writerows(q1_rows)

print(f" Query 1 exported to {q1_csv_path}")

# Query 2: Region-wise total revenue and order count
q2_sql = """
SELECT 
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(o.order_id) AS total_orders
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""
cur.execute(q2_sql)
q2_rows = cur.fetchall()

q2_csv_path = os.path.join(OUTPUT_DIR, "region_revenue.csv")
with open(q2_csv_path, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["region", "total_revenue", "total_orders"])
  writer.writerows(q2_rows)

print("\n--- Query 2: Region-wise Summary ---")
for row in q2_rows:
  print(f"Region: {row[0]} | Revenue: INR {row[1]} | Orders: {row[2]}")

# Query 3: Top Resellers with spend > 50,000
q3_sql = """
SELECT 
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""
cur.execute(q3_sql)
q3_rows = cur.fetchall()

q3_csv_path = os.path.join(OUTPUT_DIR, "top_resellers.csv")
with open(q3_csv_path, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["reseller_id", "reseller_name", "total_spend"])
  writer.writerows(q3_rows)

print("\n--- Query 3: Top Resellers (> 50,000 Spend) ---")
for row in q3_rows:
  print(f"{row[0]} ({row[1]}): INR {row[2]}")

# Query 4: Resellers who have never placed an order + Demonstration of COUNT(*) vs COUNT(order_id)
q4_sql = """
SELECT 
    r.reseller_id,
    r.reseller_name,
    r.region,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING COUNT(o.order_id) = 0;
"""
cur.execute(q4_sql)
q4_rows = cur.fetchall()

q4_csv_path = os.path.join(OUTPUT_DIR, "zero_order_resellers.csv")
with open(q4_csv_path, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow([
      "reseller_id",
      "reseller_name",
      "region",
      "count_star",
      "count_order_id",
  ])
  writer.writerows(q4_rows)

print("\n--- Query 4: Zero-Order Reseller Demonstration ---")
for row in q4_rows:
  print(
      f"ID: {row[0]} | Name: {row[1]} | Region: {row[2]} | COUNT(*): {row[3]} |"
      f" COUNT(order_id): {row[4]}"
  )

# Query 5: Average Order Value (AOV) for June Delivered Orders
q5_sql = """
SELECT 
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';
"""
cur.execute(q5_sql)
june_aov = cur.fetchone()[0]

print(
    f"\n--- Query 5: June Delivered AOV ---\nJune Delivered AOV: INR"
    f" {june_aov}"
)

conn.close()