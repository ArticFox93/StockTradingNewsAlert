import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "your own api key from alphavantage"
NEWS_API_KEY = "your own api key from newsapi"

TWILIO_ACCOUNT_SID = "your twilio account sid"
TWILIO_ACCOUNT_AUTH_TOKEN = "your twilio auth token"

VIRTUAL_TWILIO_NUMBER = "input your twilio number"
VERIFIED_NUMBER = "input your own verified number with twilio"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (data, value) in data.items()]
yesterday_data = data_list[0]
yesterdays_closing_data = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_data = day_before_yesterday_data["4. close"]

comparison = abs(float(yesterdays_closing_data) - float(day_before_yesterday_closing_data))
up_down = None
if comparison > 0:
    up_down = "👍"
else:
    up_down = "👎"

comparison_percent = round((comparison / float(yesterdays_closing_data)) * 100)

if abs(comparison_percent) > 5:

    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    article = response.json()["articles"]
    three_articles = article[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{comparison_percent}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER,
        )