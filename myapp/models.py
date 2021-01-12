from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
import jdatetime
import uuid
from enum import Enum


class ContractStatus(models.TextChoices):
    NONE = 'NONE', _('ایجاد نشده')
    WAITING_FOR_EXCHANGER_ACCEPTANCE = 'WAITING_FOR_EXCHANGER_ACCEPTANCE', _('در انتظار پذیرش صراف')
    WAITING_FOR_EXPORTER_ACCEPTANCE = 'WAITING_FOR_EXPORTER_ACCEPTANCE', _('در انتظار پذیرش صادرکننده')
    WAITING_FOR_IMPORTER_PAYMENT = 'WAITING_FOR_IMPORTER_PAYMENT', _('در انتظار پرداخت واردکننده')
    WAITING_FOR_EXCHANGER_PAYMENT = 'WAITING_FOR_EXCHANGER_PAYMENT', _('در انتظار پرداخت صراف')
    REJECTED_BY_EXCHANGER = 'REJECTED_BY_EXCHANGER', _('رد شده توسط صراف')
    REJECTED_BY_EXPORTER = 'REJECTED_BY_EXPORTER', _('رد شده توسط صادرکننده')
    DOING_BY_EXCHANGER = 'DOING_BY_EXCHANGER', _('در حال انجام توسط صراف')
    DOING_BY_EXPORTER = 'DOING_BY_EXPORTER', _('در حال انجام توسط صادرکننده')
    WAITING_FOR_IMPORTER_CONFIRMATION = 'WAITING_FOR_IMPORTER_CONFIRMATION', _('در انتظار تایید واردکننده')
    WAITING_FOR_EXCHANGER_CONFIRMATION = 'WAITING_FOR_EXCHANGER_CONFIRMATION', _('در انتظار تایید صراف')
    WAITING_FOR_PARENT = 'WAITING_FOR_PARENT', _('در انتظار پایان معامله وارد کننده و صراف')
    CONFIRMED_BY_EXCHANGER = 'CONFIRMED_BY_EXCHANGER', _('تایید شده توسط صراف')
    DENIED_BY_EXCHANGER = 'DENIED_BY_EXCHANGER', _('رد شده توسط صراف')
    CONFIRMED_BY_IMPORTER = 'CONFIRMED_BY_IMPORTER', _('تایید شده توسط واردکننده')
    CLAIMED_BY_IMPORTER = 'CLAIMED_BY_IMPORTER', _('رد شده توسط واردکننده، در انتظار داوری')
    JUDGED = 'JUDGED', _('داوری شده است')


class JudgeVote(models.TextChoices):
    NOT_CLAIMED = "NOT_CLAIMED", _('هنوز درخواست داوری نشده است')
    NOT_JUDGED = "NOT_JUDGED", _('هنوز داوری نشده است')
    DONE = "DONE", _('قرارداد انجام شده است')
    NOT_DONE = "NOT_DONE", _('قرارداد انجام نشده است')
    SEMI_DONE = "SEMI_DONE", _('قرارداد ناقص انجام شده است')


class SettlementType(models.TextChoices):
    SINGLE = 'SINGLE', _('تک حواله ای')
    MULTI = 'MULTI', _('چند حواله ای')


class RemittanceCurrencyType(models.TextChoices):
    RIAL = 'RIAL', _('ریال')
    DOLLAR = 'DOLLAR', _('دلار')
    EURO = 'EURO', _('یورو')
    RUBLE = 'RUBLE', _('روبل')


class OperatorType(models.TextChoices):
    NORMAL_USER = 'NORMAL_USER', _('کاربر')
    ADMIN = 'ADMIN', _('سیستم')


class OwnerType(models.TextChoices):
    IMPORTER = 'IMPORTER', _('واردکننده')
    EXCHANGER = 'EXCHANGER', _('صراف')
    EXPORTER = 'EXPORTER', _('صادرکننده')
    RETURN = 'RETURN', _('RETURN')
    CLAIM = 'CLAIM', _('CLAIM')


class TransactionType(models.TextChoices):
    CHARGE = 'CHARGE', _('شاٰرژ اولیه')
    PAYMENT = 'PAYMENT', _('پرداخت')
    CLAIM = 'CLAIM', _('درخواست داوری')
    RETURN_REMAINING = 'RETURN_REMAINING', _('از حساب صراف به حساب RETURN')
    JUDGEMENT_NOT_DONE = 'JUDGEMENT_NOT_DONE', _('از حساب CLAIM به حساب RETURN')
    JUDGEMENT_DONE = 'JUDGEMENT_DONE', _('از حساب CLAIM به حساب صادرکننده')


def init_from_json(self, args, kwargs):
    for dictionary in args:
        for key in dictionary:
            setattr(self, key, dictionary[key])
    for key in kwargs:
        setattr(self, key, kwargs[key])


# Create your models here.


class AuthProfileManager(BaseUserManager):

    def create_user(self, username, role, password=None):
        if not username:
            raise ValueError('User must have an username address')

        user = self.model(username=username)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AuthProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    objects = AuthProfileManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Owner(models.Model):
    bank_account_id = models.CharField(max_length=255, primary_key=True)
    owner_type = models.CharField(max_length=255, choices=OwnerType.choices, default=OwnerType.IMPORTER)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)

    def owner_type_verbose(self):
        return OwnerType(self.owner_type).label

    def __str__(self):
        return str(self.bank_account_id)


class UserProfile(models.Model):
    national_code = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)

    def __repr__(self):
        return self.national_code

    class Meta:
        pass


class JudgeProfile(models.Model):
    national_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)

    def __repr__(self):
        return self.national_id

    def __str__(self):
        return self.national_id


class ReporterProfile(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    full_name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)


class Contract(models.Model):
    id = models.IntegerField(primary_key=True)
    dst_owner_bank_account_id = models.CharField(max_length=255)

    value_in_rial = models.IntegerField()
    remittance_value = models.IntegerField()
    judge_vote = models.CharField(max_length=255, choices=JudgeVote.choices, default=JudgeVote.NOT_CLAIMED)
    expire_date = models.BigIntegerField()
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, choices=ContractStatus.choices)

    def judge_vote_verbose(self):
        return JudgeVote(self.judge_vote).label

    def status_verbose(self):
        return ContractStatus(self.status).label

    def expire_date_verbose(self):
        return str(jdatetime.datetime.fromtimestamp(self.expire_date).strftime("%Y/%m/%d"))

    class Meta:
        abstract = True


class NormalContract(Contract):
    src_owner_bank_account_id = models.CharField(max_length=255)

    remittance_currency = models.CharField(max_length=255, choices=RemittanceCurrencyType.choices, default=RemittanceCurrencyType.DOLLAR)
    settlement_type = models.CharField(max_length=255, choices=SettlementType.choices, default=SettlementType.SINGLE)
    judge_national_id = models.CharField(max_length=255)
    judge_name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)

    def settlement_type_verbose(self):
        return SettlementType(self.settlement_type).label


class Subcontract(Contract):
    parent_id = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=255, choices=TransactionType.choices, default='')
    relevant_contract_id = models.IntegerField()
    src_owner_bank_account_id = models.CharField(max_length=255)
    src_owner_type = models.CharField(max_length=255, choices=OwnerType.choices, default='')
    dst_owner_bank_account_id = models.CharField(max_length=255)
    dst_owner_type = models.CharField(max_length=255, choices=OwnerType.choices, default='')
    amount = models.IntegerField()
    operator_type = models.CharField(max_length=255, choices=OperatorType.choices, default=OperatorType.NORMAL_USER)
    operator_id = models.CharField(max_length=255)
    # date = models.CharField(max_length=255)
    date = models.BigIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_from_json(self, args, kwargs)

    def transaction_type_verbose(self):
        return TransactionType(self.transaction_type).label

    def src_owner_type_verbose(self):
        return OwnerType(self.src_owner_type).label

    def dst_owner_type_verbose(self):
        return OwnerType(self.dst_owner_type).label

    def operator_type_verbose(self):
        return OperatorType(self.operator_type).label

    def date_verbose(self):
        # return str(jdatetime.datetime.fromtimestamp(1602163718283 / 1000).strftime("%Y/%m/%d-%H:%M:%S"))
        return str(jdatetime.datetime.fromtimestamp(self.date / 1000).strftime("%Y/%m/%d-%H:%M:%S"))
