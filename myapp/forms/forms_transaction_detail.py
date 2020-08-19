from .utils import *


class TransactionDetailForm(ModelForm):
    myid = forms.IntegerField()
    transaction_type = forms.CharField(label='نوع تراکنش', widget=forms.Select(choices=TRANSACTION_TYPE), disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            'otherside_owner': 'حساب طرف دیگر تراکنش',
            'value': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator': 'کد ملی اپراتور',
        }
