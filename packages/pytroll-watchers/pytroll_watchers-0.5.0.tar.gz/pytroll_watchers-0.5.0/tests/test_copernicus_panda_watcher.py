from urllib.parse import urlencode, urlsplit, urlunsplit

from responses import _recorder
import responses
import requests


opensearch_url = "http://panda.copernicus.eu/Mc3OpenSearch/webapi/Services/getProducts/"

@responses.activate
def test_list():
    filter_params = dict(instrument="SAR", start="2024-11-14T00:00:00.000Z")
    query_string = urlencode(filter_params)
    url_bits = urlsplit(opensearch_url)
    url = urlunsplit((url_bits.scheme, url_bits.netloc, url_bits.path, query_string, ""))
    responses._add_from_file(file_path="tests/panda_search_response.yaml")
    feed_text = requests.get(url, timeout=60).text
    import feedparser

    feed = feedparser.parse(feed_text)
    assert len(feed.entries) == 6
