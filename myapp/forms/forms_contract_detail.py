from .utils import *


class ContractDetailForm(ModelForm):
    field_order = ['id',
                   'src_owner',
                   'dst_owner',
                   'value_in_rial',
                   'remittance_currency',
                   'judge_name',
                   'judge',
                   'judge_vote',
                   'remittance_value',
                   'settlement_type',
                   'expire_date',
                   'status',
                   'description'
                   ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'] = forms.IntegerField(disabled=True, label="شناسه", initial=self.instance.id)
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['settlement_type'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True

    def hide_judge_vote_and_status(self):
        self.fields['judge_vote'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()

    # def display_judge_vote_and_status(self):
    #     self.fields['judge_vote'].widget = forms.TextInput()
    #     self.fields['status'].widget = forms.TextInput()

    def add_judge_information_fields(self):
        self.fields['judge_name'] = forms.CharField(max_length=50,
                                                    required=False,
                                                    label="نام داور",
                                                    disabled=True,
                                                    initial=self.instance.judge.name)

        self.fields['judge'] = forms.CharField(max_length=100,
                                               required=False,
                                               label="شناسه ملی داور",
                                               disabled=True,
                                               initial=self.instance.judge)

    def add_src_owner_field(self):
        self.fields['src_owner'] = forms.CharField(max_length=50,
                                                   required=False,
                                                   label="شماره حساب واردکننده",
                                                   disabled=True,
                                                   initial=self.instance.src_owner)
        self.order_fields(field_order=self.field_order)

    def add_dst_owner_fields(self):
        self.fields['dst_owner'] = forms.CharField(max_length=50,
                                                   required=False,
                                                   label="شماره حساب صراف",
                                                   disabled=True,
                                                   initial=self.instance.dst_owner)

    def perform_importer_point_of_view(self):
        self.add_judge_information_fields()
        self.add_dst_owner_fields()
        self.order_fields(field_order=self.field_order)

    def perform_exchanger_point_of_view(self):
        self.add_judge_information_fields()
        self.add_src_owner_field()
        self.order_fields(field_order=self.field_order)

    class Meta:
        model = NormalContract
        fields = [
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge_vote',
            'expire_date',
            'status',
            'description',
        ]
        labels = {
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'settlement_type': 'نوع تسویه',
            'judge_vote': 'رای داور',
            'expire_date': 'تاریخ اعتبار',
            'status': 'وضعیت',
            'description': 'توضیحات',
        }
