import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['figure.dpi'] = 150
palette = sns.color_palette("crest", 5)

df = pd.read_csv('sales_data.csv', parse_dates=['Date'])

# ============================================================
# 1. BAR CHART — Total Revenue by Product Category
# ============================================================
cat_rev = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False) / 1e6

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.bar(cat_rev.index, cat_rev.values, color=sns.color_palette("crest", len(cat_rev)))
ax.set_title('Total Revenue by Product Category (2024–2025)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Revenue ($ Millions)')
for bar, val in zip(bars, cat_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f'${val:.1f}M', ha='center', fontsize=11, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('01_bar_revenue_by_category.png', bbox_inches='tight')
plt.close()

# ============================================================
# 2. LINE CHART — Monthly Revenue Trend (overall + by region)
# ============================================================
monthly = df.groupby(['Date', 'Region'])['Revenue'].sum().reset_index()
monthly_total = df.groupby('Date')['Revenue'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6.5))
for i, region in enumerate(df['Region'].unique()):
    sub = monthly[monthly['Region'] == region]
    ax.plot(sub['Date'], sub['Revenue']/1000, marker='o', markersize=3.5,
            linewidth=1.8, label=region, color=sns.color_palette("crest", 4)[i])
ax.plot(monthly_total['Date'], monthly_total['Revenue']/1000, color='black',
        linewidth=2.6, linestyle='--', label='Total (All Regions)')
ax.set_title('Monthly Revenue Trend by Region (2024–2025)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($ Thousands)')
ax.legend(loc='upper left', frameon=True, ncol=3, fontsize=10)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('02_line_monthly_revenue_trend.png', bbox_inches='tight')
plt.close()

# ============================================================
# 3. SCATTER PLOT — Marketing Spend vs Revenue
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
cats = df['Category'].unique()
colors = sns.color_palette("crest", len(cats))
for cat, c in zip(cats, colors):
    sub = df[df['Category'] == cat]
    ax.scatter(sub['MarketingSpend'], sub['Revenue']/1000, alpha=0.55, s=45, color=c, label=cat, edgecolor='white', linewidth=0.3)

# overall trend line
z = np.polyfit(df['MarketingSpend'], df['Revenue']/1000, 1)
xline = np.linspace(df['MarketingSpend'].min(), df['MarketingSpend'].max(), 100)
ax.plot(xline, np.poly1d(z)(xline), color='#333333', linestyle='--', linewidth=2, label='Overall Trend')

corr = df['MarketingSpend'].corr(df['Revenue'])
ax.set_title(f'Marketing Spend vs. Revenue (r = {corr:.2f})', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Marketing Spend ($)')
ax.set_ylabel('Revenue ($ Thousands)')
ax.legend(loc='upper left', fontsize=9, ncol=2)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('03_scatter_marketing_vs_revenue.png', bbox_inches='tight')
plt.close()

# ============================================================
# 4. HEATMAP — Correlation Matrix of Key Numeric Variables
# ============================================================
numeric_cols = ['UnitsSold', 'Revenue', 'MarketingSpend', 'DiscountPct', 'Profit', 'ProfitMargin']
corr_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='crest', center=0,
            square=True, linewidths=0.6, cbar_kws={'label': 'Correlation Coefficient'}, ax=ax)
ax.set_title('Correlation Heatmap of Key Sales Metrics', fontsize=15, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('04_heatmap_correlation.png', bbox_inches='tight')
plt.close()

# ============================================================
# 5. BONUS HEATMAP — Avg Monthly Revenue by Region x Category
# ============================================================
pivot = df.pivot_table(index='Region', columns='Category', values='Revenue', aggfunc='mean') / 1000

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='crest',
            linewidths=0.6, cbar_kws={'label': 'Avg. Monthly Revenue ($K)'}, ax=ax)
ax.set_title('Average Monthly Revenue: Region vs. Product Category', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Product Category')
ax.set_ylabel('Region')
plt.tight_layout()
plt.savefig('05_heatmap_region_category.png', bbox_inches='tight')
plt.close()

# ============================================================
# 6. BONUS — Box Plot of Profit Margin by Region
# ============================================================
fig, ax = plt.subplots(figsize=(9, 6.5))
sns.boxplot(data=df, x='Region', y='ProfitMargin', hue='Region', palette='crest', ax=ax, legend=False)
ax.set_title('Profit Margin Distribution by Region', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Region')
ax.set_ylabel('Profit Margin (%)')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('06_boxplot_margin_by_region.png', bbox_inches='tight')
plt.close()

print("All 6 visualizations generated successfully.")
print("Correlation matrix:\n", corr_matrix.round(2))
