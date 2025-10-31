# EICHER Motors Limited - Financial Analysis Report

## 📊 Project Overview

Comprehensive financial analysis of EICHER Motors Limited (EICHERMOT) covering FY 2020-21 to FY 2024-25 (5 years), including:
- Balance Sheet, Income Statement, and Cash Flow Analysis
- Common-Size Financial Statements
- Ratio Analysis with Interpretations
- SIP Investment Analysis with Actual Market Data
- Management Commentary and Key Findings

**Group Project for Foundations of Finance Course**

## 📁 Project Structure

```
FF_Project/
├── Eicher_Financial_Analysis_Report.tex    # Main LaTeX report (18-20 pages)
├── EICHER_Financial_Analysis.xlsx          # Complete financial analysis workbook
├── SIP_Actual_Results.xlsx                 # SIP investment calculation annexure
├── README.md                               # This file - project documentation
├── Readme.md                               # Project instructions from course
├── CHECKLIST.md                            # Submission requirements
├── REPORT_COMPILATION_INSTRUCTIONS.md      # LaTeX compilation guide
├── FINAL_PROJECT_SUMMARY.md                # Project summary
├── Eicher-logo-640x323.jpg                 # Company logo
├── Stock price on first trading day.csv    # Market data for SIP analysis
├── data/                                   # Raw CSV data (5 years)
│   └── raw_csv/
│       ├── 2020-2021/                      # Balance sheet, income, cash flow
│       ├── 2021-2022/
│       ├── 2022-2023/
│       ├── 2023-2024/
│       └── 2024-2025/
├── EICHER/                                 # Source PDFs (annual reports)
│   ├── Standalone-financials_20-21.pdf
│   ├── Standalonefinancial-21-22.pdf
│   ├── Standalone-Financials22-23.pdf
│   ├── Standalone-Financials23-24.pdf
│   └── Standalone-fs-24-25.pdf
├── figs/                                   # Financial charts (6 charts)
│   ├── chart_1_total_assets_growth.png
│   ├── chart_2_revenue_pat_trend.png
│   ├── chart_3_common_size_income.png
│   ├── chart_4_profitability_ratios.png
│   ├── chart_5_sip_growth.png
│   └── chart_6_key_metrics_summary.png
└── scripts/                                # Data processing & analysis scripts
    ├── process_statements.py               # Process raw CSV data
    ├── calculate_actual_sip.py             # SIP calculation with actual prices
    ├── generate_charts.py                  # Generate all financial charts
    └── generate_sip_chart.py               # SIP investment growth chart
```

## 🎯 Key Deliverables

1. **Financial Analysis Report** (LaTeX)
   - Executive Summary
   - Company Profile & Industry Overview
   - 5-Year Financial Statement Analysis
   - Common-Size Statements
   - Comprehensive Ratio Analysis
   - Operations Interpretation
   - SIP Investment Analysis
   - Key Findings & Conclusions

2. **Excel Workbook** (`EICHER_Financial_Analysis.xlsx`)
   - 26 sheets with complete financial data
   - Raw statements, common-size statements
   - Ratio analysis summaries

3. **SIP Annexure** (`SIP_Actual_Results.xlsx`)
   - Monthly SIP investment details
   - Stock prices from NSE/BSE
   - Dividend reinvestment calculations
   - Returns analysis

4. **Financial Charts** (6 charts in `figs/`)
   - Total Assets Growth
   - Revenue & PAT Trends
   - Common-Size Income Statement
   - Profitability Ratios
   - SIP Investment Growth
   - Key Metrics Summary

## 📈 Analysis Highlights

### Financial Performance (FY 2020-21 to FY 2024-25)
- **Total Assets**: ₹1,962.66 Cr → ₹13,375.59 Cr (7.8x growth)
- **Revenue**: ₹9,974 Cr → ₹22,918 Cr (2.3x growth)
- **PAT**: ₹1,179 Cr → ₹4,401 Cr (3.7x growth)
- **ROE**: 44.85% → 33.64% (strong but moderated)
- **Current Ratio**: Maintained above 2.0 (healthy liquidity)

### SIP Investment Results (₹10,000/month for 60 months)
- **Total Investment**: ₹6,00,000
- **Current Portfolio Value**: ₹10,41,724
- **Absolute Returns**: ₹4,41,724 (73.62%)
- **Annualized Returns (CAGR)**: 11.67% p.a.
- **Shares Accumulated**: 212.31 shares

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+ (for scripts)
- LaTeX distribution (MiKTeX/TeX Live) or Overleaf account
- Excel or LibreOffice Calc (for viewing .xlsx files)

### Compiling the Report
1. **Option A: Using Overleaf (Recommended)**
   - Upload `Eicher_Financial_Analysis_Report.tex` to https://www.overleaf.com
   - Click "Recompile"
   - Download PDF

2. **Option B: Local LaTeX**
   ```bash
   pdflatex Eicher_Financial_Analysis_Report.tex
   pdflatex Eicher_Financial_Analysis_Report.tex  # Run twice for references
   ```

### Running Python Scripts
```bash
# Install dependencies
pip install pandas matplotlib openpyxl pdfplumber

# Process raw financial data
python scripts/process_statements.py

# Generate all charts
python scripts/generate_charts.py

# Calculate SIP with actual stock prices
python scripts/calculate_actual_sip.py

# Generate SIP investment growth chart
python scripts/generate_sip_chart.py
```

## 📚 Data Sources

- **Financial Statements**: EICHER Motors Limited standalone financials (FY 2020-21 to FY 2024-25)
- **Stock Prices**: NSE/BSE historical data (first trading day prices for SIP calculation)
- **Dividends**: Company annual reports

## 📋 File Descriptions

### Main Documents
- **`Eicher_Financial_Analysis_Report.tex`**: LaTeX source file for the complete financial analysis report (18-20 pages)
- **`EICHER_Financial_Analysis.xlsx`**: Comprehensive Excel workbook with 26 sheets containing all financial data, common-size statements, and ratios
- **`SIP_Actual_Results.xlsx`**: Detailed SIP investment calculation with month-by-month breakdown, stock prices, and returns

### Source Data
- **`data/raw_csv/`**: Extracted financial statements in CSV format for 5 years (2020-21 to 2024-25)
- **`EICHER/`**: Original PDF annual reports from company website
- **`Stock price on first trading day.csv`**: Historical stock prices for SIP calculation

### Scripts
- **`scripts/process_statements.py`**: Processes raw CSV data, calculates common-size statements and financial ratios
- **`scripts/calculate_actual_sip.py`**: Calculates SIP returns using actual stock prices and dividend history
- **`scripts/generate_charts.py`**: Generates all 6 financial charts (assets, revenue, ratios, etc.)
- **`scripts/generate_sip_chart.py`**: Creates the SIP investment growth visualization

### Documentation
- **`README.md`**: This file - comprehensive project documentation
- **`Readme.md`**: Original project instructions from the course
- **`CHECKLIST.md`**: Submission requirements and deliverables checklist
- **`REPORT_COMPILATION_INSTRUCTIONS.md`**: Guide for compiling LaTeX report
- **`FINAL_PROJECT_SUMMARY.md`**: Overall project status and summary

## 📝 Key Findings

1. **Strong Financial Position**: Consistent revenue growth, robust profitability
2. **Premium Brand**: Royal Enfield maintains market leadership in mid-size motorcycles
3. **International Expansion**: Growing presence in global markets
4. **Capital Efficiency**: Improving asset utilization and working capital management
5. **Shareholder Returns**: Increasing dividend payouts (₹37 → ₹70 per share)


**Note**: This report was prepared using actual financial data from EICHER Motors Limited and represents an independent analysis. Stock prices and SIP calculations are based on publicly available data from NSE/BSE.
