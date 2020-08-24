from myapp.views.utils import *


def get_owners(user_national_code):
    owners = []
    r = requests.get("http://localhost:8080/api/users/{}/owners".format(user_national_code))
    for j in r.json():
        owner_serializer = OwnerSerializer(data=j)
        flag = owner_serializer.is_valid()
        if owner_serializer.is_valid():
            owner = Owner(j['bank_account_id'], j['owner_type'])
            owners.append(owner)
    print("hello")
    return owners


class OwnerListView(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = serializers.OwnerSerializer
    pass


class UserOwnersListView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/accounts-list.html'

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        accounts = user_profile.owners.all()
        return Response({"pk": pk, "accounts": accounts})


class MyOwnerListView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        # user_profile = get_user(national_code)
        accounts = get_owners(national_code)
        for account in accounts:
            print(account.bank_account_id)

        if request.accepted_renderer.format == 'html':
            context = {"user": national_code, "accounts": accounts}
            return Response(context, template_name='myapp/accounts-list.html')

        serializer = serializers.OwnerSerializer(accounts, many=True)
        data = serializer.data
        return Response(data)


class MyOwnerDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get_normal_contracts_list(self, instance):
        if instance.owner_type == OwnerType.IMPORTER:
            queryset = NormalContract.objects.filter(
                Q(src_owner=instance.bank_account_id))
        else:
            queryset = NormalContract.objects.filter(
                Q(dst_owner=instance.bank_account_id))

        return queryset

    def get_subcontracts_list(self, instance):
        queryset = Subcontract.objects.filter(
            Q(dst_owner=instance.bank_account_id))
        return queryset

    def get_transactions_list(self, instance):
        queryset = Transaction.objects.filter(
            Q(owner=instance.bank_account_id) | Q(otherside_owner=instance.bank_account_id))
        return queryset

    def get(self, request, pk, format=None):

        role = request.GET.get('login-as', )
        national_code = request.GET.get('user', )
        owner = get_owner(pk=pk)
        user_profile = get_user(pk=national_code)

        if owner.owner_type == OwnerType.EXPORTER:  # exporter
            contracts = self.get_subcontracts_list(owner)
        else:
            contracts = self.get_normal_contracts_list(owner)

        transactions = self.get_transactions_list(owner)

        if request.accepted_renderer.format == 'html':
            context = {'user': national_code, 'owner_type': owner.owner_type, 'owner': owner.bank_account_id,
                       "contracts": contracts, 'transactions': transactions}
            return Response(context, template_name='myapp/account-detail.html')

        serializer = serializers.ContractSerializer(contracts, many=True)
        data = serializer.data

        return Response(data)
