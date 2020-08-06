import datetime
import os
from myapp.models import UserProfile, JudgeProfile, Contract, Subcontract, Transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")


def run():
    user = UserProfile(
        '0924043687',
        'محمد',
        'مجاهد')

    owner = Owner(
        '1234567890',
        '1'
    )

    judge = JudgeProfile(
        '123456',
        'پرداخت نوین')

    contract = Contract(
        '111111',
        datetime.datetime.now(),
        '1',
        '4000000',
        'دلار',
        '20',
        '123456',
        '0924043687',
        '22222222',
        'نامعلوم',
        'یک معامله برای تست',
        '1', )

    subcontract = Subcontract(
        '111110',
        datetime.datetime.now(),
        '4000000',
        '20',
        'نامعلوم',
        'یک زیر معامله برای تست',
        '22222222',
        '111111',
        '1', )

    transaction = Transaction(
        '2222',
        '1',
        '1234567890',
        '3333333333',
        '1000000',
        '1',
        '0924043687',
    )
