import os
import requests
import json


def test_endpoint(url, input, context):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    print(f"URL: {url}")
    print(f"Input: {input}")
    print(f"Context: {context}")

    try:
        res = requests.post(url, headers=headers, data=json.dumps(input))
        res.raise_for_status()

        print(f"Response: {res.text}")
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)


if __name__ == "__main__":
    heroku_api_link = os.environ.get("HEROKU_API_LINK")

    print("TESTING API...")

    url = heroku_api_link

    # REQUIRED: Please check input data if correct
    data = {
        "Store": 1111,
        "DayOfWeek": 4,
        "Date": "2014-07-10",
        "Customers": 4100,
        "Open": 1,
        "Promo": 0,
        "StateHoliday": "0",
        "SchoolHoliday": 1,
    }

    test_endpoint(url=url, input=data, context="")
