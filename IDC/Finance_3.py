
import requests
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search
import time

# Function to scrape S&P 500 companies from an archived Wikipedia page
def fetch_sp500_companies():
    archived_url = 'https://web.archive.org/web/20200101000000/https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_tables = pd.read_html(archived_url)
    sp500_df = sp500_tables[1]
    return sp500_df



# Function to fetch WFH policy data using NewsAPI with date filtering
def fetch_wfh_data(company_name, api_key):
    url = f"https://newsapi.org/v2/everything?q={company_name}+work+from+home&from=2020-01-01&to=2020-12-31&sortBy=relevancy&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    
    for article in articles:
        if "work from home" in article['description'].lower():
            return article['description']

def fetch_policy(company):
    query = f"{company} remote work in 2020"
    search_results = search(query, num_results=10)
    
    for result in search_results:
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example of extracting text from a paragraph (customize this for actual structure)
            paragraphs = soup.find_all('remote')
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if "remote" in text.lower():
                    return text
        except Exception as e:
            print(f"Failed to fetch data for {company} from {result}: {e}")
        time.sleep(1)  # Sleep to avoid making too many requests in a short time
    
    return "No data found"






def run():
    # Your NewsAPI key
    api_key =  'bbb' # Replace with your actual API key
    print('Fetching companies')
    # Fetch the S&P 500 companies
    sp500_df = fetch_sp500_companies()

    # Loop through each company and fetch the policy
    policies = []
    for index, row in sp500_df.iterrows():
        if index == 10:
            break
        company = row['Security']
        print(f"Fetching policy for {company}...")
        policy = fetch_policy(company)
        policies.append({'Company': company, 'Work-from-Home Policy': policy})

    # Convert the results to a DataFrame
    df = pd.DataFrame(policies)

    print('Starting to create dataFroame for wfh')
   
    # Create DataFrame for WFH data
    wfh_df = pd.DataFrame(df, columns=['Company Name', 'WFH Policy'])

    print('Starting merge with s&p data')

    sp500_df = sp500_df.rename(columns={'Security' : 'Company Name'})
    print('renamed sp500 column')

    print(wfh_df)
    print(sp500_df)



if __name__ == '__main__':
    run()

