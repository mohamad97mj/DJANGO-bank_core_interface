from .utils import *


class TransactionDetailForm(ModelForm):
    myid = forms.IntegerField()
    transaction_type = forms.CharField(label='نوع تراکنش', widget=forms.Select(choices=TRANSACTION_TYPE), disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dst_owner_bank_account_id'].widget.attrs['disabled'] = True
        self.fields['amount'].widget.attrs['disabled'] = True
        self.fields['operator_type'].widget.attrs['disabled'] = True
        self.fields['operator_id'].widget.attrs['disabled'] = True
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['id'].initial = self.instance.id
        self.fields['id'].label = 'شناسه'

    class Meta:
        model = Transaction
        fields = [
            'myid',
            'transaction_type',
            'dst_owner_bank_account_id',
            'amount', 'operator_type',
            'operator_id',
        ]

        labels = {
            'dst_owner_bank_account_id': 'حساب طرف دیگر تراکنش',
            'amount': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator_id': 'کد ملی اپراتور',
        }
