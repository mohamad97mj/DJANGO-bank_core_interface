from myapp.utils import *
from myapp import forms


# class ContractListView(generics.ListAPIView):
#     queryset = models.Contract.objects.all()
#     serializer_class = serializers.ContractSerializer
#     pass


# class UserContractsListView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#     template_name = 'myapp/contracts-list.html'
#
#     def get_list(self, instance):
#         queryset = models.Contract.objects.none()
#         for owner in instance.owners.all():
#             queryset = queryset | models.Contract.objects.filter(
#                 Q(dst_owner=owner.bank_account_id) | Q(src_owner=owner.bank_account_id))
#
#         return queryset
#
#     def get(self, request, pk, format=None):
#         user_profile = get_user(pk)
#         contracts = self.get_list(instance=user_profile)
#         return Response({"pk": pk, "contracts": contracts})


class MyNewContractView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        user = get_user(national_code)
        owner = get_owner(bank_account_id)
        new_contract_form = forms.NewContractForm(src_owner=owner.bank_account_id)
        if owner.owner_type == '1':
            new_contract_form.fields['dst_owner'].label = "شماره حساب صراف"
        else:
            new_contract_form.fields['dst_owner'].label = "شماره حساب صادر کننده"

        context = {'user': user.national_code, 'owner': owner.bank_account_id, 'new_contract_form': new_contract_form}
        return Response(context, template_name='myapp/new-contract.html')

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params['user']
        bank_account_id = request.query_params['account']

        user = get_user(national_code)
        owner = get_owner(bank_account_id)

        if format == 'html':
            new_contract_form = forms.NewContractForm(data=data, src_owner=data['src_owner'])
            if new_contract_form.is_valid():
                new_contract = new_contract_form.save(commit=False)
                new_contract.save()
                query_param = '?' + 'role=user' + '&' + 'user=' + user.national_code + '&' + 'account=' \
                              + str(owner.bank_account_id)
                return redirect(reverse('myapp:my_contract_detail', kwargs={'pk': new_contract.id}) + query_param)
            else:
                context = {'user': user.national_code, 'owner': owner.bank_account_id,
                           'new_contract_form': new_contract_form}

                return render(request, 'myapp/new-contract.html', context)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # TODO test later
            serializer = serializers.ContractSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# incomplete
class MyContractListView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get_user_list_of_contracts(self, instance):
        queryset = models.NormalContract.objects.none()
        for owner in instance.owners.all():
            queryset = queryset | models.NormalContract.objects.filter(
                Q(dst_owner=owner.bank_account_id) | Q(src_owner=owner.bank_account_id))

        return queryset

    def get(self, request, format=None):
        """
        Return a list of all contracts.
        """
        format = request.accepted_renderer.format

        role = request.GET.get('role', '')
        if role == 'judge':
            judge_national_id = request.GET.get('judge', '')
            judge_profile = get_judge(pk=judge_national_id)
            # contracts = judge_profile.contract_set.all()
            not_judged_contracts = judge_profile.contract_set.filter(Q(status='2'))
            judged_contracts = judge_profile.contract_set.filter(Q(status='3'))

            context = {'judge': judge_profile.national_id, 'judged_contracts': judged_contracts,
                       'not_judged_contracts': not_judged_contracts}
            return Response(context, template_name='myapp/judge-contracts-list.html')

        elif role == 'user':
            user_national_code = request.GET.get('user', '')
            user_profile = get_user(pk=user_national_code)
            contracts = self.get_user_list_of_contracts(user_profile)
            serializer = serializers.ContractSerializer(contracts, many=True)
            data = serializer.data
            if format == 'json':
                return Response(data)


class MyContractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):

        role = request.GET.get('role', '')
        format = request.accepted_renderer.format

        if role == 'user':
            national_code = request.GET.get('user', '')
            bank_account_id = request.GET.get('account', '')

            user = get_user(pk=national_code)
            owner = get_owner(pk=bank_account_id)
            # TODO check if the account is for this user

            if owner.owner_type == '3':
                contract = get_subcontract(pk)
                if format == 'html':
                    contract_detail_form = forms.SubcontractDetailForm(instance=contract)
                    contract_detail_form.fields['dst_owner'].label = "شماره حساب صراف"

            else:
                contract = get_contract(pk)
                if format == 'html':
                    contract_detail_form = forms.ContractDetailForm(instance=contract)
                    if owner.owner_type == '1':
                        contract_detail_form.fields['dst_owner'].label = "شماره حساب صراف"
                    else:
                        if owner.bank_account_id == contract.src_owner:
                            contract_detail_form.fields['dst_owner'].label = 'شماره حساب صادر کننده'
                        else:
                            contract_detail_form.fields['dst_owner'].label = 'شماره حساب وارد کننده'

            if format == 'html':
                context = {'role': role, "user": user.national_code, "owner": owner.bank_account_id,
                           "owner_type": owner.owner_type,
                           'contract': contract.id, 'contract_detail_form': contract_detail_form}

            if owner.owner_type == '2':
                subcontracts = contract.subcontract_set.all()
                if format == 'html':
                    context['subcontracts'] = subcontracts

            if format == 'html':
                return Response(context, template_name='myapp/contract-detail.html')

            serializer = serializers.ContractSerializer(contract)
            data = serializer.data
            return Response(data)

        else:
            national_id = request.GET.get('judge', '')
            judge = get_judge(national_id)
            contract = get_contract(pk)

            subcontracts = contract.subcontract_set.all()

            if format == 'html':
                to = request.GET.get('to', '')
                contract_detail_form = forms.ContractDetailForm(instance=contract)
                context = {'role': role, 'contract': contract.id, 'subcontracts': subcontracts,
                           'judge': judge.national_id,
                           'contract_detail_form': contract_detail_form, 'to': to}
                return Response(context, template_name='myapp/judge-contract-detail.html')

            elif to == 'view':
                serializer = serializers.ContractSerializer(contract)
                data = serializer.data
                return Response(data)
