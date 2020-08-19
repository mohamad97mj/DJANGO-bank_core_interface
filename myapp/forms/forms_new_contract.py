from .utils import *


class NewContractForm(ModelForm):
    judge = forms.CharField(max_length=50, required=False)

    def __init__(self, src_owner,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expire_date'].widget.attrs['placeholder'] = "1400/11/05"
        self.fields['dst_owner'].required = False
        self.fields['value_in_rial'].required = False
        self.fields['remittance_currency'].required = False
        self.fields['remittance_value'].required = False
        self.fields['judge'].label = 'داور'
        self.fields['expire_date'].required = False
        self.fields['description'].required = False

    def save(self, commit=True):
        m = super(NewContractForm, self).save(commit=False)
        m.judge_vote = '0'
        m.status = '1'
        if commit:
            m.save()
        return m

    def clean_dst_owner(self):

        dst_owner_bank_account_id = self.cleaned_data['dst_owner']
        empty_field_validator(dst_owner_bank_account_id)
        src_owner = get_owner(self.src_owner)

        try:
            dst_owner = models.Owner.objects.get(pk=dst_owner_bank_account_id)
            if src_owner.owner_type == '1':
                if dst_owner.owner_type == '2':
                    return dst_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

            elif src_owner.owner_type == '2':
                if dst_owner.owner_type == '3':
                    return dst_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صادر کننده با این مشخصات در صامانه ثبت نشده است!")

        except models.Owner.DoesNotExist:
            if src_owner.owner_type == '1':
                raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            else:
                raise forms.ValidationError("خطا: صادر کننده با این مشخصات در سامانه ثبت نشده است!")

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        empty_field_validator(expire_date)
        try:
            return datetime.datetime.strptime(expire_date, "%Y/%m/%d").date().strftime('%Y/%m/%d')
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

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

    def clean_judge(self):
        judge_national_id = self.cleaned_data['judge']
        empty_field_validator(judge_national_id)
        try:
            return models.JudgeProfile.objects.get(pk=judge_national_id)
        except models.JudgeProfile.DoesNotExist:
            raise forms.ValidationError('خطا: داور با این مشخسات در سامانه ثبت نشده است!')

    class Meta:
        model = NormalContract
        fields = [
            'src_owner',
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
            'expire_date': 'تاریخ اعتبار',
            'judge': 'شناسه ملی داور',
            'description': 'توضیحات',
        }
        help_texts = {
            'expire_date': 'با فرمت YYYY/MM/DD',
        }
