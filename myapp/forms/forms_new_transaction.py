from .utils import *


class NewTransactionForm(ModelForm):

    def __init__(self, owner, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.fields['owner'].widget = forms.HiddenInput()
        self.fields['owner'].initial = owner
        self.fields['operator'].widget = forms.HiddenInput()
        self.fields['operator'].initial = operator
        self.fields['otherside_owner'].required = False
        self.fields['value'].required = False

    def clean_otherside_owner(self):
        otherside_owner_bank_account_id = self.cleaned_data['otherside_owner']
        empty_field_validator(otherside_owner_bank_account_id)
        owner = get_owner(self.owner)

        try:
            otherside_owner = models.Owner.objects.get(pk=otherside_owner_bank_account_id)
            if owner.owner_type == '1':
                if otherside_owner.owner_type == '2':
                    return otherside_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            elif owner.owner_type == '2':
                if otherside_owner.owner_type == '3':
                    return otherside_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صادر کننده با این مشخصات در صامانه ثبت نشده است!")

        except models.Owner.DoesNotExist:
            if owner.owner_type == '1':
                raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            else:
                raise forms.ValidationError("خطا: صادر کننده با این مشخصات در سامانه ثبت نشده است!")

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
