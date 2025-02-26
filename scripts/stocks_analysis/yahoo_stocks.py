import pandas as pd
import yfinance as yf
from datetime import datetime

# Konfigurácia
INPUT_FILE = "stocks.xlsx"
# Generovanie názvu súboru s aktuálnym dátumom a časom
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"stocks_updated_{current_datetime}.xlsx"
#OUTPUT_FILE = "stocks_updated.xlsx"
SHEET_NAME = "Hárok1"

def get_yahoo_data(symbol):
    """Získa finančné údaje pre symbol z Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        return {
            'Aktuálna cena': info.get('currentPrice', history['Close'].iloc[0] if not history.empty else 'N/A'),
            # Nové analytické odhady a odporúčania
            'Cieľová cena analytikov': info.get('targetMedianPrice', 'N/A'),
            'Počet analytikov': info.get('numberOfAnalystOpinions', 'N/A'),
            'Odporúčanie': info.get('recommendationKey', 'N/A'),
            'Forward P/E': info.get('forwardPE', 'N/A'),
            'PEG Ratio': info.get('pegRatio', 'N/A'),
            # Finančné odhady
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
