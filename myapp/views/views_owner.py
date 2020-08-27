from myapp.views.utils import *


# class OwnerListView(generics.ListAPIView):
#     queryset = Owner.objects.all()
#     serializer_class = serializers.OwnerSerializer
#     pass
#
#
# class UserOwnersListView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#     template_name = 'myapp/accounts-list.html'
#
#     def get_object(self, pk):
#         try:
#             return UserProfile.objects.get(pk=pk)
#         except UserProfile.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user_profile = self.get_object(pk)
#         accounts = user_profile.owners.all()
#         return Response({"pk": pk, "accounts": accounts})


class MyOwnerListView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        # user_profile = get_user(national_code)
        accounts = get_user_owners(national_code)
        if accounts:
            [print(account.bank_account_id) for account in accounts]

        if request.accepted_renderer.format == 'html':
            context = {"user": national_code, "accounts": accounts}
            return Response(context, template_name='myapp/accounts-list.html')

        serializer = serializers.OwnerSerializer(accounts, many=True)
        data = serializer.data
        return Response(data)


class MyOwnerDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    # def get_normal_contracts_list(self, instance):
    #     if instance.owner_type == OwnerType.IMPORTER:
    #         queryset = NormalContract.objects.filter(
    #             Q(src_owner=instance.bank_account_id))
    #     else:
    #         queryset = NormalContract.objects.filter(
    #             Q(dst_owner=instance.bank_account_id))
    #
    #     return queryset

    # def get_subcontracts_list(self, instance):
    #     queryset = Subcontract.objects.filter(
    #         Q(dst_owner=instance.bank_account_id))
    #     return queryset

    # def get_transactions_list(self, instance):
    #     queryset = Transaction.objects.filter(
    #         Q(owner=instance.bank_account_id) | Q(otherside_owner=instance.bank_account_id))
    #     return queryset

    def get(self, request, pk, format=None):

        role = request.GET.get('login-as', )
        national_code = request.GET.get('user', )
        # owner = load_owner(pk)
        owner = get_owner(pk)
        if owner.owner_type == OwnerType.EXPORTER:
            # contracts = self.get_subcontracts_list(owner)
            contracts = get_owner_subcontracts(owner.bank_account_id)
        else:
            # contracts = self.get_normal_contracts_list(owner)
            contracts = get_owner_normal_contracts(owner.bank_account_id)

        for contract in contracts:
            print(contract.id)

        if request.accepted_renderer.format == 'html':
            context = {'user': national_code, 'owner_type': owner.owner_type, 'owner': owner.bank_account_id,
                       "contracts": contracts}
            return Response(context, template_name='myapp/account-detail.html')

        serializer = NormalContractSerializer(contracts, many=True)
        data = serializer.data

        return Response(data)
