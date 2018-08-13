# linker
A simple website URL and link checker. It crawls through a given sitemap for every accessible URL, checks that the response is 200 (OK). It then procedes to check every link in the html of that page. 

This script does not create the sitemap for you, so for that you can a website such as https://freesitemapgenerator.com/ or https://www.xml-sitemaps.com/.

## Setup 

It is recommended to use a virtual environment with this package, although it is not essential.

To install the required packages use `pip`:
`pip install -r requirements.txt`

## Usage
### Command Line & Server side
To run the script, ensure you have python (min <2.7) installed and run:
`python linker.py`

Copy the contents of the `config.ini.example` file into `config.ini` in the same directory. 

Modify your config file with the details for your site:

**GENERAL CONFIG**

|Config option|Description|
|-------------|-----------|
UseLocalFile|yes (default) / no
LocalSitemapFile | File path + name relative to this directory
DownloadSitemap | yes / no (default)
RemoteSitemapUrl | The url of the sitemap hosted on your website
OutputToFile | yes (default) / no
OutputFileName | Name of the file that the results will store. Can be placed elsewhere using relative path

**EMAIL CONFIG**

|Config option|Description|
|-------------|-----------|
SiteName|The name of your site, this is for display only and gets used in the output for easier identification
EmailOutput|yes / no (default)
AdminEmailAddress|The address of that emails will be sent from
AdminEmailPassword|The password of the Admins email account *PLAIN TEXT!*
RecipientEmailAddress|The recipient's email where the output gets sent to

### Graphical interface
Enter the linker directory, and run:
`python main.py`

From here you can enter or browse for the filename of the XML sitemap, and click enter. 

#### HTTP Auth
If your site has http authentication, then you will be asked to enter the username and password for the site. These details are not stored. 

The script will carry out the test on every url, and then output a report of all the broken links found.
