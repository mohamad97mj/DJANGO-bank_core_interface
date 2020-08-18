from .utils import *


class TransactionDetailForm(ModelForm):
    myid = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].widget.attrs['disabled'] = True
        self.fields['otherside_owner'].widget.attrs['disabled'] = True
        self.fields['value'].widget.attrs['disabled'] = True
        self.fields['operator_type'].widget.attrs['disabled'] = True
        self.fields['operator'].widget.attrs['disabled'] = True
        self.fields['myid'].widget.attrs['disabled'] = True
        self.fields['myid'].initial = self.instance.id
        self.fields['myid'].label = 'شناسه'

    class Meta:
        model = Transaction
        fields = ['myid', 'transaction_type', 'otherside_owner', 'value', 'operator_type', 'operator']
        labels = {
            'transaction_type': 'نوع تراکنش',
            'otherside_owner': 'حساب طرف دیگر تراکنش',
            'value': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator': 'کد ملی اپراتور',
        }
