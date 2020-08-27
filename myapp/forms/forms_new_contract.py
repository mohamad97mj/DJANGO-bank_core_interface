from .utils import *


class NewContractForm(ModelForm):

    def __init__(self, src_owner=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.src_owner_bank_account_id = src_owner
        self.fields['src_owner_bank_account_id'].widget = forms.HiddenInput()
        self.fields['src_owner_bank_account_id'].initial = src_owner
        self.fields['dst_owner_bank_account_id'].required = False
        self.fields['value_in_rial'].required = False
        self.fields['remittance_currency'].required = False
        self.fields['remittance_value'].required = False
        self.fields['judge_name'].required = False
        self.fields['judge_national_id'].required = False
        self.fields['expire_date'].widget.attrs['placeholder'] = "1400/05/11"
        self.fields['expire_date'].required = False
        self.fields['description'].required = False

    def save(self, commit=True):
        m = super(NewContractForm, self).save(commit=False)
        # m.judge_vote = JudgeVote.NOT_JUDGED
        # m.status = ContractStatus.WAITING_FOR_EXCHANGER
        if commit:
            m.save()
        return m

    def clean_dst_owner_bank_account_id(self):

        dst_owner_bank_account_id = self.cleaned_data['dst_owner_bank_account_id']
        empty_field_validator(dst_owner_bank_account_id)

        # try:
        # dst_owner = Owner.objects.get(pk=dst_owner_bank_account_id)
        dst_owner = get_owner(dst_owner_bank_account_id)
        if dst_owner and dst_owner.owner_type == OwnerType.EXCHANGER:
            return dst_owner.bank_account_id
        else:
            raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

        # except Owner.DoesNotExist:
        #     raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

    def clean_value_in_rial(self):
        value_in_rial = self.cleaned_data['value_in_rial']
        empty_field_validator(value_in_rial)
        return value_in_rial

    def clean_remittance_currency(self):
        remittance_currency = self.cleaned_data['remittance_currency']
        empty_field_validator(remittance_currency)
        return remittance_currency

    def clean_remittance_value(self):
        remittance_value = self.cleaned_data['remittance_value']
        empty_field_validator(remittance_value)
        return remittance_value

    def clean_judge_name(self):
        judge_name = self.cleaned_data['judge_name']
        empty_field_validator(judge_name)

    def clean_judge_national_id(self):
        judge_national_id = self.cleaned_data['judge_national_id']
        empty_field_validator(judge_national_id)
        # try:
        # judge = get
        #     return JudgeProfile.objects.get(pk=judge_national_id)
        # except JudgeProfile.DoesNotExist:
        #     raise forms.ValidationError('خطا: داور با این مشخصات در سامانه ثبت نشده است!')

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        empty_field_validator(expire_date)
        try:
            return datetime.datetime.strptime(expire_date, "%Y/%m/%d").date().strftime('%Y/%m/%d')
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    class Meta:
        model = NormalContract
        fields = [
            'src_owner_bank_account_id',
            'dst_owner_bank_account_id',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge_name',
            'judge_national_id',
            'expire_date',
            'description'
        ]
        labels = {
            'src_owner_bank_account_id': "شماره حساب وارد کننده",
            'dst_owner_bank_account_id': "شماره حساب صراف",
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'settlement_type': 'نوع تسویه',
            'judge_name': 'نام داور',
            'judge_national_id': 'شناسه ملی داور',
            'expire_date': 'تاریخ اعتبار',
            'description': 'توضیحات',
        }
        help_texts = {
            'expire_date': 'با فرمت YYYY/MM/DD',
        }
