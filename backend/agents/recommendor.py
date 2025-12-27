import random
from utils.scraper import fetch_from_hm, fetch_from_zara, fetch_from_flipkart, fetch_from_amazon

def fetch_from_linked_sites(choices, linked_sites):
    results = {}
    for site in linked_sites:
        site_results = []
        for choice in choices:
            # if site == "HM":
            #     site_results.extend(fetch_from_hm(choice))
            if site == "Zara":
                site_results.extend(fetch_from_zara(choice))
            # elif site == "Flipkart":
            #     site_results.extend(fetch_from_flipkart(choice))
            elif site == "Amazon":
                site_results.extend(fetch_from_amazon(choice))
        random.shuffle(site_results)
        results[site] = site_results[:50]
    return results
