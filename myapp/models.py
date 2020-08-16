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
    ('0', 'هنوز داوری نشده'),
    ('1', 'معامله انجام شده است'),
    ('2', 'معامله انجام نشده است')
)

OWNER_TYPE = (
    ('1', 'صراف'),
    ('2', 'وارد کننده'),
    ('3', 'صادر کننده'),
)

CONTRACT_STATUS = (
    ('1', 'در انتظار تایید طرف دیگر قرارداد'),
    ('2', 'در انتظار داوری'),
    ('3', 'داوری شده است'),
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
    src_owner = models.IntegerField()
    dst_owner = models.IntegerField()
    value_in_rial = models.IntegerField()
    remittance_currency = models.CharField(max_length=40)
    remittance_value = models.IntegerField()
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_TYPE, default='1')
    judge = models.ForeignKey(JudgeProfile, on_delete=models.SET_NULL, null=True)
    judge_vote = models.CharField(max_length=50, choices=JUDGE_VOTE)
    expire_date = models.DateField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS)

    def settlement_type_verbose(self):
        return dict(SETTLEMENT_TYPE)[self.settlement_type]

    def judge_vote_verbose(self):
        return dict(JUDGE_VOTE)[self.judge_vote]

    def status_verbose(self):
        return dict(CONTRACT_STATUS)[self.status]


class Subcontract(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(Contract, on_delete=models.CASCADE)
    dst_owner = models.IntegerField()
    value_in_rial = models.IntegerField()
    remittance_value = models.IntegerField()
    judge_vote = models.CharField(max_length=50, choices=JUDGE_VOTE)
    expire_date = models.DateField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS)

    def judge_vote_verbose(self):
        return dict(JUDGE_VOTE)[self.judge_vote]

    def status_verbose(self):
        return dict(CONTRACT_STATUS)[self.status]


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    otherside_owner = models.IntegerField()
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE, default='1')
    value = models.IntegerField()
    operator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    operator_type = models.CharField(max_length=50, choices=OPERATOR_TYPE, default='1')

    def transaction_type_verbose(self):
        return dict(TRANSACTION_TYPE)[self.transaction_type]

    def operator_type_verbose(self):
        return dict(OPERATOR_TYPE)[self.operator_type]
