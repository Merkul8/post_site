from tinydb import TinyDB

templates = {
    1: {
        "name": "Registration form",
        "email": "user1@example.com",
        "phone": "+7 912 445 67 89",
        "date": "2023-01-16",
        "text": "This is a registration form.",
    },
    2: {
        "name": "Feedback form",
        "email": "user2@example.com",
        "phone": "+7 912 345 78 89",
        "text": "This is a feedback form.",
    },
    3: {
        "name": "Product order form",
        "email": "user3@example.com",
        "phone": "+7 912 345 11 89",
        "date": "2023-02-16",
        "text": "This is a product order form.",
    },
    4: {
        "name": "Booking form",
        "email": "user4@example.com",
        "phone": "+7 919 345 67 89",
        "date": "2023-03-16",
        "text": "This is a booking form.",
    },
    5: {
        "name": "Callback request form",
        "email": "user5@example.com",
        "phone": "+7 911 945 67 89",
        "date": "2023-10-16",
        "text": "This is a callback request form.",
    },
    6: {
        "name": "Hello:)",
        "email": "user6@example.com",
        "phone": "+7 987 654 43 21",
        "date": "01.01.2002",
        "text": "Hello Hello Hello Hello.",
    },
}

db = TinyDB('db.json')

def save_templates_to_db(templates):
    for key, template in templates.items():
        db.insert({'id': key, 'template': template})

save_templates_to_db(templates)

def get_all_templates():
    templates = {}
    data = db.all()
    for item in data:
        templates[item['id']] = item['template']
    return templates