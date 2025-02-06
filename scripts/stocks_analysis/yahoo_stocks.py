#l0tr1k yahoo stocks analysis, take ticker and add current price and company inf
#version 1.0

import pandas as pd
import yfinance as yf
from datetime import datetime

# Konfigurácia
INPUT_FILE = "stocks.xlsx"
OUTPUT_FILE = "stocks_updated.xlsx"
SHEET_NAME = "Hárok1"

def get_yahoo_data(symbol):
    """Získa finančné údaje pre symbol z Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        return {
            'Aktuálna cena': info.get('currentPrice', history['Close'].iloc[0] if not history.empty else 'N/A'),
            'P/E': info.get('trailingPE', 'N/A'),
            'EPS': info.get('trailingEps', 'N/A'),
            '52WeekHigh': info.get('fiftyTwoWeekHigh', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
            'Trhová kapitalizácia': info.get('marketCap', 'N/A'),
            'EBITDA': info.get('ebitda', 'N/A'),
            'Výnosy TTM': info.get('totalRevenue', 'N/A'),
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
