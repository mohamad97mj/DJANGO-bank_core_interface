from myapp.views.utils import *


class NewTransactionView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('account')
        user = get_user(national_code)
        owner = get_public_owner(bank_account_id)
        new_transaction_form = forms.NewTransactionForm(owner=owner, operator=user.national_code)

        context = {'user': user.national_code, 'owner': owner.bank_account_id,
                   'new_transaction_form': new_transaction_form}
        return Response(context, template_name='myapp/new-transaction.html')

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('account')

        user = get_user(national_code)
        owner = get_public_owner(bank_account_id)

        if format == 'html':
            new_transaction_form = forms.NewTransactionForm(data=data,
                                                            owner=load_owner(data['owner']),
                                                            operator=data['operator'])
            if new_transaction_form.is_valid():
                new_transaction = new_transaction_form.save(commit=False)
                new_transaction.save()
                query_param = '?' + \
                              'role=user' + '&' + \
                              'user=' + national_code + '&' + \
                              'account=' + owner.bank_account_id
                return redirect(reverse('myapp:transaction_detail', kwargs={'pk': new_transaction.id}) + query_param)
            else:
                context = {'new_transaction_form': new_transaction_form, 'user': user.national_code,
                           'owner': owner.bank_account_id}
                return Response(context, template_name='myapp/new-transaction.html')
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = serializers.TransactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):
        role = request.query_params.get('role')
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('account')
        user = get_user(national_code)
        owner = get_public_owner(bank_account_id)
        transaction = load_transaction(pk)
        transaction_detail_form = forms.TransactionDetailForm(instance=transaction)

        transaction_detail_form.fields['dst_owner_bank_account_id'].label = "hello"

        if owner.owner_type != OWNER_TYPE.EXCHANGER:
            transaction_detail_form.fields['dst_owner_bank_account_id'].label = 'شماره حساب صراف'
            if owner.owner_type == OwnerType.IMPORTER:
                transaction_detail_form.fields['transaction_type'].initial = '1'
            else:
                transaction_detail_form.fields['transaction_type'].initial = '2'
        else:
            if owner.bank_account_id == transaction.src_owner:
                transaction_detail_form.fields['dst_owner_bank_account_id'].label = 'شماره حساب صادرکننده'
                transaction_detail_form.initial['otherside_owner'] = transaction.dst_owner_bank_account_id
                transaction_detail_form.fields['transaction_type'].initial = '1'
            else:
                transaction_detail_form.fields['dst_owner_bank_account_id'].label = 'شماره حساب واردکننده'
                transaction_detail_form.initial['otherside_owner'] = transaction.src_owner
                transaction_detail_form.fields['transaction_type'].initial = '2'

        context = {
            'transaction': transaction.id,
            'user': user.national_code,
            'transaction_detail_form': transaction_detail_form}

        if request.accepted_renderer.format == 'html':
            return Response(context, template_name='myapp/transaction-detail.html')
        serializer = serializers.TransactionSerializer(transaction)
        data = serializer.data
        return Response(data)
