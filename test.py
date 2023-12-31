import requests

url = "http://localhost:7439/get_form"

tests = [
    "phone=+7 912 445 67 89&date=2023-01-16",
    "name=Feedback form&email=user2@example.com&phone=+7 912 345 78 89",
    "date=2021-02-16&text=This are a product order form.",
    "phone=+7 919 345 67 89&date=2023-03-16",
    "email=user5@example.com&phone=+7 911 945 67 89&date=2023-10-16",
    "name=Booking form&email=user10@example.com&phone=+7 919 345 67 89&date=2023-03-16&text=This is a booking form.",
    "name=Booking form&email=user4@example.com&lastname=Merkulov&phone=+7 919 345 67 89&date=2023-03-16&text=This is a booking form.",
    "phone=+7 912 445 67 89&date=2023-01-16&lastname=Merkulov",
    "phone=+7 987 654 43 21&date=01.01.2002&text=Hello Hello Hello Hello.",
    'phone=+7 919 345 67 89&date=2023-03-16'
]

for test in tests:
    data = {k: v for k, v in (item.split("=") for item in test.split("&"))}
    response = requests.post(url, json=data)
    if response.status_code == 422:
        print(response.json())
    else:
        print(response.text)