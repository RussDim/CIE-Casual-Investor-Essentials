import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from GoogleNews import GoogleNews
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# Yahoo Finance API
def get_stock_data(ticker, days):
    stock_data = yf.download(ticker, period=f'{days}d')
    dates = stock_data.index.date
    closing_prices = stock_data['Close'].values
    return dates, closing_prices


# Google News API
def get_news_articles(ticker):
    googlenews = GoogleNews(lang='en')
    googlenews.search(ticker)
    news_articles = googlenews.result()
    articles_df = pd.DataFrame(news_articles, columns=['title', 'desc', 'date', 'source'])
    articles_df = articles_df[['title', 'desc', 'date']]
    return articles_df


# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.Label('Enter a stock ticker'),
        dcc.Input(id='stock-ticker-input', value='AAPL', type='text')
    ]),
    html.Div([
        html.Label('Enter number of days of history'),
        dcc.Input(id='history-days-input', value=365, type='number')
    ]),
    dcc.Graph(id='stock-chart', figure={}),
    html.Div([
        html.H3('Latest News'),
        dcc.Dropdown(
            id='news-sort-dropdown',
            options=[
                {'label': 'Most Recent', 'value': 'recent'},
                {'label': 'Most Relevant', 'value': 'relevant'}
            ],
            value='recent',
            clearable=False
        ),
        html.Table(id='news-table', children=[])
    ])
])

@app.callback(
    Output('stock-chart', 'figure'),
    Input('stock-ticker-input', 'value'),
    Input('history-days-input', 'value')
)
def update_stock_chart(ticker, days):
    dates, closing_prices = get_stock_data(ticker, days)
    trace = go.Scatter(x=dates, y=closing_prices, mode='lines')
    layout = go.Layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
    figure = go.Figure(data=[trace], layout=layout)
    return figure

@app.callback(
    Output('news-table', 'children'),
    Input('stock-ticker-input', 'value'),
    Input('news-sort-dropdown', 'value')
)
def update_news_table(ticker, sort_by):
    news_articles_df = get_news_articles(ticker)
    if sort_by == 'recent':
        news_articles_df = news_articles_df.sort_values('date', ascending=False)
    else:
        news_articles_df = news_articles_df.sort_values('desc', ascending=False)
    news_articles_df = news_articles_df.head(10)
    table_rows = []
    for i in range(len(news_articles_df)):
        table_rows.append(html.Tr([
            html.Td(news_articles_df.iloc[i]['title']),
            html.Td(news_articles_df.iloc[i]['desc']),
            html.Td(news_articles_df.iloc[i]['date'])
        ]))
    return table_rows

if __name__ == '__main__':
    app.run_server(debug=True)
