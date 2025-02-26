import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_yahoo_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        data = {
            'Aktuálna cena': info.get('currentPrice', history['Close'].iloc[-1] if not history.empty else np.nan),
            'Odporúčanie': info.get('recommendationKey', 'N/A'),
            'Cieľová cena analytikov': info.get('targetMedianPrice', np.nan),
            'Počet analytikov': info.get('numberOfAnalystOpinions', np.nan),
            '52 Week High': info.get('fiftyTwoWeekHigh', np.nan),
            '52 Week Low': info.get('fiftyTwoWeekLow', np.nan),
            'P/E': info.get('trailingPE', np.nan),
            'Forward P/E': info.get('forwardPE', np.nan),
            'EPS': info.get('trailingEps', np.nan),
            'PEG Ratio': info.get('pegRatio', np.nan),
            'Trhová kapitalizácia': info.get('marketCap', np.nan),
            'Dividend Yield': info.get('dividendYield', np.nan) * 100 if info.get('dividendYield') is not None else np.nan,
            'Beta': info.get('beta', np.nan),
            'Výnosy TTM': info.get('totalRevenue', np.nan),
            'Profit Margin': info.get('profitMargins', np.nan),
            'Návratnosť vlastného kapitálu': info.get('returnOnEquity', np.nan),
            'Návratnosť aktív': info.get('returnOnAssets', np.nan),
            'Rast výnosov': info.get('revenueGrowth', np.nan),
            'Rast zisku': info.get('earningsGrowth', np.nan),
            'Celkový dlh': info.get('totalDebt', np.nan),
            'Celková hotovosť': info.get('totalCash', np.nan),
            'Free Cash Flow': info.get('freeCashflow', np.nan),
            'EBITDA': info.get('ebitda', np.nan),
        }
        
        data['Piotroski F-score'] = calculate_piotroski_score(ticker)
        data['Percent_Change'] = get_historical_data(ticker)
        
        return symbol, data
    except Exception as e:
        print(f"Chyba pri {symbol}: {str(e)}")
        return symbol, None

def calculate_piotroski_score(ticker):
    try:
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow
        
        score = 0
        
        if financials.loc['Net Income'].iloc[0] > 0:
            score += 1
        if cash_flow.loc['Operating Cash Flow'].iloc[0] > 0:
            score += 1
        roa_current = financials.loc['Net Income'].iloc[0] / balance_sheet.loc['Total Assets'].iloc[0]
        roa_previous = financials.loc['Net Income'].iloc[1] / balance_sheet.loc['Total Assets'].iloc[1]
        if roa_current > roa_previous:
            score += 1
        if cash_flow.loc['Operating Cash Flow'].iloc[0] > financials.loc['Net Income'].iloc[0]:
            score += 1
        if balance_sheet.loc['Long Term Debt'].iloc[0] < balance_sheet.loc['Long Term Debt'].iloc[1]:
            score += 1
        current_ratio_current = balance_sheet.loc['Current Assets'].iloc[0] / balance_sheet.loc['Current Liabilities'].iloc[0]
        current_ratio_previous = balance_sheet.loc['Current Assets'].iloc[1] / balance_sheet.loc['Current Liabilities'].iloc[1]
        if current_ratio_current > current_ratio_previous:
            score += 1
        if balance_sheet.loc['Common Stock'].iloc[0] <= balance_sheet.loc['Common Stock'].iloc[1]:
            score += 1
        gross_margin_current = (financials.loc['Gross Profit'].iloc[0] / financials.loc['Total Revenue'].iloc[0])
        gross_margin_previous = (financials.loc['Gross Profit'].iloc[1] / financials.loc['Total Revenue'].iloc[1])
        if gross_margin_current > gross_margin_previous:
            score += 1
        asset_turnover_current = financials.loc['Total Revenue'].iloc[0] / balance_sheet.loc['Total Assets'].iloc[0]
        asset_turnover_previous = financials.loc['Total Revenue'].iloc[1] / balance_sheet.loc['Total Assets'].iloc[1]
        if asset_turnover_current > asset_turnover_previous:
            score += 1
        
        return score
    except Exception as e:
        print(f"Chyba pri výpočte Piotroski F-score: {str(e)}")
        return np.nan

def get_historical_data(ticker):
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=180)
    hist = ticker.history(start=start_date, end=end_date)
    if not hist.empty:
        return (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100
    return None

def main():
    df = pd.read_excel('stocks_all.xlsx')
    symbols = df['Symbol'].tolist()
    
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_symbol = {executor.submit(get_yahoo_data, symbol): symbol for symbol in symbols}
        for future in as_completed(future_to_symbol):
            symbol, data = future.result()
            if data:
                results[symbol] = data
    
    for symbol, data in results.items():
        for key, value in data.items():
            df.loc[df['Symbol'] == symbol, key] = value
    
    df = df.sort_values('Percent_Change', ascending=False)
    df['6mRPS'] = (df['Percent_Change'].rank(ascending=False) / len(df)) * 100
    
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"stocks_updated_{current_datetime}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Dáta boli úspešne uložené do {output_file}")

if __name__ == "__main__":
    main()
