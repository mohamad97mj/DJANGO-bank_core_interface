from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
import datetime
import uuid
from enum import Enum


class ContractAction(Enum):
    CONFIRM = "confirm"
    REJECT = "reject"
    END = 'end'
    CLAIM = 'claim'


class ContractStatus(models.TextChoices):
    WAITING_FOR_EXCHANGER = 'WAITING_FOR_EXCHANGER', _('در انتظار تایید صراف')
    WAITING_FOR_EXPORTER = 'WAITING_FOR_EXPORTER', _('در انتظار تایید صادرکننده')
    CONFIRMED_BY_EXCHANGER = 'CONFIRMED_BY_EXCHANGER', _('تایید شده و در حال انجام توسط صراف')
    CONFIRMED_BY_EXPORTER = 'CONFIRMED_BY_EXPORTER', _('تایید شده و درحال انجام توسط صادرکننده')
    DENIED_BY_EXCHANGER = 'DENIED_BY_EXCHANGER', _('رد شده توسط صراف')
    DENIED_BY_EXPORTER = 'DENIED_BY_EXPORTER', _('رد شده توسط صادرکننده')
    PAYED_BY_IMPORTER = 'PAYED_BY_IMPORTER', _('پرداخت معامله توسط وارد کننده، در انتظار تایید واردکننده')
    PAYED_BY_EXCHANGER = 'PAYED_BY_EXCHANGER', _('پرداخت معامله توسط صراف')
    ENDED_BY_EXCHANGER = 'ENDED_BY_EXCHANGER', _('پایان معامله توسط صراف، در انتظار تایید واردکننده')
    ENDED_BY_EXPORTER = 'ENDED_BY_EXPORTER', _('پایان معامله توسط صادرکننده')
    ENDED_BY_IMPORTER = 'CONFIRMED_BY_IMPORTER', _('تایید شده توسط واردکننده')
    CLAIMED_BY_IMPORTER = 'CLAIMED_BY_IMPORTER', _('رد شده توسط واردکننده، در انتظار داوری')
    JUDGED = 'JUDGED', _('داوری شده است')


class JudgeVote(models.TextChoices):
    NOT_JUDGED = "NOT_JUDGED", _('هنوز داوری نشده است')
    DONE = "DONE", _('معامله انجام شده است')
    NOT_DONE = "NOT_DONE", _('معامله انجام نشده است')
    SEMI_DONE = "SEMI_DONE", _('معامله ناقص انجام شده است')


class SettlementType(models.TextChoices):
    SINGLE = 'SINGLE', _('تک حواله ای')
    MULTI = 'MULTI', _('چند حواله ای')


class OperatorType(models.TextChoices):
    USER = 'USER', _('کاربر')
    ADMIN = 'ADMIN', _('سیستم')


class OwnerType(models.TextChoices):
    IMPORTER = 'IMPORTER', _('واردکننده')
    EXCHANGER = 'EXCHANGER', _('صراف')
    EXPORTER = 'EXPORTER', _('صادرکننده')


# Create your models here.


class AuthProfileManager(BaseUserManager):

    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email, full_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AuthProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    # should be changed by national code

    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # is this field required ?

    is_staff = models.BooleanField(default=False)

    objects = AuthProfileManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    # Email is required by default because it is USERNAME_FIELD

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.email


class Owner(models.Model):
    bank_account_id = models.IntegerField(primary_key=True)
    owner_type = models.CharField(max_length=50, choices=OwnerType.choices, default=OwnerType.IMPORTER)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def owner_type_verbose(self):
        return OwnerType(self.owner_type).label

    def __str__(self):
        return str(self.bank_account_id)

    class Meta:
        # managed = False
        pass


class UserProfile(models.Model):
    national_code = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    # owners = models.ManyToManyField(Owner)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return self.national_code

    class Meta:
        # managed = False
        pass


class JudgeProfile(models.Model):
    national_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return self.national_id

    class Meta:
        # managed = False
        pass


class Contract(models.Model):
    # dst_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True
    #                               , related_name="%(app_label)s_%(class)s_dst_owner"
    #                               , related_query_name="%(app_label)s_%(class)ss")
    id = models.IntegerField(primary_key=True)
    dst_owner_bank_account_id = models.IntegerField()

    value_in_rial = models.IntegerField()
    remittance_value = models.IntegerField()
    judge_vote = models.CharField(max_length=50, choices=JudgeVote.choices)
    expire_date = models.BigIntegerField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=ContractStatus.choices)

    def judge_vote_verbose(self):
        return JudgeVote(self.judge_vote).label

    def status_verbose(self):
        return ContractStatus(self.status).label

    class Meta:
        abstract = True
        # managed = False


#     just for git


class NormalContract(Contract):
    # src_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True
    #                               , related_name="%(app_label)s_%(class)s_src_owner"
    #                               , related_query_name="%(app_label)s_%(class)ss")
    src_owner_bank_account_id = models.IntegerField()

    remittance_currency = models.CharField(max_length=40)
    settlement_type = models.CharField(max_length=50, choices=SettlementType.choices, default=SettlementType.SINGLE)
    # judge = models.ForeignKey(JudgeProfile, on_delete=models.SET_NULL, null=True)
    judge_national_id = models.IntegerField()
    judge_name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def settlement_type_verbose(self):
        return SettlementType(self.settlement_type).label

    class Meta:
        # managed = False
        pass


class Subcontract(Contract):
    # parent = models.ForeignKey(NormalContract, on_delete=models.CASCADE)
    parent_id = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    class Meta:
        # managed = False
        pass


class Transaction(models.Model):
    # owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="owner")
    src_owner_bank_account_id = models.IntegerField()
    # otherside_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="otherside_owner")
    dst_owner_bank_account_id = models.IntegerField()
    value = models.IntegerField()
    # operator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    operator_national_code = models.IntegerField()
    operator_type = models.CharField(max_length=50, choices=OperatorType.choices, default=OperatorType.USER)
    datetime = models.CharField(max_length=50)

    def operator_type_verbose(self):
        return OperatorType(self.operator_type).label

    class Meta:
        # managed = False
        pass
