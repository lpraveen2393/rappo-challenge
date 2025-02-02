import requests
from bs4 import BeautifulSoup
import json

def scrape_atlassian_case_studies():
    base_url = 'https://www.atlassian.com/customers'
    results = []
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all customer story elements
        customer_stories = soup.find_all('a', class_='_311tkb7n')
        
        for story in customer_stories:
            try:
                # Extract the company name from the first img tag's alt attribute
                img_tag = story.find('img', loading='lazy')
                company_name = img_tag.get('alt', 'Unknown Company') if img_tag else 'Unknown Company'
                
                # Extract the name of the person from the h4 tag
                name_tag = story.find('h4')
                name = name_tag.get_text(strip=True) if name_tag else 'Unknown Name'
                
                # Extract the designation from the p tag with class 'eyebrow-md'
                designation_tag = story.find('p', class_='eyebrow-md')
                designation = designation_tag.get_text(strip=True) if designation_tag else 'Unknown Designation'
                
                # Skip entries where any value is unknown
                if company_name == 'Unknown Company' or name == 'Unknown Name' or designation == 'Unknown Designation':
                    continue
                
                # Create a dictionary with extracted data
                results.append({
                    "company": company_name,
                    "testimonial": {
                        "name": name,
                        "title": designation,
                        "company": company_name,
                        "URL": base_url
                    }
                })
            except Exception as e:
                print(f"Error processing one customer story: {str(e)}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {str(e)}")
    
    return results

def save_to_json(data, filename="atlassian_case_studies.json"):
    """Saves the scraped data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")

if __name__ == "__main__":
    extracted_data = scrape_atlassian_case_studies()
    save_to_json(extracted_data)
