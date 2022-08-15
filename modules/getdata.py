from lxml import etree
import requests
from io import StringIO
from modules.extract_csv_from_URL import extractURL


def get_data_from_gob(url):
    """This will get the data from the provided URL"""
    try:
        r = requests.get(url)
    except:
        return -1
    parser = etree.HTMLParser()
    # Decode the page content from bytes to string
    html = r.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    print(r.status_code)
    print(r.headers['content-type'])
    # print(r.content)
    parser.feed(str(r.content))
    return extractURL(tree)
