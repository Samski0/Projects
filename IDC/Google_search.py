import requests
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search
import time

import requests
from bs4 import BeautifulSoup
import time
from googlesearch import search  # Ensure this package is installed: pip install google

def fetch_policy(company):
    query = f"{company} remote work policy 2020"
    search_results = search(query, num_results=10)
    
    for result in search_results:
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example of extracting text from a paragraph (customize this for actual structure)
            # Try finding paragraphs with keywords related to remote work policies
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if "work from home policy" in text.lower() or "remote work policy" in text.lower() or "telecommute" in text.lower():
                    return text
        except Exception as e:
            print(f"Failed to fetch data for {company} from {result}: {e}")
        time.sleep(1)  # Sleep to avoid making too many requests in a short time
    
    return "No data found"



def run():
    companies = ["Apple", "Microsoft", "Amazon", "Google", "Meta", "Salesforce", "IBM", "Netflix"]

    # Loop through each company and fetch the policy
    policies = []
    for company in companies:
        print(f"Fetching policy for {company}...")
        policy = fetch_policy(company)
        policies.append({'Company': company, 'Work-from-Home Policy': policy})
        print(f'finished fetching for {company}')

    # Convert the results to a DataFrame
    df = pd.DataFrame(policies)

    print(df)

    print('Starting to create dataFrame for wfh')
   
    # Create DataFrame for WFH data
    wfh_df = pd.DataFrame(df, columns=['Company Name', 'WFH Policy'])
    print(wfh_df)


if __name__ == '__main__':
    run()