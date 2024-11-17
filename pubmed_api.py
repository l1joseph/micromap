import requests
from xml.etree import ElementTree

# Function to fetch citing PMCIDs
def fetch_citing_pmcids(pmcid):
    elink_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    elink_params = {
        'dbfrom': 'pmc',
        'linkname': 'pmc_pmc_cites',
        'from_uid': pmcid,
        'retstart': 0,
        'retmax': 100
    }

    citing_pmcs = []
    while True:
        response = requests.get(elink_url, params=elink_params)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)

        links_found = 0
        for linkset in root.findall('.//LinkSetDb'):
            linkname = linkset.find('LinkName').text
            if linkname == "pmc_pmc_cites":
                for link in linkset.findall('Link'):
                    citing_pmcid = link.find('Id').text
                    citing_pmcs.append(citing_pmcid)
                    links_found += 1

        if links_found < elink_params['retmax']:
            break
        else:
            elink_params['retstart'] += elink_params['retmax']

    return citing_pmcs

# Function to fetch detailed article information
def fetch_article_details(pmcid):
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        'db': 'pmc',
        'id': pmcid,
        'retmode': 'xml'
    }

    response = requests.get(efetch_url, params=efetch_params)
    response.raise_for_status()
    root = ElementTree.fromstring(response.content)

    article_details = {
        'pmcid': pmcid,
        'title': root.findtext('.//article-title', default=''),
        'abstract': root.findtext('.//abstract//p', default=''),
        'pub_date': root.findtext('.//pub-date//year', default='') + "-" + root.findtext('.//pub-date//month', default='') + "-" + root.findtext('.//pub-date//day', default=''),
        'corresponding_author': '',
        'corresponding_author_email': '',
        'author_list': [],
        'affiliations_list': [],
        'pubmed_id': root.findtext('.//article-id[@pub-id-type="pmid"]', default=''),
        'url': f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/"
    }

    for contrib in root.findall('.//contrib'):
        name = contrib.find('name')
        if name is not None:
            lastname = name.findtext('surname', default='')
            forename = name.findtext('given-names', default='')
            author = f"{forename} {lastname}"
            article_details['author_list'].append(author)
            if contrib.get('corresp') == 'yes':
                article_details['corresponding_author'] = author
                email = contrib.findtext('.//email', default='')
                article_details['corresponding_author_email'] = email

    for aff in root.findall('.//aff'):
        if aff.text is not None:
            article_details['affiliations_list'].append(aff.text.strip())

    return article_details

