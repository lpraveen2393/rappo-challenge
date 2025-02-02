import requests
from bs4 import BeautifulSoup
import json
import re

def sanitize_url(company_name):
    """Sanitize company name to match the URL format."""
    company_name = company_name.lower()  # Lowercase for consistency
    company_name = re.sub(r'[^a-z0-9-]', '', company_name)  # Remove non-alphanumeric characters except dash
    return company_name

def scrape_mongodb_case_studies():
    base_url = 'https://www.splunk.com/en_us/customers/success-stories/'
    case_studies = ['checkpoint', 'bosch', 'imdex', 'slack', 'engie', 'rent-the-runway',
                    'saskte', 'sapura', 'transunion', 'ersilia', 'delivery-hero', 'dana',
                    'carnival', '2c2p', 'unitel', 'asics', 'travis-perkins',
                    'ace', 'visca', 'imprivata', 'yelp', 'meggitt', 'kurt-geiger',
                    'hyphen-group', 'zillow', 'rappi', 'yokogawa', 'manpowergroup', 'cloudreach',
                    'puma', 'namely', 'orbis', 'apromore']    
    results = []
    
    for site in case_studies:
        try:
            # Sanitize the site name to match URL format
            site_url = sanitize_url(site)
            url = f'{base_url}{site_url}.html'
            response = requests.get(url)
            
            # Skip sites that return a 404 error
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            name_element = soup.find('span', class_="author")
            
            if name_element:
                name_title_company = name_element.get_text(strip=True)
                
                # Assuming the name is at the start, followed by the title and company after a comma or dash
                parts = [part.strip() for part in name_title_company.split(",", 2)]
                
                # Assign values for name, title, company
                name = parts[0] if len(parts) > 0 else "Unknown Name"
                title = parts[1] if len(parts) > 1 else "Unknown Title"
                company = parts[2] if len(parts) > 2 else site.capitalize()

                # Append the structured result as per the desired JSON format
                results.append({
                    "company": company,
                    "testimonial": {
                        "name": name,
                        "title": title,
                        "company": company,
                        "URL": url
                    }
                })
            else:
                print(f"Name not found for site: {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"Exception for the site: {url} - Error: {str(e)}")
    
    return results

def save_to_json(data, filename="splunk_case_studies.json"):
    """Saves the scraped data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")

if __name__ == "__main__":
    extracted_data = scrape_mongodb_case_studies()
    save_to_json(extracted_data)
