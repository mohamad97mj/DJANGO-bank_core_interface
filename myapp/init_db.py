import datetime
import os
from myapp.models import Owner, UserProfile, JudgeProfile, NormalContract, Subcontract, Transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")

# def run():
user = UserProfile(
    '1111',
    'محمد',
    'مجاهد'
)

user.save()

owner1 = Owner(
    123,
    '1'
)
owner1.save()

owner2 = Owner(
    bank_account_id=456,
    owner_type='2'
)

owner2.save()

owner3 = Owner(
    789,
    '3'
)

owner3.save()

judge = JudgeProfile(
    '2222',
    'پرداخت نوین'
)

judge.save()

normalcontract = NormalContract(
    src_owner=owner1,
    dst_owner=owner2,
    value_in_rial='4000000',
    remittance_currency='دلار',
    remittance_value='20',
    settlement_type='1',
    judge=judge,
    judge_vote='0',
    expire_date='1400/05/11',
    description='یک معامله برای تست',
    status='11',
)

normalcontract.save()

subcontract = Subcontract(
    parent=normalcontract,
    dst_owner=owner3,
    value_in_rial='4000000',
    remittance_value='20',
    judge_vote='0',
    expire_date=datetime.datetime.now(),
    description='یک زیر معامله برای تست',
    status='13',
)

subcontract.save()
transaction = Transaction(
    owner=owner1,
    otherside_owner=owner2,
    value=1000000,
    operator=user,
    operator_type='1',
)

transaction.save()
