import requests
from bs4 import BeautifulSoup
import json
import re

def sanitize_url(company_name):
    """Sanitize company name to match the URL format."""
    company_name = company_name.lower()  # Lowercase for consistency
    company_name = re.sub(r'[^a-z0-9-]', '', company_name)  # Remove non-alphanumeric characters except dash
    return company_name

def scrape_fastly_case_studies():
    base_url = 'https://www.fastly.com/customers/'
    case_studies = [
        "jetblue", "gannett-usa", "new-relic", "ticketmaster", "doordash", "outbrain", 
        "quantcdn", "river-island", "mastodon-gmbh", "znipe-tv", "gourmet-gift-baskets", 
        "kubernetes", "rust-foundation", "bending-spoons", "cohost", "imgix", "ekstra-bladet", 
        "stuff", "ppg", "flagsmith", "python-software-foundation", "stellate", "thg", "anchor", 
        "squarespace", "life-time", "le-monde", "itvx", "brad's-deals", "duolingo", "tf1", 
        "strawberry", "gitguardian", "nine-entertainment", "dansons", "paramount-global", "marfeel", 
        "commonbond", "winning-group", "bambora", "movember", "finnai", "chef", "namely", "leantaa", 
        "prezi", "sauce-labs", "one-medical", "cybrary", "remitly", "bloomnation", "magnolia", 
        "gannett-usa-today-network", "bell-media", "spread-group", "amazee.io", "the-weather-company", 
        "api.video", "seenthis", "storytel", "loveholidays", "giphy", "pronovias-group", "slate", 
        "taboola", "trademe", "litium", "ofx", "axon", "betterment", "maritz", "launchdarkly-compute", 
        "network-10", "edgemesh", "brandfolder", "mediaset-espanã", "blackpepper", "jw-player", 
        "linktree", "nine", "filestack", "superology", "dena", "mercari", "madeiramadeira", "split", 
        "realtyninja", "skillsoft", "shoptimize", "launchdarkly", "dunelm", "ticketmaster", "hoodoo", 
        "yottaa", "gannett", "rvu", "atresmedia", "jimdo", "la-redoute", "wikihow", "fubotv", "big-cartel", 
        "yelp", "deliveroo", "1stdibs", "wayfair", "wanelo", "foursquare", "shazam", "wired", "7digital", 
        "business-insider", "opera", "new-relic", "imgur", "the-guardian", "boots-uk", "drupal-association", 
        "github", "sonatype", "wenner-media"
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
            
            # Find the <cite> element containing the name and designation
            cite_tag = soup.find('cite')
            if cite_tag:
                # Extract the name (from strong tag inside cite)
                name_tag = cite_tag.find('strong')
                name = name_tag.get_text(strip=True) if name_tag else "Unknown Name"
                
                # Extract the designation (from the part before the company name)
                designation_text = cite_tag.get_text(strip=True).split(",")[0]
                designation = designation_text if designation_text else "Unknown Title"
                
                # The company name is taken directly from the URL (formatted from the case study list)
                company = site.replace('-', ' ').capitalize()

                # If either name or designation is unknown, skip this entry
                if name == "Unknown Name" or designation == "Unknown Title":
                    print(f"Skipping site: {url} due to unknown name or title.")
                    continue

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
                print(f"Cite element not found for site: {url}")
                
        except requests.exceptions.RequestException as e:
            print(f"Exception for the site: {url} - Error: {str(e)}")
    
    return results

def save_to_json(data, filename="fastly_case_studies.json"):
    """Saves the scraped data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")

if __name__ == "__main__":
    extracted_data = scrape_fastly_case_studies()
    save_to_json(extracted_data)
