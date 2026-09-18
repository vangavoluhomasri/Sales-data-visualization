import pandas as pd
import numpy as np

np.random.seed(42)

# ---- Simulate 2 years of monthly retail sales data ----
regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
segments = ['Consumer', 'Corporate', 'Small Business']

dates = pd.date_range('2024-01-01', '2025-12-01', freq='MS')

rows = []
# base demand + seasonality + category multipliers + regional multipliers
category_base = {'Electronics': 42000, 'Clothing': 28000, 'Home & Garden': 22000,
                  'Sports': 18000, 'Books': 9000}
region_mult = {'North': 1.15, 'South': 0.95, 'East': 1.05, 'West': 0.9}
category_margin = {'Electronics': 0.18, 'Clothing': 0.32, 'Home & Garden': 0.27,
                    'Sports': 0.24, 'Books': 0.35}

for date in dates:
    month = date.month
    # seasonal factor: holiday bump in Nov/Dec, summer dip in Jul/Aug
    seasonal = 1.0
    if month in (11, 12):
        seasonal = 1.45
    elif month in (7, 8):
        seasonal = 0.85
    elif month in (1, 2):
        seasonal = 0.9
    # mild year-over-year growth
    yoy_growth = 1.0 + (date.year - 2024) * 0.08

    for region in regions:
        for cat in categories:
            base = category_base[cat] * region_mult[region] * seasonal * yoy_growth
            noise = np.random.normal(1, 0.08)
            revenue = max(base * noise, 500)

            marketing_spend = revenue * np.random.uniform(0.04, 0.11)
            # marketing has a modest positive effect already baked into revenue via noise correlation
            discount_pct = np.clip(np.random.normal(12, 5), 0, 35)
            units_sold = revenue / np.random.uniform(35, 95)
            margin = category_margin[cat] + np.random.normal(0, 0.03)
            profit = revenue * margin - (revenue * discount_pct / 100 * 0.3)
            segment = np.random.choice(segments, p=[0.55, 0.3, 0.15])

            rows.append({
                'Date': date,
                'Region': region,
                'Category': cat,
                'CustomerSegment': segment,
                'UnitsSold': round(units_sold),
                'Revenue': round(revenue, 2),
                'MarketingSpend': round(marketing_spend, 2),
                'DiscountPct': round(discount_pct, 2),
                'Profit': round(profit, 2),
            })

df = pd.DataFrame(rows)
df['ProfitMargin'] = (df['Profit'] / df['Revenue'] * 100).round(2)
df.to_csv('sales_data.csv', index=False)
print(df.shape)
print(df.head())
print(df.describe())
