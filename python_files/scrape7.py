import requests
from bs4 import BeautifulSoup
import json
import re

def sanitize_url(company_name):
    """Sanitize company name to match the URL format."""
    company_name = company_name.lower()  # Lowercase for consistency
    company_name = re.sub(r'[^a-z0-9-]', '', company_name)  # Remove non-alphanumeric characters except dash
    return company_name

def scrape_case_studies():
    base_url = 'https://www.chef.io/customers'
    case_studies = [
        "azure", "bank-hapoalim", "capital-one", "cerner", "danske-bank", 
        "discount-tire", "google-cloud-platform", "greenway-health", "havenetec", 
        "ibm", "intility", "sap", "schuberg-philis", "shadow-soft", "shinola-detroit", 
        "slalom-consulting", "standard-bank", "meta", "ncr", "optum", "rakuten", 
        "relativity", "rizing", "tesco", "verisk-analytics", "walmart-irl", 
        "zynx-health", "target"
    ]
    results = []
    
    for site in case_studies:
        try:
            # Sanitize the site name to match URL format
            site_url = sanitize_url(site)
            url = f'{base_url}/{site_url}'  # Assuming the URL pattern
            
            response = requests.get(url)
            
            # Skip sites that return a 404 error
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the <figcaption> element
            figcaption = soup.find('figcaption')
            
            if figcaption:
                # Extract the name from the <cite> tag within <figcaption>
                name_tag = figcaption.find('cite')
                name = name_tag.get_text(strip=True) if name_tag else "Unknown Name"
                
                # Extract the designation from the <span> tag within <figcaption>
                designation_tag = figcaption.find('span')
                designation = designation_tag.get_text(strip=True) if designation_tag else "Unknown Title"
                
                # Extract company from designation (after a comma)
                company = designation.split(',')[-1].strip() if ',' in designation else site.capitalize()

                # Append the structured result as per the desired JSON format
                results.append({
                    "company": company,
                    "testimonial": {
                        "name": name,
                        "title": designation,
                        "company": company,
                        "URL": url
                    }
                })
            else:
                print(f"figcaption not found for site: {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"Exception for the site: {url} - Error: {str(e)}")
    
    return results

def save_to_json(data, filename="chef_case_studies.json"):
    """Saves the scraped data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")

if __name__ == "__main__":
    extracted_data = scrape_case_studies()
    save_to_json(extracted_data)
