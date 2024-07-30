from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of S&P 500 companies (this is just a sample, you need to add all the companies)
companies = ["Apple", "Microsoft", "Amazon", "Google", "Meta", "Salesforce", "IBM", "Netflix"]

def fetch_policy(company):
    query = f"{company} work from home policy 2024"
    search_results = search(query, num_results=10)
    
    for result in search_results:
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example of extracting text from a paragraph (customize this for actual structure)
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                text = paragraph.get_text()
                if "work from home" in text.lower():
                    return text
        except Exception as e:
            print(f"Failed to fetch data for {company} from {result}: {e}")
        time.sleep(1)  # Sleep to avoid making too many requests in a short time
    
    return "No data found"

# Loop through each company and fetch the policy
policies = []
for company in companies:
    print(f"Fetching policy for {company}...")
    policy = fetch_policy(company)
    policies.append({'Company': company, 'Work-from-Home Policy': policy})

# Convert the results to a DataFrame
df = pd.DataFrame(policies)

# Save the DataFrame to a CSV file
df.to_csv('work_from_home_policies.csv', index=False)

print("Data saved to work_from_home_policies.csv")




print('Fetched companies')
    # Collect WFH data
    wfh_data = []
    for index, row in sp500_df.iterrows():
        if index == 10:
            break
        try:
            company_name = row['Security']
            policy_info = fetch_wfh_data(company_name, api_key)
            print(policy_info)
            wfh_data.append([company_name, policy_info])
        except Exception as e:
            print(e, row)

    wfh_data = [data for data in wfh_data if data is not None]
    print(f'Found {len(wfh_data)} rows')