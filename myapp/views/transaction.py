from .utils import *


# class UserTransactionsListView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#     template_name = 'myapp/transactions-list.html'
#
#
#     def get_transaction_list(self, instance):
#         queryset = models.Transaction.objects.none()
#         for owner in instance.owners.all():
#             queryset = queryset | models.Transaction.objects.filter(
#                 Q(owner=owner.bank_account_id) | Q(otherside_owner=owner.bank_account_id))
#
#         return queryset
#
#     def get(self, request, pk, format=None):
#         user_profile = get_user(pk)
#         transactions = self.get_transaction_list(instance=user_profile)
#         return Response({'pk': pk, 'transactions': transactions})


# class TransactionListView(generics.ListAPIView):
#     queryset = models.Transaction.objects.all()
#     serializer_class = serializers.TransactionSerializer
#     pass


class MyNewTransactionView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        new_transaction_form = forms.NewTransactionForm()
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        user = get_user(national_code)
        owner = get_owner(bank_account_id)

        context = {'user': user.national_code, 'owner': owner.bank_account_id,
                   'new_transaction_form': new_transaction_form}
        return Response(context, template_name='myapp/new-transaction.html')


class MyTransactionListView(APIView):
    pass


class MyTransactionDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):
        role = request.GET.get('role', '')
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        user = get_user(pk=national_code)
        owner = get_owner(pk=bank_account_id)
        transaction = get_transaction(pk)
        transaction_detail_form = forms.TransactionDetailForm(instance=transaction)
        context = {
            'transaction': transaction.id,
            'user': user.national_code,
            'owner': owner.bank_account_id,
            'transaction_detail_form': transaction_detail_form}

        if request.accepted_renderer.format == 'html':
            return Response(context, template_name='myapp/transaction-detail.html')
        serializer = serializers.TransactionSerializer(transaction)
        data = serializer.data
        return Response(data)
