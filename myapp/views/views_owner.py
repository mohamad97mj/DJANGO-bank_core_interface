from myapp.utils import *
from myapp import forms


class OwnerListView(generics.ListAPIView):
    queryset = models.Owner.objects.all()
    serializer_class = serializers.OwnerSerializer
    pass


class UserOwnersListView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/accounts-list.html'

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # tmp = request.GET.get('test', '')
        # print("temppppppppppp", tmp)
        user_profile = self.get_object(pk)
        accounts = user_profile.owners.all()
        return Response({"pk": pk, "accounts": accounts})


class MyOwnerListView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        user_profile = get_user(national_code)
        accounts = user_profile.owners.all()
        if request.accepted_renderer.format == 'html':
            context = {"user": national_code, "accounts": accounts}
            return Response(context, template_name='myapp/accounts-list.html')

        serializer = serializers.OwnerSerializer(accounts, many=True)
        data = serializer.data
        return Response(data)


class MyOwnerDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get_contracts_list(self, instance):
        queryset = models.NormalContract.objects.filter(
            Q(src_owner=instance.bank_account_id) | Q(dst_owner=instance.bank_account_id))
        return queryset

    def get_subcontracts_list(self, instance):
        queryset = models.Subcontract.objects.filter(
            Q(dst_owner=instance.bank_account_id))
        return queryset

    def get_transactions_list(self, instance):
        queryset = models.Transaction.objects.filter(
            Q(owner=instance.bank_account_id) | Q(otherside_owner=instance.bank_account_id))
        return queryset

    def get(self, request, pk, format=None):

        role = request.GET.get('login-as', )
        national_code = request.GET.get('user', )
        owner = get_owner(pk=pk)
        user_profile = get_user(pk=national_code)

        if owner.owner_type == '3':  # exporter
            contracts = self.get_subcontracts_list(owner)
        else:
            contracts = self.get_contracts_list(owner)

        transactions = self.get_transactions_list(owner)

        if request.accepted_renderer.format == 'html':
            context = {'user': national_code, 'owner_type': owner.owner_type, 'owner': owner.bank_account_id,
                       "contracts": contracts, 'transactions': transactions}
            return Response(context, template_name='myapp/account-detail.html')

        serializer = serializers.ContractSerializer(contracts, many=True)
        data = serializer.data

        return Response(data)
