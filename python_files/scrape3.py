import requests
import json
from bs4 import BeautifulSoup

def extract_name_details(text):
    """
    Extracts name, designation, and company from testimonial text.
    Handles cases with single or multiple commas.
    Example Inputs:
        - "Sun Lei, Senior Technical Director, XTransfer"
        - "Steve Hwang, CTO of NOD Games"
    """
    parts = [part.strip() for part in text.split(",")]

    name = parts[0] if len(parts) > 0 else "Unknown"
    title = parts[1] if len(parts) > 1 else "Unknown"
    
    # If there's a third part, assume it's the company name
    if len(parts) > 2:
        company = parts[2]
    else:
        # Try to extract company from title if it contains "of"
        if " of " in title:
            title, company = title.split(" of ", 1)
        else:
            company = "Unknown"

    return name, title, company

def scrape_mongodb_case_studies():
    base_url = 'https://www.mongodb.com/solutions/customer-case-studies/'
    case_studies = [
        'xtransfer', 'csx', 'clarifruit', 'autodesk', 'swisscom',
        'lokalee', 'paychex', 'relevanceai', 'vainu', 'indeed', 'cargurus',
        'igt-solutions', 'naologic', 'toyota-connected', 'poste-italiane',
        'cisco', 'ceto', 'questflow', 'bumpp', 'scalestack', 'syncly',
        'okta', 'gong', 'wolt', 'zebra', 'kovai', 'ada', 'playvox', 'arc-xp',
        'one-ai-success-story', 'payload', 'telefonica', 'nod-games', 'verizon', 'tim'
    ]

    results = []

    for site in case_studies:
        if not site.strip():  # Ignore empty or malformed entries
            continue

        try:
            url = f'{base_url}{site}'
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract testimonial text
            name_element = soup.find('p', style="font-size: 16px; color: #798186;")
            testimonial_text = name_element.get_text(strip=True) if name_element else ""

            if testimonial_text:
                name, title, company = extract_name_details(testimonial_text)
            else:
                name, title, company = "Unknown", "Unknown", "Unknown"

            results.append({
                "company": company,
                "testimonial": {
                    "name": name,
                    "title": title,
                    "company": company,
                    "URL": url
                }
            })

        except requests.exceptions.RequestException as e:
            print(f"Error getting results for this website: {url}")
    return results

# Scrape data
data = scrape_mongodb_case_studies()

# Save results to a JSON file
with open("mongodb_case_studies.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Scraping completed. Data saved to case_studies.json")
