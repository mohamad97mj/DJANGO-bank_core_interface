from .utils import *


class NewTransactionForm(ModelForm):

    def __init__(self, owner, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.src_owner = owner
        self.fields['src_owner_bank_account_id'].widget = forms.HiddenInput()
        self.fields['src_owner_bank_account_id'].initial = owner.bank_account_id
        self.fields['operator_national_code'].widget = forms.HiddenInput()
        self.fields['operator_national_code'].initial = operator
        self.fields['dst_owner_bank_account_id'].required = False
        if owner.owner_type == OwnerType.IMPORTER:
            self.fields['dst_owner_bank_account_id'].label = "شماره حساب صراف"
        else:
            self.fields['dst_owner_bank_account_id'].label = "شماره حساب صادرکننده"

        self.fields['value'].required = False

    def clean_dst_owner_bank_account_id(self):
        dst_owner_bank_account_id = self.cleaned_data['dst_owner_bank_account_id']
        empty_field_validator(dst_owner_bank_account_id)

        try:
            dst_owner = Owner.objects.get(pk=dst_owner_bank_account_id)
            if self.src_owner.owner_type == OwnerType.IMPORTER:
                if dst_owner.owner_type == OwnerType.EXCHANGER:
                    return dst_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            elif self.src_owner.owner_type == OwnerType.EXCHANGER:
                if dst_owner.owner_type == OwnerType.EXPORTER:
                    return dst_owner.bank_account_id
                else:
                    raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

        except Owner.DoesNotExist:
            if self.src_owner.owner_type == OwnerType.IMPORTER:
                raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")
            else:
                raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

    def clean_value(self):
        value = self.cleaned_data['value']
        empty_field_validator(value)
        return value

    def save(self, commit=True):
        m = super(NewTransactionForm, self).save(commit=False)
        m.owner_type = OwnerType.EXCHANGER
        m.operator_type = OperatorType.USER
        if commit:
            m.save()
        return m

    class Meta:
        model = Transaction
        fields = [
            'operator_national_code',
            'src_owner_bank_account_id',
            'dst_owner_bank_account_id',
            'value']
        labels = {
            'value': 'مبلغ',
        }
