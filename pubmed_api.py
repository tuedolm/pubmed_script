import requests
from xml.etree import ElementTree

base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
database = 'pubmed'
search_term = 'genome'
retmax = 100 # Maximum number of records to retrieve per API call
max_papers = 10000 # Maximum number of papers to retrieve
pmids = [] # List of PubMed IDs

# Retrieve papers until we have reached the desired maximum
while len(pmids) < max_papers:
    # Calculate the value for retstart based on the number of papers we have already retrieved
    retstart = len(pmids)
    
    # Construct the URL for the PubMed search API
    url = f"{base_url}esearch.fcgi?db={database}&term={search_term}&retmax={retmax}&retstart={retstart}"
    
    # Make the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response using ElementTree
        root = ElementTree.fromstring(response.content)
        
        # Extract the list of PubMed IDs
        pmids += [id_.text for id_ in root.findall('.//Id')]
        
        # If we have retrieved all available papers, break out of the loop
        if int(root.find('.//Count').text) <= len(pmids):
            break
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        break

# Construct the URL for the PubMed summary API
url = f"{base_url}efetch.fcgi?db={database}&id={','.join(pmids)}&retmode=xml"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response using ElementTree
    root = ElementTree.fromstring(response.content)
    
    # Extract the article metadata
    for article in root.findall('.//PubmedArticle'):
        pmid = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text
        abstract = article.find('.//AbstractText').text
        
        # Do something with the metadata (e.g. store it in a database, write it to a file, etc.)
        # ...
else:
    print(f"Error: {response.status_code} - {response.reason}")
