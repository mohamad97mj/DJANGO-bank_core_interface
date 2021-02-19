from .utils import *


class NewContractForm(ModelForm):
    expire_date = forms.CharField(required=False,
                                  label="تاریخ اعتبار",
                                  widget=forms.TextInput(attrs={'placeholder': '1400/02/01'}))

    value_in_rial = forms.CharField(required=False, label="مبلغ به ریال")
    remittance_value = forms.CharField(required=False, label="مبلغ حواله")

    field_order = [
        'dst_owner_bank_account_id',
        'value_in_rial',
        'remittance_currency',
        'remittance_value',
        'settlement_type',
        'judge_national_id',
        'judge_name',
        'expire_date',
        'status',
        'description',
    ]

    def __init__(self, src_owner=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.src_owner_bank_account_id = src_owner
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['id'].initial = 0
        self.fields['src_owner_bank_account_id'].widget = forms.HiddenInput()
        self.fields['src_owner_bank_account_id'].initial = src_owner
        self.fields['dst_owner_bank_account_id'].required = False
        self.fields['remittance_currency'].required = False
        self.fields['judge_national_id'].required = False
        self.fields['judge_name'].required = False
        self.fields['judge_name'].widget.attrs['disabled'] = True
        self.fields['description'].required = False
        self.order_fields(field_order=self.field_order)

    def save(self, commit=True):
        m = super(NewContractForm, self).save(commit=False)
        m.status = ContractStatus.NONE
        if commit:
            m.save()
        return m

    def clean_dst_owner_bank_account_id(self):

        print("here4")
        dst_owner_bank_account_id = self.cleaned_data['dst_owner_bank_account_id']
        empty_field_validator(dst_owner_bank_account_id)

        # dst_owner = Owner.objects.get(pk=dst_owner_bank_account_id)
        dst_owner = get_public_owner(dst_owner_bank_account_id)
        if dst_owner and dst_owner.owner_type == OwnerType.EXCHANGER:
            return dst_owner.bank_account_id
        else:
            raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

        # except Owner.DoesNotExist:
        #     raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

    def clean_value_in_rial(self):
        value_in_rial = self.cleaned_data['value_in_rial']
        empty_field_validator(value_in_rial)
        int_value_in_rial = int(value_in_rial.replace(',', ''))
        if int_value_in_rial <= 0:
            raise forms.ValidationError("خطا: مبلغ قرار داد باید بیشتر از صفر باشد!")
        return int_value_in_rial

    def clean_remittance_currency(self):
        remittance_currency = self.cleaned_data['remittance_currency']
        empty_field_validator(remittance_currency)
        return remittance_currency

    def clean_remittance_value(self):
        remittance_value = self.cleaned_data['remittance_value']
        empty_field_validator(remittance_value)
        int_remittance_value = int(remittance_value.replace(',', ''))
        if int_remittance_value <= 0:
            raise forms.ValidationError("خطا: مبلغ حواله باید بیشتر از صفر باشد!")
        return int_remittance_value

    def clean_judge_name(self):
        judge_name = self.cleaned_data['judge_name']
        empty_field_validator(judge_name)
        return judge_name

    def clean_judge_national_id(self):
        judge_national_id = self.cleaned_data['judge_national_id']
        empty_field_validator(judge_national_id)
        # try:
        judge = get_judge(judge_national_id)
        # judge = load_judge(judge_national_id)
        if judge:
            return judge.national_id
        else:
            raise forms.ValidationError('خطا: داور با این شناسه ملی در سامانه ثبت نشده است!')

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        empty_field_validator(expire_date)
        try:
            return jdate2timestamp(expire_date)
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    def clean(self):
        pass
        return self.cleaned_data

    class Meta:
        model = NormalContract
        fields = [
            'id',
            'src_owner_bank_account_id',
            'dst_owner_bank_account_id',
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge_national_id',
            'judge_name',
            'expire_date',
            'description'
        ]
        labels = {
            'src_owner_bank_account_id': "شماره حساب واردکننده",
            'dst_owner_bank_account_id': "شماره حساب صراف",
            'remittance_currency': 'ارز حواله',
            'settlement_type': 'نوع تسویه',
            'judge_national_id': 'شناسه ملی داور',
            'judge_name': 'نام داور',
            'description': 'توضیحات',
        }
        help_texts = {
            'expire_date': 'با فرمت YYYY/MM/DD',
        }
