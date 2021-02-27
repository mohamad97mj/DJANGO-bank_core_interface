from .utils import *
from django.contrib.auth import authenticate


class OutputReportForm(Form):
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

    def clean_from_date(self):
        from_date = self.cleaned_data['from_date']
        empty_field_validator(from_date)
        try:
            return int(jdate2timestamp(from_date))
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        empty_field_validator(to_date)
        try:
            return int(jdate2timestamp(to_date))
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")
