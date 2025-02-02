import requests
from bs4 import BeautifulSoup
import json

def scrape_case_studies():
    base_url = 'https://www.confluent.io/customers/'
    case_studies = [
        'alight', 'amway', '8x8', 'acertus', 'ao', 'affin-hwang-asset-management', 
        'apna', 'arcese', 'audacy', 'bmw-group', 'bank-btpn', 'bestsecret',
        'bigcommerce', 'booking-com', 'buzzvil', 'care-com', 'cerved', 
        'citizens-bank', 'curve', 'datev', 'dish-wireless', 'gep-worldwide', 
        'euronext', 'evo-banco', 'etc', 'drivecentric', 'dominos', 
        'dicks-sporting-goods', 'deutsche-bahn', 'dkvmobility', 'generali', 
        'globe-group', 'humana', 'instacart', 'intel', 'judo-bank', 'kakao-games', 
        'king', 'kredivo', 'meesho', 'michelin', 'moniepoint', 'nord-lb', 'nuuly', 
        'otto', 'one-mount-group', 'optimove', 'outsystems', 'picnic', 'q2', 'rbc', 
        'recursion', 'rodan-fields', 'roosevelt-and-delta-dental', 'sas', 
        'sei-investments', 'sainsburys', 'ticketmaster', 'sunpower', 'sumup', 
        'sulamerica', 'storyblocks', 'singapore-exchange', 'securityscorecard', 
        'sencrop', 'toolstation', 'trust-bank', 'vimeo', 'virta', 'zyte', 
        'ebay-korea', 'ifood'
    ]
    
    results = []

    for site in case_studies:
        try:
            url = f'{base_url}{site}'
            response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
            response.raise_for_status()  # Raise an error for bad responses
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the name element
            name_element = soup.find('p', class_=lambda x: x and "ContentfulEmbedTestimonial-module--name" in x)
            name = name_element.get_text(strip=True) if name_element else "Unknown Name"
            
            # Find the role and company element
            role_company_element = soup.find('p', class_=lambda x: x and "ContentfulEmbedTestimonial-module--roleAndCompany" in x)
            if role_company_element:
                role_company = role_company_element.get_text(strip=True)
                parts = [part.strip() for part in role_company.split(',', 1)]
                role = parts[0] if len(parts) > 0 else "Unknown Role"
                company = parts[1] if len(parts) > 1 else site.replace('-', ' ').title()
            else:
                role, company = "Unknown Role", site.replace('-', ' ').title()
            
            # Append the result with the structure requested
            results.append({
                "company": company,
                "testimonial": {
                    "name": name,
                    "title": role,
                    "company": company,
                    "URL": url
                }
            })

        except requests.exceptions.Timeout:
            print(f"Timeout occurred while trying to scrape {site}. Skipping...")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error {http_err.response.status_code} for {site}. Skipping...")
        except requests.exceptions.RequestException:
            print(f"Failed to scrape {site}. Skipping...")
        except Exception as e:
            print(f"Unexpected error for {site}: {str(e)}. Skipping...")

    return results

def save_to_json(data, filename="confluent_case_studies.json"):
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
