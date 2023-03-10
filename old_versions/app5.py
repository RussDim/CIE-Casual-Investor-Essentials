import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from GoogleNews import GoogleNews
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


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
    links = googlenews.get_links()
    articles_df = pd.DataFrame(news_articles, columns=['title', 'desc', 'date', 'source', 'link'])
    articles_df = articles_df[['title', 'desc', 'date', 'link']]
    return articles_df


# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Quick Stock'),
    html.Div([
        html.Label('Enter a stock ticker'),
        dcc.Input(id='stock-ticker-input', value='AAPL', type='text')
    ]),
    html.Div([
        html.Label('Enter number of days of history'),
        dcc.Input(id='history-days-input', value=365, type='number')
    ]),
    html.Button('Update', id='update-button'),
    dcc.Graph(id='stock-chart', figure={}),
    html.Div([
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
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '10px'}),
        html.Div([
            html.Button('Sort', id='sort-button'),
        ], style={'display': 'inline-block', 'vertical-align': 'top'}),
        html.Table(id='news-table', children=[])
    ])
])

@app.callback(
    Output('stock-chart', 'figure'),
    Input('update-button', 'n_clicks'),
    State('stock-ticker-input', 'value'),
    State('history-days-input', 'value')
)
def update_stock_chart(n_clicks, ticker, days):
    if n_clicks is None:
        return dash.no_update
    dates, closing_prices = get_stock_data(ticker, days)
    trace = go.Scatter(x=dates, y=closing_prices, mode='lines')
    layout = go.Layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
    figure = go.Figure(data=[trace], layout=layout)
    return figure

@app.callback(
    Output('news-table', 'children'),
    Input('update-button', 'n_clicks'),
    Input('sort-button', 'n_clicks'),
    State('stock-ticker-input', 'value'),
    State('news-sort-dropdown', 'value')
)
def update_news_table(n_clicks, sort_clicks, ticker, sort_by):
    if n_clicks is None and sort_clicks is None:
        return dash.no_update
    news_articles_df = get_news_articles(ticker)
    if sort_by == 'recent':
        news_articles_df = news_articles_df.sort_values('date', ascending=True)
    else:
        news_articles_df = news_articles_df.sort_values('desc', ascending=False)
    news_articles_df = news_articles_df.head(10)
    table_rows = [html.Tr([html.Th(col) for col in news_articles_df.columns])]  # add column headers
    for i in range(len(news_articles_df)):
        table_rows.append(html.Tr([
            html.Td(news_articles_df.iloc[i][col]) if col != 'link' else html.Td(html.A('link', href=news_articles_df.iloc[i]['link']))
            for col in news_articles_df.columns
        ]))
    return html.Table(table_rows)


if __name__ == '__main__':
    app.run_server(debug=True)  
