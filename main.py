from datetime import datetime
import re
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator
from models import get_all_templates

app = FastAPI(debug=True)

class EmailField(BaseModel):
     email: EmailStr

class PhoneField(BaseModel):
    phone: str

    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'\+7 \d{3} \d{3} \d{2} \d{2}', v):
            raise ValueError('Invalid phone number')
        return v

class DateField(BaseModel):
    date: datetime

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%d.%m.%Y')
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
           raise ValueError('Invalid date format')
        return v
    
class TextField(BaseModel):
    text: str

class FormInput(BaseModel):
    date: DateField
    phone: PhoneField
    email: EmailField
    text: TextField

# Основная логика
@app.post("/get_form")
def get_form(form_data: Dict[str, str]):
    form_data = needed_fields(form_data)
    templates = get_all_templates()
    for _, template in templates.items():
        # Если форма соответствует шаблону возвращаем имя шаблона
        result = get_validated_form(template, form_data)
        if result:
            return result
    else:
        # Иначе, проверяем типы полей
        return check_form(form_data)

# Воврат имени шаблона    
def get_validated_form(fields_dict: dict, form_dict: dict) -> str:
    result = None
    flag = 0
    for k, _ in fields_dict.items():
        if k in form_dict and form_dict[k] == fields_dict[k]:
            flag += 1
    if len(form_dict) == flag:
        result = fields_dict['name']
    return result

# Воврат словаря в случае если шаблон не найден
def check_form(form_data: dict) -> dict:
    result_dict = {}
    ann = FormInput.__annotations__
    for key, _ in form_data.items():
        if ann.get(key):
            result_dict[key] = ann.get(key).__name__
    return result_dict

# Сортировка нужных полей в пришедшей форме
def needed_fields(form_data: dict):
    sorted_form_data = {}
    needed_fields_list = ['date', 'phone', 'email', 'text']
    for i in form_data.keys():
        if i in needed_fields_list:
            sorted_form_data[i] = form_data[i]
    return sorted_form_data