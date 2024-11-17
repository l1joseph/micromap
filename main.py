# main.py

from pubmed_api import fetch_citing_pmcids, fetch_article_details
from database import create_connection, create_table, insert_publication

def main():
    database = "publications.db"

    # Create a database connection
    conn = create_connection(database)

    # Create publications table
    if conn is not None:
        create_table(conn)
    else:
        print("Error! Cannot create the database connection.")

    # Define the PMCID (without "PMC" prefix)
    pmcid = "7015180"

    # Fetch citing PMCIDs
    citing_pmcs = fetch_citing_pmcids(pmcid)

    # Fetch and store article details
    for citing_pmcid in citing_pmcs:
        article_details = fetch_article_details(citing_pmcid)
        publication = (
            article_details['pmcid'],
            article_details['title'],
            article_details['abstract'],
            article_details['pub_date'],
            article_details['corresponding_author'],
            article_details['corresponding_author_email'],
            ', '.join(article_details['author_list']),
            ', '.join(article_details['affiliations_list']),
            article_details['pubmed_id'],
            article_details['url']
        )
        insert_publication(conn, publication)

    # Close the database connection
    if conn:
        conn.close()

if __name__ == '__main__':
    main()

