from django import forms
from django.forms import ModelForm, TextInput, Form
from .models import AuthProfile, UserProfile, JudgeProfile, Transaction, Contract, Subcontract
from django.utils.translation import gettext_lazy as _

LOGIN_ROLES = [
    ('user', 'کاربر حساب'),
    ('judge', 'داور'),
]


class LoginForm(Form):
    role = forms.CharField(label='ورود به سامانه به عنوان', widget=forms.Select(choices=LOGIN_ROLES),
                           help_text="")
    username = forms.CharField(max_length=255, label="نام کاربری*", required=False,
                               help_text="به صورت پیش فرض همان کد ملی شماست")
    password = forms.CharField(max_length=32, label="گذرواژه*", widget=forms.PasswordInput, required=False,
                               help_text="")

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if username != "mohamad":
    #         raise forms.ValidationError("خطا: این کاربر وجود ندارد!")
    #     else:
    #         return username


class UserProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_code'].widget.attrs['disabled'] = True
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True

    class Meta:
        model = UserProfile
        fields = ['national_code', 'first_name', 'last_name']
        labels = {
            'national_code': 'کد ملی',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }


class JudgeProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_id'].widget.attrs['disabled'] = True
        self.fields['name'].widget.attrs['disabled'] = True

    class Meta:
        model = JudgeProfile
        fields = ['national_id', 'name']
        labels = {
            'national_id': 'شناسه ملی',
            'name': 'نام',
        }


class ContractDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['src_owner'].widget.attrs['disabled'] = True
        self.fields['dst_owner'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['settlement_type'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True

    class Meta:
        model = Contract
        fields = [
            'id',
            'src_owner',
            'dst_owner',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge',
            'judge_vote',
            'expire_date',
            'status',
            'description',
        ]
        labels = {
            'id': 'شناسه',
            'src_owner': 'شماره حساب مبداء',
            'dst_owner': 'شماره حساب مقصد',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'settlement_type': 'نوع تسویه',
            'judge': 'شناسه ملی داور',
            'judge_vote': 'رای داور',
            'expire_date': 'تاریخ اعتبار',
            'status': 'وضعیت',
            'description': 'توضیحات',
        }


class NewContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = [
            'dst_owner',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge',
            'expire_date',
            'description'
        ]
        labels = {
            'dst_owner': 'شماره حساب مقصد',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'settlement_type': 'نوع تسویه',
            'judge': 'شناسه ملی داور',
            'expire_date': 'تاریخ اعتبار',
            'description': 'توضیحات',
        }


class SubcontractDetailForm(ModelForm):
    judge = forms.CharField(max_length=50)
    remittance_currency = forms.CharField(max_length=40)
    src_owner = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['dst_owner'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['judge'].widget = forms.HiddenInput()
        self.fields['remittance_currency'].widget = forms.HiddenInput()
        self.fields['src_owner'].widget = forms.HiddenInput()

    # this method is called just for exporter point of view

    def add_judge_field(self):
        self.fields['judge'].widget = forms.TextInput()
        self.fields['judge'].label = 'شناسه ملی داور'
        self.fields['judge'].widget.attrs['disabled'] = True
        self.fields['judge'].initial = self.instance.parent.judge

    def add_remittance_currency_field(self):
        self.fields['remittance_currency'].widget = forms.TextInput()
        self.fields['remittance_currency'].label = 'ارز حواله'
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].initial = self.instance.parent.remittance_currency

    def add_exporter_fields(self):
        self.add_judge_field()
        self.add_remittance_currency_field()

    def add_judge_fields(self):
        self.add_remittance_currency_field()
        self.fields['src_owner'].widget = forms.TextInput()
        self.fields['src_owner'].widget.attrs['disabled'] = True
        self.fields['src_owner'].initial = self.instance.parent.dst_owner
        self.fields['src_owner'].label = 'حساب مبداء'
        self.fields['dst_owner'].label = 'حساب مقصد'

    class Meta:
        model = Subcontract
        fields = [
            'id',
            'src_owner',
            'dst_owner',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'judge',
            'judge_vote',
            'expire_date',
            'description',
            'status',

        ]
        labels = {
            'id': 'شناسه',
            'dst_owner': 'حساب طرف دیگر قرارداد',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'description': 'توضیحات',
            'judge_vote': 'رای داور',
            'expire_date': 'تاریخ اعتبار',
            'status': 'وضعیت',
        }


class NewSubcontractForm(ModelForm):
    class Meta:
        model = Subcontract
        fields = ['expire_date', 'value_in_rial', 'remittance_value', 'status', 'description', 'dst_owner']
        labels = {
            'expire_date': 'تاریخ اعتبار',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'status': 'وضعیت',
            'description': 'توضیحات',
            'dst_owner': 'حساب طرف دیگر قرار داد',
        }


class TransactionDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['transaction_type'].widget.attrs['disabled'] = True
        self.fields['otherside_owner'].widget.attrs['disabled'] = True
        self.fields['value'].widget.attrs['disabled'] = True
        self.fields['operator_type'].widget.attrs['disabled'] = True
        self.fields['operator'].widget.attrs['disabled'] = True

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'otherside_owner', 'value', 'operator_type', 'operator']
        labels = {
            'id': 'شناسه',
            'transaction_type': 'نوع تراکنش',
            'otherside_owner': 'حساب طرف دیگر تراکنش',
            'value': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator': 'کد ملی اپراتور',
        }


class NewTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['otherside_owner', 'value']
        labels = {
            'otherside_owner': 'شماره حساب مقصد',
            'value': 'مبلغ',
        }
