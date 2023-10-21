import requests,datetime as dt
from newsapi import NewsApiClient
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY_STOCK_PRICE = "KMFZ786EMGIPOS4K"
API_KEY_STOCK_NEWS = "9b8607b85c5c4c98843a15d217951f74"

account_sid = 'AC2117b51f874d6c08512bcecf36601b40'
auth_token = '(authtoken)'

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : API_KEY_STOCK_PRICE,
}

now = dt.datetime.now()
year = now.year
month = now.month
day = now.day


response = requests.get(url= STOCK_ENDPOINT, params=parameters)
close_price_1dbf = float(response.json()["Time Series (Daily)"][f"{year}-{month}-{day-1}"]["4. close"])
close_price_2dbf = float(response.json()["Time Series (Daily)"][f"{year}-{month}-{day-2}"]["4. close"])

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return float("{:.2f}".format((abs(current - previous) / previous) * 100.0))
    except ZeroDivisionError:
        return float('inf')


if get_change(close_price_1dbf, close_price_2dbf) >= 5.0:
    newsapi = NewsApiClient(api_key='9b8607b85c5c4c98843a15d217951f74')

    top_headlines = newsapi.get_everything(
        q=COMPANY_NAME,
    )
    headlines = [article["title"] for article in top_headlines["articles"][:3]]
    descriptions = [article["description"] for article in top_headlines["articles"][:3]]


    final_message = ""
    for element in range(0,3):
        final_message += f"{STOCK_NAME}: 🔺{get_change(close_price_1dbf, close_price_2dbf)}\nHeadline: {headlines[element]}\nBrief: {descriptions[element]}\n"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+17817677738',
        body= final_message,
        to='+40761623757'
    )

    print(message.sid)



