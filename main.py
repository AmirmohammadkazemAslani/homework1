from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hi, this page is home."}


def regex_validate(text,pattern):
    import re
    result = re.match(pattern, str(text))
    if result:
        return True
    return False

persian_char = [" ", "ا", "آ", "ب", "پ", "ت", "ث", "ج", "چ", "خ", "ح", "د", "ذ", "ر", "ز", "ژ", "ئ", "س", "ش", "ص",
                "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "گ", "ل", "م", "ن", "و", "ه", "ي", "ك", "ء", "ی"]




# practice 1

class data_model(BaseModel):
    code : int

def check_code(code):
    if len(str(code)) != 11:
        raise HTTPException(status_code=203, detail="student code should be 11 digits!")
    year = int(str(code)[:3])
    if not 400 <= year <= 402:
        raise HTTPException(status_code=203, detail="year part is not correct!")
    middle = int(str(code)[3:9])
    if middle != 114150:
        raise HTTPException(status_code=203, detail="middle part is not correct!")
    index = int(str(code)[-2:])
    if not 1 <= index <= 99:
        raise HTTPException(status_code=203, detail="index is not correct!")
    return code


@app.get("/student_code/{student_code}")
async def student_code_path(student_code: int):
    code = check_code(student_code)
    return f"student code is correct. -> {code}"



@app.get("/student_code/")
async def student_code_query(code: int):
    code = check_code(code)
    return f"student code is correct. -> {code}"


@app.post("/student_code/")
async def student_code_query(obj:data_model):
    code = check_code(obj.code)
    return f"student code is correct. -> {code}"


#practice 2

def validate_Name(name):
    if len(name) > 10:
        raise HTTPException(status_code=203, detail="name is too long (must be less than 11 digits)")

    for i in name:
        if i not in persian_char:
            raise HTTPException(status_code=203, detail="name must be only contain persian characters")

    return name




@app.get("/name/{name}")
async def name(name:str):
    name = validate_Name(name)
    return {"message": f"your name is {name}"}


#practice 3


def validate_date(date):
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        raise HTTPException(status_code=203, detail="date format is not correct.")

    list = date.split("-")

    year = int(list[0])
    if year > 1402:
        raise HTTPException(status_code=203, detail="year is not correct.")

    month = int(list[1])
    if not 1 <= month <= 12:
        raise HTTPException(status_code=203, detail="month is not correct.")

    day = int(list[2])
    if not 1 <= day <= 31:
        raise HTTPException(status_code=203, detail="day is not correct.")

    return date


@app.get("/date/{date}")
async def birth_date(date:str):
    date = validate_date(date)
    return {"message": f"your date of birth is {date}"}


#practice 4

def validate_serial(serial):
    if len(serial) != 10 or serial[0] not in persian_char or serial[3] != "-" :
        raise HTTPException(status_code=203, detail="the format of serial is not correct.")
    try:
        a = int(serial[1:3])
        b = int(serial[4:])
    except:
        raise HTTPException(status_code=203, detail="the format of serial is not correct.")
    return serial

@app.get("/serial/{serial}")
async def serial(serial:str):
    serial = validate_serial(serial)
    return {"message": f"your identity serial number is {serial}"}


#practice 5

def validate_province(province):
    with open('province.json', 'r', encoding="utf-8") as json_file:
        provinces = json.load(json_file)
    provinces = list(provinces)
    new_provinces = []
    for p in provinces:
        new_provinces.append(p["name"])

    if province not in new_provinces:
        raise HTTPException(status_code=203, detail="province is not correct.")
    return provinces

@app.get("/province/{province}")
async def province(province:str):
    province = validate_province(province)
    return {"message": f"The province of your birth is {province}."}


#practice 6

def validate_city(city):
    with open('cities.json', 'r', encoding="utf-8") as json_file:
        cities = json.load(json_file)
    cities = list(cities)
    new_cities = []
    for c in cities:
        new_cities.append(c["name"])

    if city not in new_cities:
        raise HTTPException(status_code=203, detail="city is not correct.")

    return city

@app.get("/city/{city}")
async def city(city:str):
    city = validate_city(city)
    return {"message": f"The city of your birth is {city}."}


#practice 7

def validate_address(address):
    if len(address) > 100:
        raise HTTPException(status_code=203, detail="address is too long.")
    return address

@app.get("/address/{address}")
async def address(address:str):
    address = validate_address(address)
    return {"message": f"your address is: {address}."}


#practice 8

def validate_postalcode(postalcode):
    if not regex_validate(postalcode, "^(?!(\d)\1{3})[13-9]{4}[1346-9][ -]?[013-9]{5}$|^$"):
        raise HTTPException(status_code=203, detail="postalcode is not correct!")
    return postalcode

@app.get("/postal_code/{postalcode}")
async def postalcode(postalcode: int):
    postalcode = validate_postalcode(postalcode)
    return {"message": f"your postalcode is {postalcode}."}



#practice 9

def validate_mobile(mobile):
    if not regex_validate(str(mobile), "^(?:(?:(?:\\+?|00)(98))|(0))?((?:90|91|92|93|99)[0-9]{8})$"):
        raise HTTPException(status_code=203, detail="mobile number is not correct.")
    return mobile

@app.get("/mobile/{mobile}")
async def mobile(mobile: int):
    mobile = validate_mobile(mobile)
    return {"message": f"your mobile number is {mobile}."}



#practice 10

def validate_telephone(telephone):
    if not regex_validate(str(telephone), "^0[0-9]{2,}[0-9]{7,}$"):
        raise HTTPException(status_code=203, detail="telephone number is not correct.")
    return telephone

@app.get("/telephone/{telephone}")
async def telephone(telephone: int):
    telephone = validate_telephone(telephone)
    return {"message": f"your telephone number is {telephone}."}

#practice 11
def validate_college(college):
    colleges = ["فنی و مهندسی", "علوم پایه", "علوم انسانی", "دامپزشکی", "اقتصاد", "کشاورزی", "منابع طبیعی"]
    if college not in colleges:
        raise HTTPException(status_code=203, detail="college is not correct.")
    return colleges


@app.get("/college/{college}")
async def college(college: str):
    college = validate_college(college)
    return {"message": f"your college is {college}."}


#practice 12

def validate_field(field):
    fields = ["برق", "کامپیوتر", "عمران", "مکانیک", "معدن", "شهرسازی", "صنایع", "شیمی", "مواد", "هوافضا", "معماری"]
    if field not in fields:
        raise HTTPException(status_code=203, detail="field is not correct.")
    return fields

@app.get("/field/{field}")
async def field(field: str):
    field = validate_field(field)
    return {"message": f"your field is {field}."}



#practice 13

def validate_marital(marital):
    states = ["متاهل", "مجرد"]
    if marital not in states:
        raise HTTPException(status_code=203, detail="error.")
    return marital

@app.get("/marital/{marital}")
async def marital(marital: str):
    marital = validate_marital(marital)
    return {"message": f"you are {marital}"}


#practice 14

def validate_meli_code(value):
    """
    To see how the algorithem works, see http://www.aliarash.com/article/codemeli/codemeli.htm

    """
    value = str(value)

    if not len(value) == 10:
        # raise ValueError("کد ملی باید ۱۰ رقم باشد.")
        raise HTTPException(status_code=203, detail="national code is not correct.")

    res = 0
    for i, num in enumerate(value[:-1]):
        res = res + (int(num) * (10 - i))

    remain = res % 11
    if remain < 2:
        if not remain == int(value[-1]):
            # raise ValueError("کد ملی درست نیست")
            raise HTTPException(status_code=203, detail="national code is not correct.")
    else:
        if not (11 - remain) == int(value[-1]):
            # raise ValueError("کد ملی درست نیست")
            raise HTTPException(status_code=203, detail="national code is not correct.")

    return True


@app.get("/national_code/{national_code}")
async def national_code(national_code: int):
    national_code = validate_meli_code(national_code)
    return {"message": f"your national code is {national_code}."}



# practice 15

class Data(BaseModel):
    code : int
    name : str
    date : str
    serial : str
    province : str
    city : str
    address : str
    postalcode : int
    mobile : str
    telephone : str
    college : str
    field : str
    marital : str
    national_code : int


@app.post("/general")
async def general(data: Data):
    errors = dict()

    try:
        check_code(data.code)
    except Exception as e:
        errors["code"] = e


    try:
        validate_Name(data.name)
    except Exception as e:
        errors["name"] = e


    try:
        validate_date(data.date)
    except Exception as e:
        errors["date"] = e

    try:
        validate_serial(data.serial)
    except Exception as e:
        errors["serial"] = e


    try:
        validate_province(data.province)
    except Exception as e:
        errors["province"] = e

    try:
        validate_city(data.city)
    except Exception as e:
        errors["city"] = e

    try:
        validate_address(data.address)
    except Exception as e:
        errors["address"] = e


    try:
        validate_postalcode(data.postalcode)
    except Exception as e:
        errors["postalcode"] = e

    try:
        validate_mobile(data.mobile)
    except Exception as e:
        errors["mobile"] = e


    try:
        validate_telephone(data.telephone)
    except Exception as e:
        errors["telephone"] = e

    try:
        validate_college(data.college)
    except Exception as e:
        errors["college"] = e

    try:
        validate_field(data.field)
    except Exception as e:
        errors["field"] = e

    try:
        validate_marital(data.marital)
    except Exception as e:
        errors["marital"] = e


    try:
        validate_meli_code(data.national_code)
    except Exception as e:
        errors["national_code"] = e



    return errors

