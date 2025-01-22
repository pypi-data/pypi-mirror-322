from googlesearch import search


def google(query: str, num_results=5, unique=True):
    urls = list(search(query, num_results=num_results, unique=unique))
    https_urls = [url for url in urls if 'http' == url[:4]]
    return https_urls
