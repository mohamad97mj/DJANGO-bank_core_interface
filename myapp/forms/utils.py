from django import forms
from django.forms import ModelForm, TextInput, Form
from myapp.models import AuthProfile, UserProfile, JudgeProfile, Transaction, NormalContract, Subcontract
from django.utils.translation import gettext_lazy as _
from functools import partial
from myapp.utils import *
import datetime

# DateInput = partial(forms.DateInput, {'class': 'datepicker'})


EMPTY_FIELD_ERROR_MESSAGE = 'خطا: این فیلد نمی تواند خالی باشد!'

LOGIN_ROLES = [
    ('user', 'کاربر حساب'),
    ('judge', 'داور'),
]

TRANSACTION_TYPE = (
    ('1', 'پرداختی'),
    ('2', 'واریزی'),
)


def empty_field_validator(field_value):
    if not field_value:
        raise forms.ValidationError(EMPTY_FIELD_ERROR_MESSAGE)
