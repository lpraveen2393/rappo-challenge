import requests
from bs4 import BeautifulSoup
import json
import re

def sanitize_url(company_name):
    """Sanitize company name to match the URL format."""
    company_name = company_name.lower()  # Lowercase for consistency
    company_name = re.sub(r'[^a-z0-9-]', '', company_name)  # Remove non-alphanumeric characters except dash
    return company_name

def scrape_circleci_case_studies():
    base_url = 'https://circleci.com/case-studies/'
    case_studies = [
        'snyk', '17live', 'adwerx', 'ana-systems', 'avvir', 'axios', 'baracoda', 'bolt', 
        'branch', 'brandfolder', 'brikl', 'cinnamon', 'clickmechanic', 
        'clockwise', 'contentful', 'corewide', 'cruise', 'curative', 'dollar-shave-club', 
        'droppe', 'eventbrite', 'fastlane', 'fastlane-neuralegion','firstlight',
        'fuse-autotech', 'gatsbyjs', 
        'gospotcheck', 'greenhouse', 'gresham-technologies', 'ground-x', 'gtlogic',
        'healthlabs', 
        'honeycomb', 'i2', 'incident-io', 'joy', 'kaizen-platform', 'karat', 'klara', 'launchdarkly', 
        'imagine-learning-classroom', 'line', 'lumigo', 'maze', 'moshi', 'netguru', 'co-branding-airtasker', 
        'outfit7', 'outreach', 'pantheon', 'pingboard', 'pitch', 'policyme', 'poplog', 'procore', 'procurify', 
        'pytorch', 'repairpal', 'returnalyze', 'rollbar', 'salecycle', 'sevenrooms', 'solarwinds', 
        'stack-builders', 'tanda', 'tessian', 'toss', 'travelex', 'tunaiku', 'voiceflow'
    ]
    results = []
    
    for site in case_studies:
        try:
            # Sanitize the site name to match URL format
            site_url = sanitize_url(site)
            url = f'{base_url}{site_url}/'
            response = requests.get(url)
            
            # Skip sites that return a 404 error
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the <span> element for name (class="morph_font-semibold")
            name_tag = soup.find('span', class_="morph_font-semibold")
            name = name_tag.get_text(strip=True) if name_tag else "Unknown Name"
            
            # Find the <span> element for designation (class="morph_block sm:morph_inline")
            designation_tag = soup.find('span', class_="morph_block sm:morph_inline")
            designation = designation_tag.get_text(strip=True) if designation_tag else "Unknown Title"
            
            # If either name or designation is unknown, skip this entry
            if name == "Unknown Name" or designation == "Unknown Title":
                print(f"Skipping site: {url} due to unknown name or title.")
                continue

            # Extract company name (usually from the designation or site name itself)
            company = site.replace('-', ' ').capitalize()

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
        except requests.exceptions.RequestException as e:
            print(f"Exception for the site: {url} - Error: {str(e)}")
    
    return results

def save_to_json(data, filename="circleci_case_studies.json"):
    """Saves the scraped data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")

if __name__ == "__main__":
    extracted_data = scrape_circleci_case_studies()
    save_to_json(extracted_data)
