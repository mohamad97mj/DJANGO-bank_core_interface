from .utils import *


class NewSubcontractForm(ModelForm):
    dst_owner = forms.CharField(max_length=50, required=False, label="شماره حساب صادرکننده")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['parent'].widget = forms.HiddenInput()
        # self.fields['parent'].required = False
        self.fields['dst_owner'].required = False
        self.fields['value_in_rial'].required = False
        self.fields['remittance_value'].required = False
        self.fields['expire_date'].required = False
        self.fields['description'].required = False
        self.fields['dst_owner'].widget = forms.TextInput()
        # self.fields['judge_vote'].initial = '0'
        self.fields['expire_date'].widget.attrs['placeholder'] = "1400/11/05"

    def save(self, commit=True):
        m = super(NewSubcontractForm, self).save(commit=False)
        m.judge_vote = '0'
        m.status = '12'
        if commit:
            m.save()
        return m

    def clean_dst_owner(self):
        dst_owner_bank_account_id = self.cleaned_data['dst_owner']
        empty_field_validator(dst_owner_bank_account_id)

        try:
            dst_owner = Owner.objects.get(pk=dst_owner_bank_account_id)
            if dst_owner.owner_type == '3':
                return dst_owner
            else:
                raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

        except Owner.DoesNotExist:
            raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

    def clean_value_in_rial(self):
        value_in_rial = self.cleaned_data['value_in_rial']
        empty_field_validator(value_in_rial)
        return value_in_rial
        pass

    def clean_remittance_value(self):
        remittance_value = self.cleaned_data['remittance_value']
        empty_field_validator(remittance_value)
        return remittance_value

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        empty_field_validator(expire_date)
        try:
            return datetime.datetime.strptime(expire_date, "%Y/%m/%d").date().strftime('%Y/%m/%d')
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    class Meta:
        model = Subcontract
        fields = [
            # 'parent',
            'dst_owner',
            'value_in_rial',
            'remittance_value',
            'expire_date',
            'description',
        ]

        labels = {
            'expire_date': 'تاریخ اعتبار',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'description': 'توضیحات',
            'src_owner': 'شماره حساب صراف',
            'dst_owner': 'شماره حساب صادرکننده',
        }
        help_texts = {
            'expire_date': 'با فرمت YYYY/MM/DD',
        }
