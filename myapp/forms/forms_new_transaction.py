from .utils import *


class NewTransactionForm(ModelForm):
    otherside_owner = forms.CharField(max_length=50, required=False)

    def __init__(self, owner, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.fields['owner'].widget = forms.HiddenInput()
        self.fields['owner'].initial = owner
        self.fields['operator'].widget = forms.HiddenInput()
        self.fields['operator'].initial = operator
        self.fields['otherside_owner'].required = False
        if owner.owner_type == '1':
            self.fields['otherside_owner'].label = "شماره حساب صراف"
        else:
            self.fields['otherside_owner'].label = "شماره حساب صادرکننده"

        self.fields['value'].required = False

    def clean_otherside_owner(self):
        otherside_owner_bank_account_id = self.cleaned_data['otherside_owner']
        empty_field_validator(otherside_owner_bank_account_id)

        try:
            otherside_owner = Owner.objects.get(pk=otherside_owner_bank_account_id)
            if self.owner.owner_type == '1':
                if otherside_owner.owner_type == '2':
                    return otherside_owner
                else:
                    raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            elif self.owner.owner_type == '2':
                if otherside_owner.owner_type == '3':
                    return otherside_owner
                else:
                    raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

        except Owner.DoesNotExist:
            if self.owner.owner_type == '1':
                raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            else:
                raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

    def clean_value(self):
        value = self.cleaned_data['value']
        empty_field_validator(value)
        return value

    def save(self, commit=True):
        m = super(NewTransactionForm, self).save(commit=False)
        m.owner_type = '2'
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
