from .utils import *
from django.contrib.auth import authenticate


class ContradictionReportForm(Form):
    owner_type = forms.CharField(max_length=255, label='حساب عملیاتی مورد نظر',
                                 widget=forms.Select(choices=REPORT_OWNER_TYPE),
                                 help_text="حسابی که قصد گزارش گیری از آن را دارید",
                                 required=False)
    from_date = forms.CharField(max_length=255,
                                label="ابتدای بازه گزارش گیری",
                                widget=forms.TextInput(attrs={'placeholder': '1400/05/11'}),
                                required=False,
                                help_text="با فرمت YYYY/MM/DD")
    to_date = forms.CharField(max_length=255,
                              label="انتهای بازی گزارش گیری",
                              widget=forms.TextInput(attrs={'placeholder': '1400/06/11'}),
                              required=False,
                              help_text="با فرمت YYYY/MM/DD")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        owner_type = cleaned_data['owner_type']
        owner = get_operational_owner(owner_type)
        if owner:
            pass
        else:
            self.add_error("owner_type", "خطا: شماره حساب با این مشخصات در سامانه ثبت نشده است!")

    def clean_from_date(self):
        from_date = self.cleaned_data['from_date']
        empty_field_validator(from_date)
        try:
            return int(jdate2timestamp(from_date))*1000
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        empty_field_validator(to_date)
        try:
            return int(jdate2timestamp(to_date))*1000
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")
