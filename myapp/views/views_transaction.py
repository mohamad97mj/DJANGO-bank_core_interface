from myapp.views.utils import *
from myapp import forms


# class UserTransactionsListView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#     template_name = 'myapp/transactions-list.html'
#
#
#     def get_transaction_list(self, instance):
#         queryset = Transaction.objects.none()
#         for owner in instance.owners.all():
#             queryset = queryset | Transaction.objects.filter(
#                 Q(owner=owner.bank_account_id) | Q(otherside_owner=owner.bank_account_id))
#
#         return queryset
#
#     def get(self, request, pk, format=None):
#         user_profile = get_user(pk)
#         transactions = self.get_transaction_list(instance=user_profile)
#         return Response({'pk': pk, 'transactions': transactions})


# class TransactionListView(generics.ListAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = serializers.TransactionSerializer
#     pass


class MyNewTransactionView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        # user = load_user(national_code)
        user = get_user(national_code)
        # owner = load_owner(bank_account_id)
        owner = get_owner(bank_account_id)
        new_transaction_form = forms.NewTransactionForm(owner=owner, operator=user.national_code)

        context = {'user': user.national_code, 'owner': owner.bank_account_id,
                   'new_transaction_form': new_transaction_form}
        return Response(context, template_name='myapp/new-transaction.html')

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params['user']
        bank_account_id = request.query_params['account']

        user = load_user(national_code)
        owner = load_owner(bank_account_id)

        if format == 'html':
            new_transaction_form = forms.NewTransactionForm(data=data,
                                                            owner=load_owner(data['owner']),
                                                            operator=data['operator'])
            if new_transaction_form.is_valid():
                new_transaction = new_transaction_form.save(commit=False)
                new_transaction.save()
                query_param = '?' + 'role=user' + '&' + 'user=' + national_code + '&' + 'account=' \
                              + str(owner.bank_account_id)
                return redirect(reverse('myapp:my_transaction_detail', kwargs={'pk': new_transaction.id}) + query_param)
            else:
                context = {'new_transaction_form': new_transaction_form, 'user': user.national_code,
                           'owner': owner.bank_account_id}
                return render(request, 'myapp/new-transaction.html', context)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # TODO test later
            serializer = serializers.TransactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTransactionListView(APIView):
    pass


class MyTransactionDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):
        role = request.GET.get('role', '')
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        user = load_user(pk=national_code)
        owner = load_owner(path_variable=bank_account_id)
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
                transaction_detail_form.fields['dst_owner_bank_account_id'].label = 'شماره حساب وارد کننده'
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
