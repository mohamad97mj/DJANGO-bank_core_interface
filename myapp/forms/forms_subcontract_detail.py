from .utils import *


class SubcontractDetailForm(ModelForm):
    judge = forms.CharField(max_length=50)
    remittance_currency = forms.CharField(max_length=40)
    src_owner = forms.IntegerField()
    dst_owner = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
