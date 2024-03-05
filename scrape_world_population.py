import logging
import requests

from bs4 import BeautifulSoup
from config import postgres_db_params, world_population_url
from database import truncate_and_insert_to_database

logging.basicConfig(level=logging.INFO)

def scrape_world_population(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing country names and populations
        tables = soup.find_all('table', class_='table table-striped table-bordered')
        if not tables:
            logging.error("No tables found on the page.")
            return None
        
        # Assuming the first table contains the desired data
        table = tables[0]
        
        # Initialize a list of dictionaries to store scraped data
        data = []
        
        # Loop through each row in the table skipping the header row
        for row in table.find_all('tr')[1:]:
            # Extract country name and population from each row
            columns = row.find_all('td')
            country_name = columns[1].text.strip()
            population = int(columns[2].text.strip().replace(',', ''))
            
            # Construct a dictionary representing the record
            record = {'country_name': country_name, 'population': population}
            
            # Append the record to the list of data
            data.append(record)
        
        # Return the list of dictionaries
        return data
    
    else:
        # If request was unsuccessful, print an error message
        logging.error(f"Failed to retrieve page: {response.status_code}")
        return None

if __name__ == "__main__":
    data = scrape_world_population(world_population_url)
    if data:
        # Assuming data is a list of tuples (country_name, population)
        table_name = "country_population"
        schema = {
            'fields': [
                {'name': 'country_name'},
                {'name': 'population'}
            ]
        }

        truncate_and_insert_to_database(table_name, data, schema, postgres_db_params)
        logging.info("Data stored to database")
    else:
        logging.error("No data retrieved from the website")
