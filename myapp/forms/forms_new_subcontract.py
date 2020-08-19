from .utils import *


class NewSubcontractForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dst_owner'].required = False
        self.fields['value_in_rial'].required = False
        self.fields['remittance_value'].required = False
        self.fields['expire_date'].required = False
        self.fields['description'].required = False

    class Meta:
        model = Subcontract
        fields = [
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
            'dst_owner': 'شماره حساب صادر کننده',
        }
