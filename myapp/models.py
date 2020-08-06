from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

SETTLEMENT_TYPE = (
    ('1', 'تک حواله ای'),
    ('2', 'چند حواله ای'),
)

TRANSACTION_TYPE = (
    ('1', 'واریزی'),
    ('2', 'پرداختی')
)

OPERATOR_TYPE = (
    ('1', 'کاربر'),
    ('2', 'سیستم')
)

JUDGE_VOTE = (
    ('1', 'معامله انجام شده است'),
    ('2', 'معامله انجام نشده است')
)

OWNER_TYPE = (
    ('1', 'صراف'),
    ('2', 'وارد کننده'),
    ('3', 'صادر کننده'),
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
    bank_account_id = models.CharField(max_length=50, primary_key=True)
    owner_type = models.CharField(max_length=50, choices=OWNER_TYPE, default='1')

    def owner_type_verbose(self):
        return dict(OWNER_TYPE)[self.owner_type]


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
    id = models.IntegerField(primary_key=True)
    expire_date = models.DateField()
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_TYPE, default='1')
    value_in_rial = models.IntegerField()
    remittance_currency = models.CharField(max_length=40)
    remittance_value = models.IntegerField()
    judge = models.ForeignKey(JudgeProfile, on_delete=models.SET_NULL, null=True)
    src_owner = models.CharField(max_length=50)
    dst_owner = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    judge_vote = models.CharField(max_length=50, choices=JUDGE_VOTE)

    def settlement_type_verbose(self):
        return dict(SETTLEMENT_TYPE)[self.settlement_type]

    def judge_vote_verbose(self):
        return dict(JUDGE_VOTE)[self.judge_vote]


class Subcontract(models.Model):
    id = models.IntegerField(primary_key=True)
    expire_date = models.DateField()
    value_in_rial = models.IntegerField()
    remittance_value = models.IntegerField()
    status = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    dst_owner = models.CharField(max_length=50)
    parent = models.ForeignKey(Contract, on_delete=models.CASCADE)
    judge_vote = models.CharField(max_length=50, choices=JUDGE_VOTE)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE, default='1')
    owner = models.CharField(max_length=50)
    otherside_owner = models.CharField(max_length=50)
    value = models.IntegerField()
    operator_type = models.CharField(max_length=50, choices=OPERATOR_TYPE, default='1')
    operator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def transaction_type_verbose(self):
        return dict(TRANSACTION_TYPE)[self.transaction_type]

    def operator_type_verbose(self):
        return dict(OPERATOR_TYPE)[self.operator_type]
