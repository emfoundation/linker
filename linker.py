import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as Soup
import requests


print("Enter sitemap url - ie, https://www.google.com/sitemap.xml [Leave blank to use local file]:")
url = input()

if url == '':
    print("Enter the filename for the XML sitemap, include extension:")
    site_map_file = input()
else: 
    # Download XML file from site
    try: 
        xml = requests.get(url, stream=True)
        with open('xml_sitemap.xml', 'w') as file:
            file.write(xml.text)
        site_map_file = 'xml_sitemap.xml'
    except: 
        raise SystemExit("Could not download the xml file, please try again.")


tree = ET.parse(site_map_file)
root = tree.getroot()
url_count = len(list(root))

# List of tuples for broken links [(url, error, source_url)]
broken_links = []
# Every checked page url, including it's links from a tags
checked_links = []

# Loop over every <url> tag from the site map
for index, page in enumerate(root):
    # Get the <loc> tag its contents
    url = page[0].text
    # Encoded to include multi-lang urls
    url.encode('utf-8')
    print('{} of {} | Checking url [{}]'.format(index + 1, url_count, url))

    if url not in checked_links and "/assets" not in url:
        try:
            r = requests.get(url)
        except: 
            print("Uh oh, something went wrong checking {}".format(url))
            broken_links.append((url, "Unknown error", url))

        status_code = r.status_code
        if status_code != 200:
            print('Non-OK response ({}) on url: {}'.format(url,status_code))
            broken_links.append((url, status_code, url))

        checked_links.append(url)
        html = r.text
        soup = Soup(html, 'html.parser')

        links = soup.find_all('a')
        links_count = len(links)

        for index, link in enumerate(links):
            link_url = link.get('href')
            print('{} of {} | Checking url [{}]'.format(index + 1, links_count, link_url))

            if link_url not in checked_links:
                try:
                    r = requests.get(link_url)
                except: 
                    print("Uh oh, something went wrong checking {}".format(link_url))
                    broken_links.append((link_url, "Unknown error", url))

                status_code = r.status_code
                if status_code != 200:
                    print('Non-OK response ({}) on link_url: {}'.format(link_url,status_code))
                    broken_links.append((link_url, status_code, url))

                checked_links.append(link_url)
    else: 
        print('Link already checked')
        continue


for url, error, location in broken_links:
    print( "Error: " + str(error), "  =>  URL: " + url, "Location: " + location)

