import datetime
import os
from myapp.models import Owner, UserProfile, JudgeProfile, Contract, Subcontract, Transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")


# def run():
user = UserProfile(
    '0924043687',
    'محمد',
    'مجاهد'
)

user.save()

owner1 = Owner(
    123123123,
    '1'
)
owner1.save()

owner2 = Owner(
    bank_account_id=456456456,
    owner_type='2'
)

owner2.save()

owner3 = Owner(
    789789789,
    '3'
)

owner3.save()

judge = JudgeProfile(
    '123456',
    'پرداخت نوین'
)

judge.save()

contract = Contract(
    '111111',
    123123123,
    456456456,
    '4000000',
    'دلار',
    '20',
    '1',
    '123456',
    '1',
    datetime.datetime.now(),
    'یک معامله برای تست',
    '1',
)

contract.save()

subcontract = Subcontract(
    '111110',
    '111111',
    789789789,
    '4000000',
    '20',
    '1',
    datetime.datetime.now(),
    'یک زیر معامله برای تست',
    '1',
)

subcontract.save()
transaction = Transaction(
    '2222',
    123123123,
    456456456,
    '1',
    1000000,
    '0924043687',
    '1',
)

transaction.save()
