import requests
import pandas as pd
import xml.etree.ElementTree as ET

# Define the stock ticker you want to search for
stock_ticker = "AAPL"

# Send an HTTP GET request to the Google News RSS feed API
url = f"https://news.google.com/rss/search?q={stock_ticker}&hl=en-US&gl=US&ceid=US:en"
response = requests.get(url)

# Parse the response XML using ElementTree
root = ET.fromstring(response.text)

# Extract the article data from the XML and store it in a list of dictionaries
articles = []
for item in root.findall("./channel/item"):
    title = item.find("title").text
    link = item.find("link").text
    pub_date = item.find("pubDate").text
    description = item.find("description").text
    articles.append({"title": title, "desc": description, "date": pub_date, "link": link})

# Convert the list of dictionaries into a Pandas DataFrame
df = pd.DataFrame(articles)

# Print the DataFrame
print(df)
