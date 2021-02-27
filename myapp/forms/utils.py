from django import forms
from myapp.models import *
from django.forms import Form, ModelForm
from myapp.client import *
from myapp.dao import *
import datetime
import jdatetime

# DateInput = partial(forms.DateInput, {'class': 'datepicker'})


EMPTY_FIELD_ERROR_MESSAGE = 'خطا: این فیلد نمی تواند خالی باشد!'

LOGIN_ROLES = [
    ('user', 'کاربر حساب'),
    ('judge', 'داور'),
]

SPECIAL_LOGIN_ROLES = [
    ('reporter', 'گزارش دهنده'),
    # ('admin', 'ادمین'),
]

TRANSACTION_TYPE = [
    ('1', 'پرداختی'),
    ('2', 'واریزی'),
]

REPORT_OWNER_TYPE = [
    ('RETURN', 'بازگشت'),
    ('EXPORTER', 'صادرکننده ها'),
]


def empty_field_validator(field_value):
    print("here3")
    if not field_value:
        raise forms.ValidationError(EMPTY_FIELD_ERROR_MESSAGE)


def jdate2timestamp(date):
    return jdatetime.datetime.strptime(date, "%Y/%m/%d").timestamp()
