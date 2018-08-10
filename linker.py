import configparser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup as Soup


def check_links(site_map_file, auth=None):
    tree = ET.parse(site_map_file)
    root = tree.getroot()
    url_count = len(list(root))

    # List of tuples for broken links [(url, error, source_url)]
    broken_links = []
    # Every checked page url, including it's links from a tags
    checked_links = []
    site_url = root[0][0].text
    print(site_url)

    try:
        if auth:
            print(auth)
            r = requests.get(site_url, auth=(auth[0], auth[1]))
        else:
            r = requests.get(site_url)
    except:
        print("Could not reach site")
        quit
    
    if r.status_code == 401:
        return 401
    # Loop over every <url> tag from the site map
    for page_index, page in enumerate(root):
        # Get the <loc> tag its contents
        url = page[0].text
        # Encoded to include multi-lang urls
        url.encode('utf-8')

        if (url not in checked_links) and ("/assets" not in url):
            print('Page {} of {} | Checking url [{}]'.format(page_index + 1, url_count, url))

            try:
                if auth:
                    r = requests.get(url, auth=(auth[0], auth[1]))
                else:
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

            # Checks every link's href (<a/>) on the page
            for link_index, link in enumerate(links):           
                link_url = link.get('href')

                if link_url not in checked_links:
                    checked_links.append(link_url)

                    # Allows for links that are relative, ie - /contact
                    if link_url and not (link_url.startswith("http") or link_url.startswith("mailto:")):
                        if link_url.startswith("/"):
                            link_url = site_url[0:-1] + link_url
                        else:
                            link_url = site_url + link_url

                    print('Page {} of {} | Link {} of {} | Checking url [{}]'.format(page_index + 1, url_count, link_index + 1, links_count, link_url))
                    try:
                        if auth:
                            r = requests.get(link_url, auth=(auth[0],auth[1]))
                        else:
                            r = requests.get(link_url)
                    except: 
                        print("Uh oh, something went wrong checking {}".format(link_url))
                        if link_url == '':
                            link_url = link
                        broken_links.append((link_url, "Unknown error", url))
                    status_code = r.status_code
                    if status_code != 200:
                        print('Non-OK response ({}) on link_url: {}'.format(link_url,status_code))
                        print(link)
                        broken_links.append((link_url, status_code, url))
                else: 
                    continue
            
    return broken_links

def download_map(url):
 # Download XML sitemap from given web address and save to file
    site_map_file = 'tmp_sitemap.xml'
    try: 
        # Get the xml map from the site
        xml = requests.get(url, stream=True)
        with open(site_map_file, 'w') as file:
            file.write(xml.text)
        
        return site_map_file
    except: 
        raise SystemExit("Could not download the xml file, please try again.")


def send_mail(config, subject, message):
    """
    sends an email from using the EMAIL config in config.ini
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config['AdminEmailAddress'], config['AdminEmailPassword'])

    msg = MIMEMultipart()
    msg['From'] = config['AdminEmailAddress']
    msg['To'] = config['RecipientEmailAddress']
    msg['Subject'] = subject

    body = message

    msg.attach(MIMEText(body, 'plain'))

    txt = msg.as_string()
    server.sendmail(config['AdminEmailAddress'], config['RecipientEmailAddress'], txt)
    server.quit()


# Allows command line running
def run():
    config = configparser.ConfigParser()
    config.read('config.ini')

    gen_conf = config['GENERAL']
    email_conf = config['EMAIL']

    # Local file
    if gen_conf['UseLocalFile'] == 'yes':
        site_map_file = gen_conf['LocalSitemapFile']

    # Download sitemap from given url
    elif gen_conf['DownloadSitemap'] == 'yes':
        site_map_file = download_map(gen_conf['RemoteSitemapUrl'])

    # Check links
    if os.path.exists(site_map_file):
        broken_links = check_links(site_map_file)
    else:
        print("The file at {} could not be found. Please check the config and ensure the filepath is correct.".format(site_map_file))
    
    # If sitemap was downloaded, remove
    try:
        os.remove('tmp_sitemap.xml')
    except FileNotFoundError:
        pass


    ###### Output ######
    # Outputs results to a file, the terminal and via email

    count_broken_links = len(broken_links)
    subject = "ALERT: {} Broken Links detected for {}".format(count_broken_links, email_conf['SiteName'])
    message = "There were {} broken links found! \n".format(count_broken_links)
    
    # Formats the links into a human readable format
    for url, error, location in broken_links:
        broken_link = """
            ===== BROKEN LINK ============
            Broken Link Path: {}
            Location: {}
            Error: {}
            ==============================
        """.format(str(url), str(location), str(error))
        print( "Error: ", str(error), "  =>  URL: ", str(url), "Location: ", str(location))
        message += broken_link
    
    # Writes to file
    if gen_conf['OutputToFile'] == 'yes':
        with open(gen_conf['OutputFileName'], 'w') as file:
            file.write(message)

    # Emails the output to address specified in config.ini
    if email_conf['EmailOutput'] == 'yes':
        send_mail(email_conf, subject, message)

if __name__ == "__main__":
    run()
   