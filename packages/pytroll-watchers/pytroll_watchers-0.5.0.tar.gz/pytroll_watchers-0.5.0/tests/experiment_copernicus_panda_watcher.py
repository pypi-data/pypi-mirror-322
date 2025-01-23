address = "https://panda.copernicus.eu/"

# def test_one():
#     session = requests.session()
#     session.headers = {
#             "User-Agent": "pytroll/0.0.1",
#         }
#     session.auth = ("martinraspaud","FoHeefe2AeB.")
#     session.get("https://panda.copernicus.eu/Mc3OpenSearch/webapi/Services/getDescriptionFile")


import feedparser
import requests

feed = feedparser.parse("http://panda.copernicus.eu/Mc3OpenSearch/webapi/Services/getProducts/?instrument=SAR&start=2024-07-15T00:00:00.000Z&end=2024-07-30T00:00:00.000Z")
print(f"found {len(feed.entries)} entries for SAR data since july 15th.")
for entry in feed.entries:
    for link in entry["links"]:
        if link["type"] == "application/binary":
            download_link = link["href"]
            filename = entry["id"].rsplit(":", 1)[-1]
            print(f"downloading {filename}")
print(entry)
            #print(f"from {download_link}")

            # with requests.get(download_link, stream=True) as r:
            #     r.raise_for_status()
            #     with open(filename, "wb") as f:
            #         for chunk in r.iter_content(chunk_size=8192):
            #             f.write(chunk)
