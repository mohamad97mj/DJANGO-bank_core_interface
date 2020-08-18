from .utils import *


class NewTransactionForm(ModelForm):

    def __init__(self, owner, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()
        self.fields['owner'].initial = owner
        self.fields['operator'].widget = forms.HiddenInput()
        self.fields['operator'].initial = operator

    def save(self, commit=True):
        m = super(NewTransactionForm, self).save(commit=False)
        m.transaction_type = '2'
        m.operator_type = '1'
        if commit:
            m.save()
        return m

    class Meta:
        model = Transaction
        fields = [
            'owner',
            'operator',
            'otherside_owner',
            'value']
        labels = {
            'otherside_owner': 'شماره حساب مقصد',
            'value': 'مبلغ',
        }
