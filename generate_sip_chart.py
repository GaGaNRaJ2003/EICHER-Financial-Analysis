"""
Generate actual SIP investment chart with real data
"""
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

# Read actual stock prices
df = pd.read_csv('Stock price on first trading day.csv')
df = df[df['Date (First Trading Day)'].str.contains('-', na=False)].copy()
df['Price (INR)'] = df['Price (INR)'].str.replace(',', '').astype(float)
df = df.reset_index(drop=True)

# Dividend data (month_num: amount)
dividends = {
    17: 37,   # FY 2020-21 dividend
    29: 37,   # FY 2021-22 dividend
    53: 51,   # FY 2023-24 dividend
    60: 70    # FY 2024-25 dividend (final period)
}

# Calculate SIP
monthly_investment = 10000
cumulative_shares = 0

portfolio_values = [0]  # Start with 0
invested_values = [0]   # Start with 0
month_numbers = [0, 12, 24, 36, 48, 60]

print("Calculating SIP with actual prices...")
for idx, row in df.iterrows():
    month_num = idx + 1  # 1 to 60
    price = row['Price (INR)']
    
    shares_bought = monthly_investment / price
    cumulative_shares += shares_bought
    
    if month_num in dividends:
        div_amount = cumulative_shares * dividends[month_num]
        div_shares = div_amount / price
        cumulative_shares += div_shares
    
    if month_num in [12, 24, 36, 48, 60]:
        invested = month_num * monthly_investment
        portfolio_value = cumulative_shares * price
        invested_values.append(invested)
        portfolio_values.append(portfolio_value)

# Create chart
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(month_numbers, invested_values, color='#666666', marker='o', 
        markersize=8, linewidth=2, label='Amount Invested', linestyle='--', alpha=0.7)
ax.plot(month_numbers, portfolio_values, color='#2E7D32', marker='s', 
        markersize=8, linewidth=2.5, label='Portfolio Value', linestyle='-')

ax.set_xlabel('Months', fontweight='bold')
ax.set_ylabel('Amount (₹)', fontweight='bold')
ax.set_title('SIP Investment Growth Over 5 Years\n(₹10,000 per month with dividend reinvestment)', 
             fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9)

# Add labels
for i, (m, pv) in enumerate(zip([12, 24, 36, 48, 60], portfolio_values[1:])):
    ax.text(m, pv + 30000, f'₹{pv/1000:.0f}K', 
            ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2E7D32')

ax.text(60, invested_values[-1] - 50000, f'Invested: ₹600K', 
        ha='center', va='top', fontsize=9, color='#666666', fontweight='bold')

x_labels = ['Apr 2020', 'Apr 2021', 'Apr 2022', 'Apr 2023', 'Apr 2024', 'Mar 2025']
ax.set_xticks(month_numbers)
ax.set_xticklabels(x_labels)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('figs/chart_5_sip_growth.png', bbox_inches='tight', facecolor='white')
print(f"✅ SIP chart created: Portfolio values at {[12, 24, 36, 48, 60]} months")
print(f"   Final value: ₹{portfolio_values[-1]:,.0f}")
