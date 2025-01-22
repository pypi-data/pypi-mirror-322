from googlesearch import search


def google(query: str, max_urls=5, unique=True):
    urls = list(search(query, num_results=max_urls, unique=unique))
    https_urls = [url for url in urls if 'http' == url[:4]]
    return https_urls
