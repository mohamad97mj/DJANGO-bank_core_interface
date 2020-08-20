from .utils import *


class ContractDetailForm(ModelForm):
    myid = forms.IntegerField()
    dst_owner = forms.CharField(max_length=50, required=False, label="شماره حساب صراف")
    judge = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['src_owner'].widget.attrs['disabled'] = True
        self.fields['dst_owner'].widget.attrs['disabled'] = True
        self.fields['src_owner'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['settlement_type'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge'].widget.attrs['disabled'] = True
        self.fields['judge'].label = "شناسه ملی داور"
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['myid'].widget.attrs['disabled'] = True
        self.fields['myid'].initial = self.instance.id
        self.fields['myid'].label = 'شناسه'
        # self.fields['expire_date'].initial = self.instance.expire_date.

    class Meta:
        model = NormalContract
        fields = [
            'myid',
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

            'src_owner': 'شماره حساب واردکننده',
            'dst_owner': 'شماره حساب صراف',
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
