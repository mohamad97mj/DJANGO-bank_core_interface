from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import datetime

import uuid

SETTLEMENT_TYPE = (
    ('1', 'تک حواله ای'),
    ('2', 'چند حواله ای'),
)

OPERATOR_TYPE = (
    ('1', 'کاربر'),
    ('2', 'سیستم')
)

JUDGE_VOTE = (
    ('0', 'هنوز داوری نشده'),
    ('1', 'معامله انجام شده است'),
    ('2', 'معامله انجام نشده است')
)

OWNER_TYPE = (
    ('1', 'وارد کننده'),
    ('2', 'صراف'),
    ('3', 'صادرکننده'),
)

CONTRACT_STATUS = (
    ('11', 'در انتظار تایید صراف'),
    ('12', 'در انتظار تایید صادرکننده'),
    ('21', 'تایید شده و در حال انجام توسط صراف'),
    ('22', 'تایید شده و درحال انجام توسط صادرکننده'),
    ('23', 'رد شده توسط صراف'),
    ('24', 'رد شده توسط صادرکننده'),
    ('31', 'پایان معامله توسط صراف، در انتظار داوری'),
    ('32', 'پایان معامله توسط صادر کننده، در انتظار داوری'),
    ('4', 'داوری شده است'),
)


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
    owner_type = models.CharField(max_length=50, choices=OWNER_TYPE, default='1')

    def owner_type_verbose(self):
        return dict(OWNER_TYPE)[self.owner_type]

    def __str__(self):
        return str(self.bank_account_id)


class UserProfile(models.Model):
    national_code = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    owners = models.ManyToManyField(Owner)

    def __str__(self):
        return self.national_code


class JudgeProfile(models.Model):
    national_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.national_id


class Contract(models.Model):
    dst_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True
                                  , related_name="%(app_label)s_%(class)s_dst_owner"
                                  , related_query_name="%(app_label)s_%(class)ss")

    value_in_rial = models.IntegerField()
    remittance_value = models.IntegerField()
    judge_vote = models.CharField(max_length=50, choices=JUDGE_VOTE)
    expire_date = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS)

    def judge_vote_verbose(self):
        return dict(JUDGE_VOTE)[self.judge_vote]

    def status_verbose(self):
        return dict(CONTRACT_STATUS)[self.status]

    class Meta:
        abstract = True


#     just for git


class NormalContract(Contract):
    src_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True
                                  , related_name="%(app_label)s_%(class)s_src_owner"
                                  , related_query_name="%(app_label)s_%(class)ss")

    remittance_currency = models.CharField(max_length=40)
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_TYPE, default='1')
    judge = models.ForeignKey(JudgeProfile, on_delete=models.SET_NULL, null=True)

    def settlement_type_verbose(self):
        return dict(SETTLEMENT_TYPE)[self.settlement_type]


class Subcontract(Contract):
    parent = models.ForeignKey(NormalContract, on_delete=models.CASCADE)


class Transaction(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="owner")
    otherside_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="otherside_owner")
    value = models.IntegerField()
    operator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    operator_type = models.CharField(max_length=50, choices=OPERATOR_TYPE, default='1')
    datetime = models.CharField(max_length=50)

    def operator_type_verbose(self):
        return dict(OPERATOR_TYPE)[self.operator_type]
