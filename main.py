import requests
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_PERCENT_CHANGE = 5

API_Endpoint = "https://www.alphavantage.co/query"
Stock_API_key = ""                 # type your stock api key

News_API_key = ""                  # type your api news key

my_email = "test@email.com"        # type your email
password = ""                      # type your password


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_trade():
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "outputsize": "compact",
        "apikey": API_Endpoint,
    }
    response = requests.get(url=API_Endpoint, params=parameters)
    data = response.json()
    days_data = data["Time Series (Daily)"].values()

    yesterday_closing = float(days_data[0]["4. close"])
    day_before_yesterday = float(days_data[1]["4. close"])
    list_closing = [yesterday_closing, day_before_yesterday]

    difference_prices = list_closing[0] - list_closing[-1]
    difference_prices_percent = round((difference_prices / list_closing[0]) * 100, 2)
    if abs(difference_prices_percent) > STOCK_PERCENT_CHANGE:
        # print and Get News
        get_news(COMPANY_NAME)
        send_message(difference_prices_percent)


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_news(company_name):
    parameters_news = {
        "q": company_name,
        "sortBy": "publishedAt",
        "language": 'en',
        "apikey": News_API_key,
    }
    response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    print(response_news.json())
    headline1 = response_news.json()["articles"][0]["title"]
    headline2 = response_news.json()["articles"][1]["title"]
    headline3 = response_news.json()["articles"][2]["title"]

    description1 = response_news.json()["articles"][0]["description"]
    description2 = response_news.json()["articles"][1]["description"]
    description3 = response_news.json()["articles"][2]["description"]

    headlines_list = [headline1, headline2, headline3]
    headlines_string = ["".join([i if ord(i) < 128 else " " for i in headline]) for headline in headlines_list]

    descriptions_list = [description1, description2, description3]
    descriptions_string = ["".join([i if ord(i) < 128 else " " for i in description]) for description in
                           descriptions_list]
    return headlines_string, descriptions_string


# STEP 3
# Send a message with the percentage change and each article's title and description to your email.
def send_message(increase):
    headlines_string, descriptions_string = get_news(COMPANY_NAME)

    message = f"Subject: {COMPANY_NAME}: {increase}%\n\nHeadline: {headlines_string[0]}.\n" \
              f"Brief: {descriptions_string[0]}.\n\nHeadline: {headlines_string[1]}.\n" \
              f"Brief: {descriptions_string[1]}.\n\nHeadline: {headlines_string[2]}.\n" \
              f"Brief: {descriptions_string[2]}."
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=message,
        )


get_trade()

# Format the SMS message like this:
"""
TSLA: +2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
 by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of 
 the coronavirus market crash.
or
"TSLA: -5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of 
the coronavirus market crash.
"""
