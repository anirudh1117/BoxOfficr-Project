import datetime
import re
from uuid import UUID
from django.utils.crypto import get_random_string
from .exceptions import WebsiteAuthorizationError


def unix_time_millis():
    return datetime.datetime.now().timestamp() * 1000

def convert_date_time_to_unix_time_millis(dateTime):
    return dateTime.timestamp() * 1000

def convert_unix_time_millis_to_date_time(unixTime):
    unixTime = int(unixTime)
    return datetime.datetime.fromtimestamp(unixTime)

def is_valid_uuid(uuid):
    try:
        uuid_obj = UUID(str(uuid), version=4)
        return True
    except ValueError:
        return False


def string_to_uuid(uuidValue):
    return UUID(str(uuidValue))


def generate_password(len,allowed_chars):
    return str(get_random_string(length=len, allowed_chars=allowed_chars))

def get_Choices(dataList):
    l = list()
    for i in dataList:
        tup = (i,i.upper())
        l.append(tup)
    return tuple(l)

def slugify(s):
  s = s.upper().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

def common_error_message(message):
    context = {
        "detail" : message
    }
    return context


def check_school_and_current_session(request):
    if request.user:
        website = request.user.website
        if website:
            return website
        else:
            raise WebsiteAuthorizationError()


def get_initials_from_string(name):
    if len(name) == 0:
        return ''
    
    name = name.replace('.', ' ')
    initial_list = re.split(" ", name)
    initial_name = ''

    for word in initial_list:
        if word != "" or len(word) > 0:
            initial_name = initial_name + word[0].upper()

    return initial_name

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def calculate_age_difference(born, death):
    return death.year - born.year - ((death.month, death.day) < (born.month, born.day))

def convert_budget(budget):
    """
    Convert budget into millions and crores.

    Parameters:
    budget (float): The budget amount in base currency.

    Returns:
    dict: A dictionary containing the budget in millions and crores.
    """
    # Conversion factors
    million_conversion_factor = 1_000_000
    crore_conversion_factor = 10_000_000
    
    budget_in_millions = budget / million_conversion_factor
    budget_in_crores = budget / crore_conversion_factor
    
    return str(round(budget_in_millions,2)) + ' million ( ' + str(round(budget_in_crores,2)) + ' crore) '

def calculate_next_year():
    today = datetime.date.today()
    return today.year + 1

def crore_to_million(crore):
    """
    Converts an amount from crores to millions.

    Args:
    crore (float): The amount in crores.

    Returns:
    float: The amount in millions.
    """
    # 1 crore is equal to 10 million
    million = crore * 10
    return million
