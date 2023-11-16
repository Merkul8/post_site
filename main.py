from datetime import datetime
import re
from typing import Any, Dict, Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(debug=True)


class FormField(BaseModel):
    email: str = Field(None, pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone: str = Field(None, pattern=r"^\+7 \d{3} \d{3} \d{2} \d{2}$")
    date: datetime = Field(None, format="%Y-%m-%d")
    text: str = Field(None)

    @classmethod
    def parse_obj(cls, obj):
        if 'date' in obj and isinstance(obj['date'], str):
            if re.match(r'\d{2}\.\d{2}\.\d{4}', obj['date']):
                obj['date'] = datetime.strptime(obj['date'], "%d.%m.%Y")
            elif re.match(r'\d{4}-\d{2}-\d{2}', obj['date']):
                obj['date'] = datetime.strptime(obj['date'], "%Y-%m-%d")
        return obj
    
    @property
    def field_types(self):
        return {name: field.type_ for name, field in self.__fields__.items()}


shablons = {
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
}

@app.post("/get_form")
def get_form(text: str):
    # Стереть следующие 5 строчек, будем принимать json вместо строки
    text = text.split('&')
    result_dict = {}
    for value in text:
        values_list = value.split('=')
        result_dict[values_list[0]] = values_list[1]
    for _, v in shablons.items():
        result = get_validated_form(v, result_dict)
        if result:
            return result
    else:
        return 'Совпадений нет'
   
def get_validated_form(fields_dict: dict, form_dict: dict) -> str:
    result = None
    flag = 0
    for k, _ in fields_dict.items():
        if k in form_dict and form_dict[k] == fields_dict[k]:
            # result = fields_dict['name']
            # break
            flag += 1
    if len(form_dict) == flag:
        result = fields_dict['name']
    return result
