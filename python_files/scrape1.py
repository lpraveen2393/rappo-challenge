import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote
import re

def clean_company_name(name):
    """Clean and format company name for URL"""
    return re.sub(r'[^a-zA-Z0-9-]', '', name.lower().replace(' ', '-'))

def extract_testimonial(soup):
    """Extract testimonial details from various HTML structures"""
    # Option 1: Modern template with tw-flex classes
    testimonial = soup.find('div', class_='tw-flex tw-flex-col tw-justify-center')
    if testimonial:
        spans = testimonial.find_all('span')
        if len(spans) >= 3:
            return {
                'name': spans[0].text.strip(),
                'title': spans[1].text.strip(),
                'company': spans[2].text.strip()
            }
    
    # Option 2: Customer info template
    testimonial = soup.find('div', class_='customer-info')
    if testimonial:
        divs = testimonial.find_all('div')
        if len(divs) >= 3:
            return {
                'name': divs[0].text.strip(),
                'title': divs[1].text.strip(),
                'company': divs[2].text.strip()
            }
    
    # Option 3: Generic search for grouped name/title/company
    # Look for any div containing three consecutive text elements
    divs = soup.find_all('div')
    for div in divs:
        text_elements = [el.text.strip() for el in div.find_all(['div', 'span', 'p']) 
                        if el.text.strip() and not el.find(['div', 'span', 'p'])]
        if len(text_elements) >= 3:
            # Check if the elements look like a testimonial (name usually has two words)
            if ' ' in text_elements[0] and len(text_elements[0].split()) <= 3:
                return {
                    'name': text_elements[0],
                    'title': text_elements[1],
                    'company': text_elements[2],
                    
                }
    
    return None

def scrape_datadog_cases():
    base_url = "https://www.datadoghq.com/case-studies/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Get main page
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all company cards
    companies = []
    cards = soup.find_all('div', class_='card-body')
    
    for card in cards:
        company_element = card.find('h5')
        if not company_element:
            continue
            
        company_name = company_element.text.strip()
        company_url_name = clean_company_name(company_name)
        
        # Skip if company name is empty
        if not company_url_name:
            continue
            
        company_url = f"{base_url}{company_url_name}"
        
        # Add delay to avoid overwhelming the server
        time.sleep(1)
        
        try:
            # Get company-specific page
            company_response = requests.get(company_url, headers=headers)
            company_soup = BeautifulSoup(company_response.text, 'html.parser')
            
            testimonial = extract_testimonial(company_soup)
            if testimonial:
                companies.append({
                    'company': company_url_name,
                    'testimonial': testimonial
                })
        except Exception as e:
            print(f"Error processing {company_name}: {str(e)}")
    
    return companies

def main():
    # Scrape data
    case_studies = scrape_datadog_cases()
    
    # Save to JSON file
    with open('datadog_testimonials.json', 'w', encoding='utf-8') as f:
        json.dump(case_studies, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully scraped {len(case_studies)} case studies")
    return case_studies

if __name__ == "__main__":
    main()
