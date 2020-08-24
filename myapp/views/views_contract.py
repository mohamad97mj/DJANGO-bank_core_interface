from myapp.views.utils import *
from myapp import forms


# class ContractListView(generics.ListAPIView):
#     queryset = Contract.objects.all()
#     serializer_class = serializers.ContractSerializer
#     pass


# class UserContractsListView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#     template_name = 'myapp/contracts-list.html'
#
#     def get_list(self, instance):
#         queryset = Contract.objects.none()
#         for owner in instance.owners.all():
#             queryset = queryset | Contract.objects.filter(
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
        new_contract_form = forms.NewContractForm(src_owner=owner)

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
            new_contract_form = forms.NewContractForm(data=data)
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
        queryset = NormalContract.objects.none()
        for owner in instance.owners.all():
            queryset = queryset | NormalContract.objects.filter(
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
            not_judged_contracts = judge_profile.normalcontract_set.filter(Q(status=ContractStatus.CLAIMED_BY_IMPORTER))
            judged_contracts = judge_profile.normalcontract_set.filter(Q(status=ContractStatus.JUDGED))

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

            if owner.owner_type == OwnerType.EXPORTER:
                contract = get_subcontract(pk)
                if format == 'html':
                    contract_detail_form = forms.SubcontractDetailForm(instance=contract)
                    if contract.status == ContractStatus.WAITING_FOR_EXPORTER:
                        contract_detail_form.hide_judge_vote_and_status()
                    contract_detail_form.perform_exporter_point_of_view()

            else:
                contract = get_contract(pk)
                if format == 'html':
                    contract_detail_form = forms.ContractDetailForm(instance=contract)
                    if contract.status == ContractStatus.WAITING_FOR_EXCHANGER:
                        contract_detail_form.hide_judge_vote_and_status()
                    if owner.owner_type == OwnerType.IMPORTER:
                        contract_detail_form.perform_importer_point_of_view()
                    else:
                        contract_detail_form.perform_exchanger_point_of_view()

            if format == 'html':
                context = {'role': role, "user": user.national_code, "owner": owner.bank_account_id,
                           "owner_type": owner.owner_type,
                           'contract': contract.id, 'contract_detail_form': contract_detail_form,
                           'status': contract.status}

            if owner.owner_type == OwnerType.EXCHANGER:
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

            judged_subcontracts = contract.subcontract_set.filter(Q(status=ContractStatus.JUDGED))
            not_judged_subcontracts = contract.subcontract_set.filter(Q(status=ContractStatus.CLAIMED_BY_IMPORTER))

            if format == 'html':
                to = request.GET.get('to', '')
                contract_detail_form = forms.ContractDetailForm(instance=contract)
                contract_detail_form.add_src_owner_field()
                context = {'role': role, 'contract': contract.id, 'judged_subcontracts': judged_subcontracts,
                           'not_judged_subcontracts': not_judged_subcontracts,
                           'judge': judge.national_id,
                           'contract_detail_form': contract_detail_form, 'to': to}
                return Response(context, template_name='myapp/judge-contract-detail.html')

            elif to == 'view':
                serializer = serializers.ContractSerializer(contract)
                data = serializer.data
                return Response(data)

    def post(self, request, pk, format=None):
        role = request.GET.get('role', '')
        format = request.accepted_renderer.format

        if role == 'user':
            national_code = request.GET.get('user', '')
            bank_account_id = request.GET.get('account', '')
            action = request.GET.get('action')

            user = get_user(pk=national_code)
            owner = get_owner(pk=bank_account_id)

            if owner.owner_type == OwnerType.IMPORTER:
                contract = get_contract(pk)
                if action == ContractAction.END.value:
                    contract.status = ContractStatus.ENDED_BY_IMPORTER
                elif action == ContractAction.CLAIM.value:
                    contract.status = ContractStatus.CLAIMED_BY_IMPORTER
                    contract.subcontract_set.update(status=ContractStatus.CLAIMED_BY_IMPORTER)
                contract.save()
                if format == 'html':
                    contract_detail_form = forms.ContractDetailForm(instance=contract)

            elif owner.owner_type == OwnerType.EXCHANGER:
                contract = get_contract(pk)
                if action == 'confirm':
                    contract.status = ContractStatus.CONFIRMED_BY_EXCHANGER
                elif action == 'deny':
                    contract.status = ContractStatus.DENIED_BY_EXCHANGER
                else:
                    contract.status = ContractStatus.ENDED_BY_EXCHANGER

                contract.save()
                if format == 'html':
                    contract_detail_form = forms.ContractDetailForm(instance=contract)

            else:
                contract = get_subcontract(pk)
                if action == 'confirm':
                    contract.status = ContractStatus.CONFIRMED_BY_EXPORTER
                elif action == 'deny':
                    contract.status = ContractStatus.DENIED_BY_EXPORTER
                else:
                    contract.status = ContractStatus.ENDED_BY_EXPORTER
                contract.save()
                if format == 'html':
                    contract_detail_form = forms.SubcontractDetailForm(instance=contract)
                    contract_detail_form.perform_exporter_point_of_view()

            #  response .............................................................................................
            if format == 'html':
                context = {'role': role, "user": user.national_code, "owner": owner.bank_account_id,
                           "owner_type": owner.owner_type,
                           'contract': contract.id, 'contract_detail_form': contract_detail_form,
                           'status': contract.status}

                if owner.owner_type == OwnerType.EXCHANGER:
                    subcontracts = contract.subcontract_set.all()
                    if format == 'html':
                        context['subcontracts'] = subcontracts

                return Response(context, template_name='myapp/contract-detail.html')

            serializer = serializers.ContractSerializer(contract)
            data = serializer.data
            return Response(data)

        else:
            pass
