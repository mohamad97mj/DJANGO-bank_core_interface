import datetime
import os
from myapp.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")

# def run():
user = UserProfile(
    '11',
    'محمد',
    'مجاهد'
)


owner1 = Owner(
    123,
    OwnerType.IMPORTER
)

owner2 = Owner(
    bank_account_id=456,
    owner_type=OwnerType.EXCHANGER
)


owner3 = Owner(
    789,
    OwnerType.EXPORTER
)


judge = JudgeProfile(
    '2222',
    'پرداخت نوین'
)


normalcontract = NormalContract(
    src_owner=owner1.bank_account_id,
    dst_owner=owner2.bank_account_id,
    value_in_rial='4000000',
    remittance_currency='دلار',
    remittance_value='20',
    settlement_type=SettlementType.SINGLE,
    judge_national_id=judge.national_id,
    judge_name="پرداخت نوین",
    judge_vote=JudgeVote.NOT_JUDGED,
    expire_date='1400/05/11',
    description='یک معامله برای تست',
    status=ContractStatus.WAITING_FOR_EXCHANGER,
)


subcontract = Subcontract(
    parent=normalcontract.id,
    dst_owner=owner3.bank_account_id,
    value_in_rial='4000000',
    remittance_value='20',
    judge_vote=JudgeVote.NOT_JUDGED,
    expire_date=datetime.datetime.now(),
    description='یک زیر معامله برای تست',
    status=ContractStatus.WAITING_FOR_EXPORTER,
)

transaction = Transaction(
    owner=owner1.bank_account_id,
    otherside_owner=owner2.bank_account_id,
    value=1000000,
    operator=user.national_code,
    operator_type=OperatorType.USER,
)

user.save()
owner1.save()
owner2.save()
owner3.save()
judge.save()
normalcontract.save()
subcontract.save()
transaction.save()

# user.owners.add(owner1)
# user.owners.add(owner2)
# user.owners.add(owner3)
