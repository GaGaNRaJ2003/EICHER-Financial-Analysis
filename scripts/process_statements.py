"""
Process EICHER financial statements from organized CSV files.
Creates normalized statements, common-size analysis, and calculates ratios.
"""
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = PROJECT_ROOT / "data" / "raw_csv"
OUTPUT_XLSX = PROJECT_ROOT / "EICHER_Financial_Analysis.xlsx"

YEARS = ["2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]


def normalize_number(val) -> Optional[float]:
    """Convert various number formats to float."""
    if pd.isna(val) or val == "":
        return None
    s = str(val).strip()
    # Remove currency symbols first
    s = s.replace("₹", "").replace("Rs.", "").replace("\u2212", "-")
    
    # Handle Indian format: "1,962.66" -> commas between thousands
    if "," in s and "." in s:
        s = s.replace(",", "")
    # Handle cases where commas might be used as decimal separator
    elif "," in s and s.count(",") == 1:
        parts = s.split(",")
        if len(parts) == 2 and len(parts[1]) <= 2:
            s = ".".join(parts)
        else:
            s = s.replace(",", "")
    # Handle cases where dots are used as thousand separators: "13.375.59"
    elif "." in s and s.count(".") > 1:
        parts = s.split(".")
        # If last part has 2 digits, it's probably decimal (e.g., "12.624.91" -> "12624.91")
        if len(parts[-1]) == 2 and len(parts) > 2:
            s = "".join(parts[:-1]) + "." + parts[-1]
        else:
            s = s.replace(".", "")
    
    # Extract first numeric value
    match = re.search(r"-?\d+\.?\d*", s)
    return float(match.group(0)) if match else None


def load_statement(year: str, stmt_type: str) -> Optional[pd.DataFrame]:
    """Load a financial statement CSV file."""
    # Map full year to suffix: "2020-2021" -> "20-21"
    year_map = {
        "2020-2021": "20-21",
        "2021-2022": "21-22",
        "2022-2023": "22-23",
        "2023-2024": "23-24",
        "2024-2025": "24-25",
    }
    suffix = year_map.get(year, year[-5:])
    
    if stmt_type == "bs":
        filename = f"balance sheet {suffix}.csv"
    elif stmt_type == "is":
        filename = f"income statement {suffix}.csv"
    elif stmt_type == "cf":
        filename = f"cash flow statement {suffix}.csv"
    else:
        return None
    
    path = RAW_ROOT / year / filename
    if not path.exists():
        print(f"Warning: {path} not found")
        return None
    
    df = pd.read_csv(path)
    # Drop completely empty rows
    df = df.dropna(how="all")
    return df


def find_row_value(df: pd.DataFrame, search_keys: List[str], col_idx: int = -1) -> Optional[float]:
    """Find a value in a statement by searching for key strings in label columns."""
    if df is None or df.empty:
        return None
    
    # Try both column 0 and column 1 as label columns (for various CSV layouts)
    label_cols = []
    if df.shape[1] > 1 and df.iloc[:, 1].notna().any():
        label_cols.append(1)  # Most CSVs have labels in column 1
    if df.iloc[:, 0].notna().any():
        label_cols.append(0)  # Some might have it in column 0
    
    for label_col in label_cols:
        label_series = df.iloc[:, label_col].astype(str).str.lower()
        
        for key in search_keys:
            mask = label_series.str.contains(key, na=False, case=False, regex=False)
            matched_rows = df[mask]
            
            if not matched_rows.empty:
                # Try columns from right to left
                cols_to_try = list(range(df.shape[1] - 1, 0, -1)) if col_idx == -1 else [col_idx]
                for c in cols_to_try:
                    val = normalize_number(matched_rows.iloc[0, c])
                    if val is not None and val != 0:
                        return val
    
    return None


def compute_common_size_bs(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Compute common-size Balance Sheet as % of Total Assets."""
    if df is None or df.shape[1] < 2:
        return None
    
    # Find Total Assets (use the last data column)
    total_assets = find_row_value(df, ["total assets", "total-assets", "total of assets", "total-assets (a)"], col_idx=-1)
    
    if total_assets is None or total_assets == 0:
        print("Warning: Could not find Total Assets for common-size calculation")
        return None
    
    # Create copy and convert numbers
    cs_df = df.copy()
    for col_idx in range(1, df.shape[1]):
        cs_df.iloc[:, col_idx] = cs_df.iloc[:, col_idx].apply(normalize_number)
        cs_df.iloc[:, col_idx] = (cs_df.iloc[:, col_idx] / total_assets) * 100.0
    
    return cs_df


def compute_common_size_is(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Compute common-size Income Statement as % of Revenue."""
    if df is None or df.shape[1] < 2:
        return None
    
    # Find Revenue (use the last data column for yearly figures)
    revenue = find_row_value(df, ["total revenue from operations", "total income"], col_idx=-1)
    
    if revenue is None or revenue == 0:
        print("Warning: Could not find Revenue for common-size calculation")
        return None
    
    # Create copy and convert numbers
    cs_df = df.copy()
    for col_idx in range(1, df.shape[1]):
        cs_df.iloc[:, col_idx] = cs_df.iloc[:, col_idx].apply(normalize_number)
        cs_df.iloc[:, col_idx] = (cs_df.iloc[:, col_idx] / revenue) * 100.0
    
    return cs_df


def calculate_ratios() -> pd.DataFrame:
    """Calculate key financial ratios across all years."""
    ratios = []
    
    for year in YEARS:
        bs = load_statement(year, "bs")
        is_stmt = load_statement(year, "is")
        
        # Extract key values from last data column
        revenue = find_row_value(is_stmt, ["total revenue from operations", "total income"], col_idx=-1)
        pat = find_row_value(is_stmt, ["net profit after tax", "profit for the year", "profit for the period"], col_idx=-1)
        pbt = find_row_value(is_stmt, ["profit before tax", "profit before exceptional items and tax"], col_idx=-1)
        
        total_assets = find_row_value(bs, ["total assets", "total-assets", "total of assets"], col_idx=-1)
        equity = find_row_value(bs, ["total equity", "equity", "sub-total-equity", "equity and other equity"], col_idx=-1)
        total_liabilities = find_row_value(bs, ["total liabilities", "total equity and liabilities"], col_idx=-1)
        
        current_assets = find_row_value(bs, ["total current assets", "sub-total-current assets", "sub-total current assets"], col_idx=-1)
        current_liabilities = find_row_value(bs, ["total current liabilities", "sub-total-current liabilities", "sub-total current liabilities"], col_idx=-1)
        inventories = find_row_value(bs, ["inventories", "inventories including materials"], col_idx=-1)
        
        # Calculate ratios
        pat_margin = (pat / revenue * 100) if (revenue and pat and revenue != 0) else None
        roa = (pat / total_assets * 100) if (total_assets and pat and total_assets != 0) else None
        roe = (pat / equity * 100) if (equity and pat and equity != 0) else None
        current_ratio = (current_assets / current_liabilities) if (current_assets and current_liabilities and current_liabilities != 0) else None
        debt_equity = ((total_assets - equity) / equity) if (equity and total_assets and equity != 0) else None
        asset_turnover = (revenue / total_assets) if (revenue and total_assets and total_assets != 0) else None
        
        ratios.append({
            "FY": year,
            "Revenue (Cr)": revenue,
            "PAT (Cr)": pat,
            "PBT (Cr)": pbt,
            "Total Assets (Cr)": total_assets,
            "Equity (Cr)": equity,
            "PAT Margin %": pat_margin,
            "ROA %": roa,
            "ROE %": roe,
            "Current Ratio": current_ratio,
            "Debt-to-Equity": debt_equity,
            "Asset Turnover": asset_turnover,
        })
    
    return pd.DataFrame(ratios)


def main():
    """Main processing function."""
    print("Processing EICHER financial statements...")
    
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        # Process statements and common-size for each year
        for year in YEARS:
            # Balance Sheet
            bs = load_statement(year, "bs")
            if bs is not None:
                bs.to_excel(writer, sheet_name=f"{year}_BS", index=False)
                bs_cs = compute_common_size_bs(bs)
                if bs_cs is not None:
                    bs_cs.to_excel(writer, sheet_name=f"{year}_BS_CS", index=False)
            
            # Income Statement
            is_stmt = load_statement(year, "is")
            if is_stmt is not None:
                is_stmt.to_excel(writer, sheet_name=f"{year}_IS", index=False)
                is_cs = compute_common_size_is(is_stmt)
                if is_cs is not None:
                    is_cs.to_excel(writer, sheet_name=f"{year}_IS_CS", index=False)
            
            # Cash Flow Statement
            cf = load_statement(year, "cf")
            if cf is not None:
                cf.to_excel(writer, sheet_name=f"{year}_CF", index=False)
        
        # Calculate ratios
        ratios_df = calculate_ratios()
        ratios_df.to_excel(writer, sheet_name="Ratios_Summary", index=False)
        
        print(f"[OK] Processed {len(YEARS)} years of financial statements")
        print(f"[OK] Common-size analysis completed")
        print(f"[OK] Financial ratios calculated")
    
    print(f"\n[OK] Output saved to: {OUTPUT_XLSX}")
    print("\nSummary of calculated ratios:")
    print(ratios_df[["FY", "PAT Margin %", "ROA %", "ROE %", "Current Ratio"]].to_string(index=False))


if __name__ == "__main__":
    main()

