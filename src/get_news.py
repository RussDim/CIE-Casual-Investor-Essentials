# Google News API
import pandas as pd
from GoogleNews import GoogleNews
import logging

logging.basicConfig(level=logging.INFO)


def get_news_articles(ticker):
    googlenews = GoogleNews(lang='en')
    googlenews.search(ticker)
    news_articles = googlenews.result()
    links = googlenews.get_links()
    articles_df = pd.DataFrame(news_articles, columns=['title', 'desc', 'date', 'source', 'link'])
    articles_df = articles_df[['title', 'desc', 'date', 'link']]
    articles_df = articles_df.rename(columns={'title': 'Title', 'desc': 'Description', 'date': 'Date', 'link': 'Link'})
        # Save DataFrame as CSV file
    articles_df.to_csv('articles.csv', index=False)
    logging.info("done updating articles")