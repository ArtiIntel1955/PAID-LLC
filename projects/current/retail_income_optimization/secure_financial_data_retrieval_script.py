import requests
import json
from datetime import datetime
import pandas as pd
import time

def get_company_data(ticker, api_key):
    """
    Retrieve balance sheet data from Financial Modeling Prep API
    
    Args:
        ticker (str): Stock symbol (e.g., AAPL, BBY)
        api_key (str): FMP API key
    
    Returns:
        dict: Summary of key financial metrics
    """
    # Endpoint for the Balance Sheet (Annual)
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=12&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        data = response.json()
        
        if not data:
            return "No data found for this ticker."
        
        # Extracting the most recent 12 quarters of data
        summary = []
        for item in data[:12]:  # Get last 12 quarters
            quarter_data = {
                "Date": item.get("date"),
                "Symbol": item.get("symbol"),
                "Cash": item.get("cashAndCashEquivalents"),
                "Total Assets": item.get("totalAssets"),
                "Total Liabilities": item.get("totalLiabilities"),
                "Net Debt": item.get("netDebt"),
                "Current Assets": item.get("totalCurrentAssets"),
                "Current Liabilities": item.get("totalCurrentLiabilities"),
                "Inventory": item.get("inventory"),
                "Accounts Receivable": item.get("netReceivables")
            }
            summary.append(quarter_data)
        
        return summary
        
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_income_statement(ticker, api_key):
    """
    Retrieve income statement data from Financial Modeling Prep API
    
    Args:
        ticker (str): Stock symbol (e.g., AAPL, BBY)
        api_key (str): FMP API key
    
    Returns:
        dict: Summary of key income statement metrics
    """
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=12&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return "No income statement data found for this ticker."
        
        summary = []
        for item in data[:12]:  # Get last 12 quarters
            quarter_data = {
                "Date": item.get("date"),
                "Symbol": item.get("symbol"),
                "Revenue": item.get("revenue"),
                "Gross Profit": item.get("grossProfit"),
                "Operating Income": item.get("operatingIncome"),
                "Net Income": item.get("netIncome"),
                "EPS": item.get("eps"),
                "EBITDA": item.get("ebitda")
            }
            summary.append(quarter_data)
        
        return summary
        
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def get_cash_flow(ticker, api_key):
    """
    Retrieve cash flow statement data from Financial Modeling Prep API
    
    Args:
        ticker (str): Stock symbol (e.g., AAPL, BBY)
        api_key (str): FMP API key
    
    Returns:
        dict: Summary of key cash flow metrics
    """
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=12&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return "No cash flow data found for this ticker."
        
        summary = []
        for item in data[:12]:  # Get last 12 quarters
            quarter_data = {
                "Date": item.get("date"),
                "Symbol": item.get("symbol"),
                "Operating Cash Flow": item.get("operatingCashFlow"),
                "Investing Cash Flow": item.get("investingCashFlow"),
                "Financing Cash Flow": item.get("financingCashFlow"),
                "Free Cash Flow": item.get("freeCashFlow")
            }
            summary.append(quarter_data)
        
        return summary
        
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def calculate_key_ratios(balance_sheet_data, income_data):
    """
    Calculate key financial ratios from balance sheet and income statement data
    
    Args:
        balance_sheet_data (list): Balance sheet data
        income_data (list): Income statement data
    
    Returns:
        list: Calculated ratios for each quarter
    """
    ratios = []
    
    for bs, inc in zip(balance_sheet_data, income_data):
        ratio_data = {
            "Date": bs["Date"],
            "Gross Margin %": round((inc["Gross Profit"] / inc["Revenue"]) * 100, 2) if inc["Revenue"] != 0 else 0,
            "Operating Margin %": round((inc["Operating Income"] / inc["Revenue"]) * 100, 2) if inc["Revenue"] != 0 else 0,
            "Net Margin %": round((inc["Net Income"] / inc["Revenue"]) * 100, 2) if inc["Revenue"] != 0 else 0,
            "Current Ratio": round(bs["Current Assets"] / bs["Current Liabilities"], 2) if bs["Current Liabilities"] != 0 else 0,
            "Debt to Equity": round(bs["Total Liabilities"] / bs["Total Assets"], 2) if bs["Total Assets"] != 0 else 0,
            "Return on Assets %": round((inc["Net Income"] / bs["Total Assets"]) * 100, 2) if bs["Total Assets"] != 0 else 0
        }
        ratios.append(ratio_data)
    
    return ratios

def get_company_profile(ticker, api_key):
    """
    Get company profile information from Financial Modeling Prep API
    
    Args:
        ticker (str): Stock symbol (e.g., AAPL, BBY)
        api_key (str): FMP API key
    
    Returns:
        dict: Company profile information
    """
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return "No company profile found for this ticker."
        
        profile = data[0]  # Take the first (and usually only) entry
        summary = {
            "Company Name": profile.get("companyName"),
            "Industry": profile.get("industry"),
            "Sector": profile.get("sector"),
            "Market Cap": profile.get("marketCap"),
            "Price": profile.get("price"),
            "Beta": profile.get("beta"),
            "Volume": profile.get("volAvg"),
            "Last Dividend": profile.get("lastDiv"),
            "CEO": profile.get("ceo"),
            "Website": profile.get("website"),
            "Description": profile.get("description")
        }
        
        return summary
        
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def save_to_csv(data, filename):
    """
    Save data to CSV file
    
    Args:
        data (list or dict): Data to save
        filename (str): Name of the output file
    """
    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")

def main():
    """
    Main function to demonstrate the financial data retrieval
    """
    try:
        from config import FMP_API_KEY as API_KEY
    except ImportError:
        print("Configuration file not found.")
        print("Please ensure 'config.py' exists with your API key.")
        return
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    ticker = input("Enter the stock ticker (e.g., BBY for Best Buy): ").upper()
    
    print(f"\nRetrieving financial data for {ticker}...")
    
    # Get balance sheet data
    print("\nFetching balance sheet data...")
    balance_sheet = get_company_data(ticker, API_KEY)
    if isinstance(balance_sheet, str):
        print(balance_sheet)
    else:
        print(f"Retrieved {len(balance_sheet)} quarters of balance sheet data")
        save_to_csv(balance_sheet, f"{ticker}_balance_sheet.csv")
    
    # Get income statement data
    print("\nFetching income statement data...")
    income_stmt = get_income_statement(ticker, API_KEY)
    if isinstance(income_stmt, str):
        print(income_stmt)
    else:
        print(f"Retrieved {len(income_stmt)} quarters of income statement data")
        save_to_csv(income_stmt, f"{ticker}_income_statement.csv")
    
    # Get cash flow data
    print("\nFetching cash flow data...")
    cash_flow = get_cash_flow(ticker, API_KEY)
    if isinstance(cash_flow, str):
        print(cash_flow)
    else:
        print(f"Retrieved {len(cash_flow)} quarters of cash flow data")
        save_to_csv(cash_flow, f"{ticker}_cash_flow.csv")
    
    # Calculate ratios if we have both balance sheet and income data
    if isinstance(balance_sheet, list) and isinstance(income_stmt, list):
        print("\nCalculating key financial ratios...")
        ratios = calculate_key_ratios(balance_sheet, income_stmt)
        if ratios:
            save_to_csv(ratios, f"{ticker}_ratios.csv")
            print(f"Calculated {len(ratios)} quarters of financial ratios")
    
    # Get company profile
    print("\nFetching company profile...")
    profile = get_company_profile(ticker, API_KEY)
    if isinstance(profile, str):
        print(profile)
    else:
        save_to_csv(profile, f"{ticker}_profile.csv")
        print("Company profile retrieved")
    
    print(f"\nAll data for {ticker} has been retrieved and saved to CSV files.")

if __name__ == "__main__":
    main()