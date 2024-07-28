import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import time

# שלב 1: טעינת רשימת החברות מ-Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(url)[0]

# שלב 2: פונקציה לקבלת נתוני תשואה ושווי שוק
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    returns = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100  # אחוז תשואה שנתית
    market_cap = stock.info['marketCap']
    return returns, market_cap

# איסוף נתונים עבור כל חברה ב-S&P 500
financial_data = []
for ticker in sp500_table['Symbol']:
    try:
        returns, market_cap = get_financial_data(ticker)
        financial_data.append((returns, market_cap))
        time.sleep(1)  # להימנע מהגבלה של ה-API
    except Exception as e:
        financial_data.append((None, None))
        print(f"Error fetching data for {ticker}: {e}")

# הוספת הנתונים לטבלה
sp500_table['Stock Returns (%)'] = [data[0] for data in financial_data]
sp500_table['Market Cap (Millions)'] = [data[1] for data in financial_data]

# שלב 3: פונקציה לקבלת מדיניות עבודה מהבית מאתר החברה
def get_work_from_home_policy(company_name):
    search_url = f"https://www.google.com/search?q={company_name}+work+from+home+policy"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # דוגמה לחיפוש טקסט מדיניות עבודה מהבית
    policy = "No data available"  # placeholder
    return policy

# איסוף נתוני עבודה מהבית עבור כל חברה ב-S&P 500
work_from_home_data = []
for company in sp500_table['Security']:
    try:
        policy = get_work_from_home_policy(company)
        work_from_home_data.append(policy)
        time.sleep(1)  # להימנע מהגבלה של ה-API
    except Exception as e:
        work_from_home_data.append("No data available")
        print(f"Error fetching work from home policy for {company}: {e}")

# הוספת הנתונים לטבלה
sp500_table['Work From Home Days'] = work_from_home_data

# שלב 4: שמירת הטבלה לקובץ CSV
sp500_table.to_csv('sp500_companies_work_from_home.csv', index=False)

# הצגת חלק מהטבלה
print(sp500_table.head(10))  # דוגמה להצגת 10 שורות ראשונות

