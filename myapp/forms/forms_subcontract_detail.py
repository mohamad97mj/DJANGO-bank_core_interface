from .utils import *


class SubcontractDetailForm(ModelForm):
    field_order = ['id',
                   'src_owner',
                   'dst_owner',
                   'value_in_rial',
                   'remittance_currency',
                   'remittance_value',
                   'settlement_type',
                   'judge_name',
                   'judge',
                   'judge_vote',
                   'expire_date',
                   'status',
                   'description'
                   ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'] = forms.IntegerField(disabled=True, label="شناسه", initial=self.instance.id)
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True

    # this method is called just for exporter point of view

    def hide_judge_vote(self):
        self.fields['judge_vote'].widget = forms.HiddenInput()
        # self.fields['status'].widget = forms.HiddenInput()

    # def display_judge_vote_and_status(self):
    #     self.fields['judge_vote'].widget = forms.TextInput()
    #     self.fields['status'].widget = forms.TextInput()

    def add_judge_information_fields(self):
        self.fields['judge_national_id'] = forms.CharField(max_length=50,
                                                           label="شناسه ملی داور",
                                                           disabled=True,
                                                           initial=self.instance.parent_id.judge_national_id)

        self.fields['judge_name'] = forms.CharField(max_length=100,
                                                    required=False,
                                                    label="نام داور",
                                                    disabled=True,
                                                    initial=self.instance.parent_id.judge_national_id.name)

        self.order_fields(self.field_order)

    def add_remittance_currency_field(self):
        self.fields['remittance_currency'] = forms.CharField(max_length=40,
                                                             label='ارز حواله',
                                                             disabled=True,
                                                             initial=self.instance.parent_id.remittance_currency)
        self.order_fields(self.field_order)

    def add_src_owner_field(self):
        self.fields['src_owner_bank_account_id'] = forms.CharField(max_length=50,
                                                                   label="شماره حساب صراف",
                                                                   disabled=True,
                                                                   initial=self.instance.parent_id.dst_owner_bank_account_id)

    def add_dst_owner_field(self):
        self.fields['dst_owner_bank_account_id'] = forms.CharField(max_length=50,
                                                                   label="شماره حساب صادرکننده",
                                                                   disabled=True,
                                                                   initial=self.instance.dst_owner_bank_account_id)

    def perform_exchanger_point_of_view(self):
        self.add_dst_owner_field()
        self.order_fields(self.field_order)

    def perform_exporter_point_of_view(self):
        self.add_src_owner_field()
        self.add_judge_information_fields()
        self.add_remittance_currency_field()
        self.order_fields(self.field_order)

    def perform_judge_point_of_view(self):
        self.add_remittance_currency_field()
        self.add_src_owner_field()
        self.add_dst_owner_field()
        self.order_fields(self.field_order)

    class Meta:
        model = Subcontract
        fields = [
            'value_in_rial',
            'remittance_value',
            'judge_vote',
            'expire_date',
            'description',
            'status',

        ]
        labels = {
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'description': 'توضیحات',
            'judge_vote': 'رای داور',
            'expire_date': 'تاریخ اعتبار',
            'status': 'وضعیت',
        }
