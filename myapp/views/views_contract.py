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
#                 Q(dst_owner=owner.owner_bank_account_id) | Q(src_owner=owner.owner_bank_account_id))
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
        owner_type = request.GET.get('type', '')
        # user = load_user(national_code)
        # owner = load_owner(owner_bank_account_id)
        owner = get_user_owner(national_code, bank_account_id, raise_error=True)
        new_contract_form = forms.NewContractForm(src_owner=owner)

        context = {
            'user': national_code,
            'owner_type': owner_type,
            'owner': bank_account_id,
            'new_contract_form': new_contract_form
        }
        return Response(context, template_name='myapp/new-contract.html')

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params['user']
        bank_account_id = request.query_params['account']
        owner_type = request.query_params['type']

        if format == 'html':
            new_contract_form = forms.NewContractForm(data=data)
            if new_contract_form.is_valid():
                new_contract = new_contract_form.save(commit=False)
                # new_contract.save()
                created_contract = post_normal_contract(new_contract)
                query_param = '?' + 'role=user' + '&' + 'user=' + national_code + '&' + 'account=' \
                              + bank_account_id + '&' + 'type=' + owner_type
                return redirect(reverse('myapp:my_contract_detail', kwargs={'pk': created_contract.id}) + query_param)
            else:
                context = {
                    'user': national_code,
                    'owner': bank_account_id,
                    'owner_type': owner_type,
                    'new_contract_form': new_contract_form,
                }

                return render(request, 'myapp/new-contract.html', context)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # TODO test later
            serializer = NormalContractSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# incomplete
# class MyContractListView(APIView):
#     renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
#
#     def get_user_list_of_contracts(self, instance):
#         queryset = NormalContract.objects.none()
#         for owner in instance.owners.all():
#             queryset = queryset | NormalContract.objects.filter(
#                 Q(dst_owner=owner.owner_bank_account_id) | Q(src_owner=owner.owner_bank_account_id))
#
#         return queryset
#
#     def get(self, request, format=None):
#         """
#         Return a list of all contracts.
#         """
#         format = request.accepted_renderer.format
#
#         role = request.GET.get('role', '')
#         if role == 'judge':
#             judge_national_id = request.GET.get('judge', '')
#             judge_profile = load_judge(pk=judge_national_id)
#             # contracts = judge_profile.contract_set.all()
#             not_judged_contracts = judge_profile.normalcontract_set.filter(Q(status=ContractStatus.CLAIMED_BY_IMPORTER))
#             judged_contracts = judge_profile.normalcontract_set.filter(Q(status=ContractStatus.JUDGED))
#
#             context = {'judge': judge_profile.national_id, 'judged_contracts': judged_contracts,
#                        'not_judged_contracts': not_judged_contracts}
#             return Response(context, template_name='myapp/judge-contracts-list.html')
#
#         elif role == 'user':
#             user_national_code = request.GET.get('user', '')
#             # user_profile = load_user(pk=user_national_code)
#             user_profile = get_user(user_national_code, raise_error=True)
#             contracts = self.get_user_list_of_contracts(user_profile)
#             serializer = NormalContractSerializer(contracts, many=True)
#             data = serializer.data
#             if format == 'json':
#                 return Response(data)


class MyContractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):

        role = request.GET.get('role', '')
        format = request.accepted_renderer.format

        if role == 'user':
            national_code = request.GET.get('user', '')
            bank_account_id = request.GET.get('account', '')
            owner_type = request.GET.get('type', '')
            action = request.GET.get('action', 'none')

            # user = load_user(pk=national_code)
            # user = get_user(national_code, raise_error=True)
            # owner = load_owner(pk=owner_bank_account_id)
            # owner = get_owner(owner_bank_account_id, raise_error=True)
            # owner = get_user_owner(national_code, bank_account_id)

            # TODO check if the account is for this user

            if action == 'none':

                if format == "html":
                    context = {}

                    if owner_type == OwnerType.IMPORTER:
                        contract = get_user_owner_out_normal_contract(national_code, bank_account_id, pk,
                                                                      raise_error=True)
                        contract_detail_form = forms.ContractDetailForm(instance=contract)
                        if contract.status == ContractStatus.WAITING_FOR_EXCHANGER_ACCEPTANCE:
                            contract_detail_form.hide_judge_vote_field()
                        contract_detail_form.perform_importer_point_of_view()

                    elif owner_type == OwnerType.EXCHANGER:
                        # contract = load_contract(pk)
                        contract = get_user_owner_in_normal_contract(national_code, bank_account_id, pk,
                                                                     raise_error=True)
                        contract_detail_form = forms.ContractDetailForm(instance=contract)
                        if contract.status == ContractStatus.WAITING_FOR_EXCHANGER_ACCEPTANCE:
                            contract_detail_form.hide_judge_vote_field()

                        contract_detail_form.perform_exchanger_point_of_view()
                        # TODO get subcontracts if needed                                                                                                                                                                                                                                                                                                                                                       
                        subcontracts = get_user_owner_in_normal_contract_subcontracts(national_code, bank_account_id, pk)
                        context['subcontracts'] = subcontracts

                    elif owner_type == OwnerType.EXPORTER:
                        # contract = load_subcontract(pk)
                        contract = get_user_owner_in_subcontract(national_code, bank_account_id, pk, raise_error=True)
                        contract_detail_form = forms.SubcontractDetailForm(instance=contract)
                        if contract.status == ContractStatus.WAITING_FOR_EXPORTER_ACCEPTANCE:
                            contract_detail_form.hide_judge_vote()
                        contract_detail_form.perform_exporter_point_of_view()

                    context.update(
                        {
                            'role': role,
                            "user": national_code,
                            "owner": bank_account_id,
                            "owner_type": owner_type,
                            'contract': contract.id,
                            'contract_detail_form': contract_detail_form,
                            'status': contract.status
                        }
                    )
                    return Response(context, template_name='myapp/contract-detail.html')

                else:
                    if owner_type == OwnerType.IMPORTER:
                        contract = get_user_owner_out_normal_contract(national_code, bank_account_id, pk,
                                                                      raise_error=True)

                    elif owner_type == OwnerType.EXCHANGER:
                        # contract = load_subcontract(pk)
                        contract = get_user_owner_in_normal_contract(national_code, bank_account_id, pk,
                                                                     raise_error=True)
                    elif owner_type == OwnerType.EXPORTER:
                        # contract = load_contract(pk)
                        contract = get_user_owner_in_subcontract(national_code, bank_account_id, pk, raise_error=True)

                    serializer = NormalContractSerializer(contract)
                    data = serializer.data
                    return Response(data)

            else:  # with action

                contract = None
                if owner_type == OwnerType.IMPORTER:
                    # contract = load_contract(pk)
                    contract = get_user_owner_out_normal_contract(national_code, bank_account_id, pk, raise_error=True)
                    if action == ContractAction.END.value:
                        contract.status = ContractStatus.CONFIRMED_BY_IMPORTER
                        updated_contract = put_user_owner_out_normal_contract(national_code, bank_account_id, pk, contract)
                    elif action == ContractAction.CLAIM.value:
                        contract.status = ContractStatus.CLAIMED_BY_IMPORTER
                        updated_contract = put_user_owner_out_normal_contract(national_code, bank_account_id, pk, contract)
                    elif action == ContractAction.CHARGE.value:
                        updated_contract = charge_user_owner_out_normal_contract(contract.id, national_code, bank_account_id, OperatorType.USER)

                        pass

                elif owner_type == OwnerType.EXCHANGER:
                    # contract = load_contract(pk)
                    contract = get_user_owner_in_normal_contract(national_code, bank_account_id, pk, raise_error=True)
                    if action == ContractAction.ACCEPT.value:
                        contract.status = ContractStatus.WAITING_FOR_IMPORTER_PAYMENT
                        updated_contract = put_user_owner_in_normal_contract(national_code, bank_account_id, pk, contract)
                    elif action == ContractAction.REJECT.value:
                        contract.status = ContractStatus.REJECTED_BY_EXCHANGER
                        updated_contract = put_user_owner_in_normal_contract(national_code, bank_account_id, pk, contract)
                    else:
                        pass

                elif owner_type == OwnerType.EXPORTER:
                    # contract = load_subcontract(pk)
                    contract = get_user_owner_in_subcontract(national_code, bank_account_id, pk, raise_error=True)
                    if action == ContractAction.ACCEPT.value:
                        contract.status = ContractStatus.WAITING_FOR_EXCHANGER_PAYMENT
                        updated_contract = put_user_owner_in_subcontract(contract)
                    elif action == ContractAction.REJECT.value:
                        contract.status = ContractStatus.REJECTED_BY_EXPORTER
                        updated_contract = put_user_owner_in_subcontract(contract)

                    else:
                        pass

                # contract.save()

                if format == 'html':
                    contract_detail_form = forms.ContractDetailForm(instance=contract)
                    context = {
                        'role': role,
                        "user": national_code,
                        "owner": bank_account_id,
                        "owner_type": owner_type,
                        # 'contract': contract.id,
                        'contract': pk,
                        'contract_detail_form': contract_detail_form,
                        # 'status': contract.status,
                        'status': updated_contract.status,
                    }
                    if owner_type == OwnerType.EXCHANGER:
                        subcontracts = get_user_owner_in_normal_contract_subcontracts(national_code, bank_account_id, updated_contract.id)
                        context['subcontracts'] = subcontracts

                    return Response(context, template_name='myapp/contract-detail.html')

                else:
                    serializer = NormalContractSerializer(updated_contract)
                    data = serializer.data
                    return Response(data)

        elif role == 'judge':
            national_id = request.GET.get('judge', '')
            # judge = load_judge(national_id)
            judge = get_judge(national_id, raise_error=True)
            # contract = load_contract(pk)
            contract = get_contract(pk, raise_error=True)

            judged_subcontracts = contract.subcontract_set.filter(Q(status=ContractStatus.JUDGED))
            not_judged_subcontracts = contract.subcontract_set.filter(Q(status=ContractStatus.CLAIMED_BY_IMPORTER))

            if format == 'html':
                to = request.GET.get('to', '')
                contract_detail_form = forms.ContractDetailForm(instance=contract)
                contract_detail_form.__add_src_owner_field()
                context = {
                    'role': role,
                    'contract': contract.id,
                    'judged_subcontracts': judged_subcontracts,
                    'not_judged_subcontracts': not_judged_subcontracts,
                    'judge': judge.national_id,
                    'contract_detail_form': contract_detail_form,
                    'to': to
                }
                return Response(context, template_name='myapp/judge-contract-detail.html')

            else:
                # TODO add judged and not judged contracts
                serializer = NormalContractSerializer(contract)
                data = serializer.data
                return Response(data)
