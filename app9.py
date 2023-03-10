"""
add pretty layout
"""

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
    articles_df = articles_df.rename(columns={'title': 'Title', 'desc': 'Description', 'date': 'Date', 'link': 'Link'})
    return articles_df


# Dash app
app = dash.Dash(__name__)  #external_stylesheets=['/css/app_stylesheet.css']

app.layout = html.Div(style={'backgroundColor': '#f2f2f2'}, children=[
    html.H1('CIE: Casual Investor Essentials', style={'textAlign': 'center', 'marginBottom': '50px'}),
    html.Div([
        html.Label('Enter a stock ticker'),
        dcc.Input(id='stock-ticker-input', value='AAPL', type='text')
    ]),
    html.Div([
        html.Label('Enter number of days of history'),
        dcc.Input(id='history-days-input', value=365, type='number')
    ]),
    html.Button('Update', id='update-button', style={'marginTop': '10px', 'marginBottom': '10px', 'backgroundColor': '#4CAF50', 'color': 'white'}),
    dcc.Graph(id='stock-chart', figure={}, style={'marginBottom': '30px'}),
    html.Div([
        html.H3('Latest News', style={'marginBottom': '10px'}),
        html.Div([
            dcc.Dropdown(
                id='news-sort-dropdown',
                options=[
                    {'label': 'Most Recent', 'value': 'recent'},
                    {'label': 'Most Relevant', 'value': 'relevant'}
                ],
                value='recent',
                clearable=False,
                style={'width': '200px'}
            ),
            html.Button('Sort', id='sort-button', style={'backgroundColor': '#4CAF50', 'color': 'white', 'marginLeft': '10px'})
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'marginBottom': '30px', 'padding': '10px', 'backgroundColor': '#f9f9f9'}),
    html.Table(id='news-table', children=[], style={
        'width': '100%',
        'backgroundColor': 'white',  
        'borderCollapse': 'collapse'})
])


@app.callback(
    Output('stock-chart', 'figure'),
    Input('update-button', 'n_clicks'),
    State('stock-ticker-input', 'value'),
    State('history-days-input', 'value')
)
def update_stock_chart(n_clicks, ticker='AAPL', days=365):
    if n_clicks is None:
        dates, closing_prices = get_stock_data(ticker, days)
        trace = go.Scatter(x=dates, y=closing_prices, mode='lines')
        layout = go.Layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
        figure = go.Figure(data=[trace], layout=layout)
        return figure
    else:
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
def update_news_table(n_clicks, sort_clicks, ticker='AAPL', sort_by='recent', days=365):
    if n_clicks is None and sort_clicks is None:
        news_articles_df = get_news_articles(ticker)
        if sort_by == 'recent':
            news_articles_df = news_articles_df.sort_values('Date', ascending=True)
        else:
            news_articles_df = news_articles_df.sort_values('Description', ascending=False)
        news_articles_df = news_articles_df.head(10)
        table_rows = [html.Tr(
            [html.Th(col, style={'width': '7%'}) if col == 'Date' else html.Th(col) for col in news_articles_df.columns])]
        for i in range(len(news_articles_df)):
            table_rows.append(html.Tr([
                html.Td(news_articles_df.iloc[i][col]) if col != 'Link' else html.Td(html.A('Link', href=news_articles_df.iloc[i]['Link']))
                for col in news_articles_df.columns
            ]))
        return html.Table(table_rows)
    else:
        news_articles_df = get_news_articles(ticker)
        if sort_by == 'recent':
            news_articles_df = news_articles_df.sort_values('Date', ascending=True)
        else:
            news_articles_df = news_articles_df.sort_values('Description', ascending=False)
        news_articles_df = news_articles_df.head(10)
        table_rows = [html.Tr(
            [html.Th(col, style={'width': '7%'}) if col == 'Date' else html.Th(col) for col in news_articles_df.columns])]
        for i in range(len(news_articles_df)):
            table_rows.append(html.Tr([
                html.Td(news_articles_df.iloc[i][col]) if col != 'Link' else html.Td(html.A('Link', href=news_articles_df.iloc[i]['Link']))
            for col in news_articles_df.columns
        ]))
    return html.Table(table_rows)


if __name__ == '__main__':
    app.run_server(debug=True)  
