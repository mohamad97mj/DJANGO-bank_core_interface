from .utils import *


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
