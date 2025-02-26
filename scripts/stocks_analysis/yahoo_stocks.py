import pandas as pd
import yfinance as yf
from datetime import datetime

# Konfigurácia
INPUT_FILE = "stocks.xlsx"
SHEET_NAME = "Hárok1"
OUTPUT_FILE = f"stocks_updated_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"

def get_yahoo_data(symbol):
    """Získa finančné údaje pre symbol z Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        return {
            'Aktuálna cena': info.get('currentPrice', history['Close'].iloc[-1] if not history.empty else 'N/A'),
            'Odporúčanie': info.get('recommendationKey', 'N/A'),
            'Cieľová cena analytikov': info.get('targetMedianPrice', 'N/A'),
            'Počet analytikov': info.get('numberOfAnalystOpinions', 'N/A'),
            '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
            'P/E': info.get('trailingPE', 'N/A'),
            'Forward P/E': info.get('forwardPE', 'N/A'),
            'EPS': info.get('trailingEps', 'N/A'),
            'PEG Ratio': info.get('pegRatio', 'N/A'),
            'Trhová kapitalizácia': info.get('marketCap', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
            'Beta': info.get('beta', 'N/A'),
            'Výnosy TTM': info.get('totalRevenue', 'N/A'),
            'Profit Margin': info.get('profitMargins', 'N/A'),
            'Návratnosť vlastného kapitálu': info.get('returnOnEquity', 'N/A'),
            'Návratnosť aktív': info.get('returnOnAssets', 'N/A'),
            'Rast výnosov': info.get('revenueGrowth', 'N/A'),
            'Rast zisku': info.get('earningsGrowth', 'N/A'),
            'Celkový dlh': info.get('totalDebt', 'N/A'),
            'Celková hotovosť': info.get('totalCash', 'N/A'),
            'Free Cash Flow': info.get('freeCashflow', 'N/A'),
            'EBITDA': info.get('ebitda', 'N/A'),
            'Posledná aktualizácia': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    except Exception as e:
        print(f"Chyba pri {symbol}: {str(e)}")
        return None

def main():
    # Načítanie Excel súboru
    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    
    # Spracovanie každého symbolu
    for index, row in df.iterrows():
        symbol = row['Symbol']
        print(f"Spracúvam {symbol} ({index+1}/{len(df)})...")
        
        data = get_yahoo_data(symbol)
        if not data:
            continue
        
        # Aktualizácia dát
        for key, value in data.items():
            df.at[index, key] = value
    
    # Uloženie výsledkov
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Úspešne uložené do {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
