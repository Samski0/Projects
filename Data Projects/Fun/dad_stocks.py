import yfinance as yf 
import pandas as pd


tickers = ['VOO', 'QQQ', 'WIX']

for ticker in tickers:
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    last_quote = data['Close'].iloc[-1]
    

    print(ticker, last_quote)


# Merge with S&P 500 data
    combined_df = pd.merge(sp500_df, wfh_df, how='left', on='Company Name')

    print('Combining data')

    # Save combined data to an Excel file
    combined_df.to_excel('combined_data_2020.xlsx', index=False)

    print("Combined data has been created successfully.")
