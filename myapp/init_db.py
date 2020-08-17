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
    src_owner=123123123,
    dst_owner=456456456,
    value_in_rial='4000000',
    remittance_currency='دلار',
    remittance_value='20',
    settlement_type='1',
    judge=judge,
    judge_vote='1',
    expire_date='2020-12-11',
    description='یک معامله برای تست',
    status='1',
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
