
# Proposal

# Section 1: Motivation and Purpose

**Our role:** 

Data Scientist interested in supporting individuals in their pursuit of financial independence.  

**Target audience:** 

The main target audience of the app is casual investors with limited access to financial data who are interested in monitoring companies in which they are interested in investing or currently own shares in.

Beginner investors are often overwhelmed by the flood of data available online on any given financial instrument.  The Casual Investor Essentials (CIE) app aims to simplify things and provide an update on a stock price along with the most recent news articles regarding the stock.  In this way the user does not have to switch between multiple screens to get a quick update on what is happening with their company of interest.


## Section 2: Description of Data

The app combines live data from two sources through dedicated Python packages, which provide data on demand by the user:

1. `yfinance`: a python package which provides a broad range of financial data on a given stock.  The app utilizes one field of all the available data, namely:

- `Close`: closing price of the stock on a daily basis for a period in days specified by the user.

2. `GoogleNews`: a Python package, which provides access on Google News articles in real time. The package returns Pandas DataFrame based on a stock ticker entered by the user containing the following data:
- `title`: the title of the news article
- `desc`: summary of the news article
- `date`: timestamp of when the article was published
- `link`: a link to the full article on the news article's source website


## Section 3: Research questions and usage scenarios

The CIE app aims to provide a quick update on the current and past stock price for a selected stock along with the 10 most recent news articles published on the stock of interest. The app answers the following usage questions:

- At what prices is my stock of interest trading today?
- What has been the stock price closing level over the past days, months, years?
- What news articles are published on this stock recently?
- What can each news article tell me about the changes the stock is experiencing?

The team behind the app targets one main group of users for the CIE app. This group consists of stock enthusiasts, who are constantly on the move and are looking for a quick update on a publicly traded company of interest. The target audience is young people in their 20s and early 30s who lead busy lifestyles, which make it necessary for them to be able to quickly get updates on their investing queries.

A typical user from this group would be represented by the following description:

Jane is a young professional working as a Data Scientist in Downtown Vancouver.  She commutes to and from work daily and spends her days working behind a screen.  During her work breaks, during her commute, and while drinking her morning coffee Jane likes to relax and not spend extensive time behind a computer.  She also likes to catch up on companies she holds in her investing portfolio.  Jane is always annoyed when she visits yahoo finance or google news by the flood of information and advertisements which come from big corporate websites.  That is why she wants to use a single app, no ads to see how the companies she is interested in, are trading and what are the latest news on these companies.


The Casual Investor Essentials app will provide Jane exactly what she needs.  Yahoo finance has the best publicly available financial data, while Google news does the best job of aggregating news by topic.  So by navigating to CIE app Jan will get both her trading update and the news updates she needs.  The app will minimize her screen time and will not burden her with noise.  
