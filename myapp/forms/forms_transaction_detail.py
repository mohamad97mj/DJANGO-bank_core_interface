from .utils import *


class TransactionDetailForm(ModelForm):
    myid = forms.IntegerField()
    transaction_type = forms.CharField(label='نوع تراکنش', widget=forms.Select(choices=TRANSACTION_TYPE), disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dst_owner_bank_account_id'].widget.attrs['disabled'] = True
        self.fields['value'].widget.attrs['disabled'] = True
        self.fields['operator_type'].widget.attrs['disabled'] = True
        self.fields['operator_national_code'].widget.attrs['disabled'] = True
        self.fields['myid'].widget.attrs['disabled'] = True
        self.fields['myid'].initial = self.instance.id
        self.fields['myid'].label = 'شناسه'

    class Meta:
        model = Transaction
        fields = ['myid', 'transaction_type', 'dst_owner_bank_account_id', 'value', 'operator_type',
                  'operator_national_code']
        labels = {
            'dst_owner_bank_account_id': 'حساب طرف دیگر تراکنش',
            'value': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator_national_code': 'کد ملی اپراتور',
        }
