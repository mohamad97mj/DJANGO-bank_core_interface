from .utils import *


class SubcontractDetailForm(ModelForm):
    field_order = [
        'id',
        'src_owner_bank_account_id',
        'dst_owner_bank_account_id',
        'value_in_rial',
        'remittance_currency',
        'remittance_value',
        'judge_national_id',
        'judge_name',
        'judge_vote',
        'expire_date',
        'status',
        'description'
    ]

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.fields['id'] = forms.IntegerField(disabled=True, label="شناسه", initial=self.instance.id)
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['expire_date'] = forms.CharField(max_length=255,
                                                     label="تاریخ اعتبار",
                                                     disabled=True,
                                                     initial=self.instance.expire_date_verbose)
        self.order_fields(field_order=self.field_order)

    def __add_judge_information_fields(self):
        self.fields['judge_national_id'] = forms.CharField(max_length=255,
                                                           label="شناسه ملی داور",
                                                           disabled=True,
                                                           initial=self.parent.judge_national_id)

        self.fields['judge_name'] = forms.CharField(max_length=255,
                                                    label="نام داور",
                                                    disabled=True,
                                                    initial=self.parent.judge_name)

        self.order_fields(self.field_order)

    def __add_remittance_currency_field(self):
        self.fields['remittance_currency'] = forms.CharField(max_length=255,
                                                             label='ارز حواله',
                                                             disabled=True,
                                                             initial=self.parent.remittance_currency)
        self.order_fields(self.field_order)

    def __add_src_owner_field(self):
        self.fields['src_owner_bank_account_id'] = forms.CharField(max_length=255,
                                                                   label="شماره حساب صراف",
                                                                   disabled=True,
                                                                   initial=self.parent.dst_owner_bank_account_id)

    def __add_dst_owner_field(self):
        self.fields['dst_owner_bank_account_id'] = forms.CharField(max_length=255,
                                                                   label="شماره حساب صادرکننده",
                                                                   disabled=True,
                                                                   initial=self.instance.dst_owner_bank_account_id)

    def perform_exchanger_point_of_view(self):
        self.__add_dst_owner_field()
        self.order_fields(self.field_order)

    def perform_exporter_point_of_view(self):
        self.__add_src_owner_field()
        self.__add_judge_information_fields()
        self.__add_remittance_currency_field()
        self.order_fields(self.field_order)

    def perform_judge_point_of_view(self):
        self.__add_remittance_currency_field()
        self.__add_src_owner_field()
        self.__add_dst_owner_field()
        self.order_fields(self.field_order)

    class Meta:
        model = Subcontract
        fields = [
            'value_in_rial',
            'remittance_value',
            'judge_vote',
            'description',
            'status',
        ]

        labels = {
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'judge_vote': 'رای داور',
            'description': 'توضیحات',
            'status': 'وضعیت',
        }
