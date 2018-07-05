# linker
A simple website URL and link checker. It crawls through a given sitemap for every accessible URL, checks that the response is 200 (OK). It then procedes to check every link in the html of that page. 


## Setup 

It is reccomended to use a virtual environment with this package, although it is not essential.

To install the required packages use `pip`:
`pip install -r requirements.txt`

## Usage
To run the script, ensure you have python (min <2.7) installed and run:
`python linker.py`

You will be asked if you want to use a sitemap hosted on your website, these are often found at `/sitemap.xml`. If you would rather use a local xml file, leave it blank and you will be prompted for the filepath of the sitemap.

The script will carry out the test on every url, and then output a report of all the broken links found.
