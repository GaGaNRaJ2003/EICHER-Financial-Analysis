"""
Calculate ACTUAL SIP investment returns for EICHER Motors
Using real stock prices from NSE/BSE
"""
import pandas as pd
import numpy as np

print("="*80)
print("EICHER MOTORS LIMITED - ACTUAL SIP INVESTMENT CALCULATION")
print("="*80)

# Read actual stock prices
df = pd.read_csv('Stock price on first trading day.csv')
# Clean the data
df = df[df['Date (First Trading Day)'].str.contains('-', na=False)].copy()
df['Price (INR)'] = df['Price (INR)'].str.replace(',', '').astype(float)
df = df.reset_index(drop=True)  # Reset index to start from 0

print(f"\n[OK] Loaded {len(df)} months of actual stock price data")
print(f"   Period: {df['Date (First Trading Day)'].iloc[0]} to {df['Date (First Trading Day)'].iloc[-1]}")
print()

# Dividend data from annual reports (verified)
# Note: Dividends paid after year-end, applied in following months
dividends = {
    17: 37,   # FY 2020-21 dividend paid Aug 2021
    29: 37,   # FY 2021-22 dividend paid Aug 2022
    53: 51,   # FY 2023-24 dividend paid Aug 2024
    60: 70    # FY 2024-25 dividend (final period valuation)
}

# Initialize variables
monthly_investment = 10000
cumulative_shares = 0
total_invested = 0
total_dividends = 0
monthly_data = []

print("Calculating SIP performance with actual prices...")
print("-" * 80)

for idx, row in df.iterrows():
    month_num = idx + 1
    date = row['Date (First Trading Day)']
    price = row['Price (INR)']
    
    # Monthly investment
    total_invested += monthly_investment
    shares_bought = monthly_investment / price
    cumulative_shares += shares_bought
    
    # Check for dividends
    div_amount = 0
    div_shares = 0
    if month_num in dividends:
        div_amount = cumulative_shares * dividends[month_num]
        total_dividends += div_amount
        div_shares = div_amount / price
        cumulative_shares += div_shares
    
    current_value = cumulative_shares * price
    
    monthly_data.append({
        'Month': month_num,
        'Date': date,
        'Price': price,
        'Monthly_Investment': monthly_investment,
        'Shares_Bought': shares_bought,
        'Cumulative_Shares': cumulative_shares,
        'Dividend_Amount': div_amount,
        'Div_Shares': div_shares,
        'Current_Value': current_value
    })

# Final results
final_price = df['Price (INR)'].iloc[-1]
final_value = cumulative_shares * final_price
absolute_returns = final_value - total_invested
returns_pct = (absolute_returns / total_invested) * 100
cagr = ((final_value / total_invested) ** (1/5)) - 1

print("="*80)
print("ACTUAL SIP INVESTMENT RESULTS")
print("="*80)
print(f"\nInvestment Period: April 2020 to March 2025 (60 months)")
print(f"Monthly Investment: ₹10,000")
print(f"\n{'='*80}")
print(f"Total Amount Invested:      ₹{total_invested:,.2f}")
print(f"Total Dividends Received:   ₹{total_dividends:,.2f}")
print(f"Total Shares Owned:         {cumulative_shares:.4f}")
print(f"Current Stock Price:        ₹{final_price:,.2f}")
print(f"\n{'='*80}")
print(f"Current Portfolio Value:    ₹{final_value:,.2f}")
print(f"Absolute Returns:           ₹{absolute_returns:,.2f}")
print(f"Returns Percentage:         {returns_pct:.2f}%")
print(f"Annualized Returns (CAGR):  {cagr*100:.2f}%")
print("="*80)

# Quarterly summary
quarterly_data = []
for q in [12, 24, 36, 48, 60]:
    if q <= len(monthly_data):
        m = monthly_data[q-1]
        invested = q * monthly_investment
        returns = m['Current_Value'] - invested
        returns_pct_q = (returns / invested) * 100
        
        quarterly_data.append({
            'Period': f'{q} months',
            'Shares': m['Cumulative_Shares'],
            'Invested': invested,
            'Value': m['Current_Value'],
            'Returns': returns,
            'Returns_%': returns_pct_q
        })

print("\nQUARTERLY PERFORMANCE SUMMARY")
print("="*80)
q_df = pd.DataFrame(quarterly_data)
print(q_df.to_string(index=False))

# Save detailed results
results_df = pd.DataFrame(monthly_data)
results_df.to_excel('SIP_Actual_Results.xlsx', index=False)
print(f"\n[OK] Detailed results saved to: SIP_Actual_Results.xlsx")

# Create summary for LaTeX
print("\n" + "="*80)
print("SUMMARY FOR LATEX REPORT")
print("="*80)
print(f"\\textbf{{Total Investment}}: ₹6,00,000")
print(f"\\textbf{{Dividends Received}}: ₹{total_dividends:.2f}")
print(f"\\textbf{{Total Shares}}: {cumulative_shares:.2f}")
print(f"\\textbf{{Current Value}}: ₹{final_value:.2f}")
print(f"\\textbf{{Absolute Returns}}: ₹{absolute_returns:.2f}")
print(f"\\textbf{{Returns Percentage}}: {returns_pct:.2f}\\%")
print(f"\\textbf{{CAGR}}: {cagr*100:.2f}\\%")
print("="*80)

