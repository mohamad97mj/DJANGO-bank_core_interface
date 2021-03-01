from myapp.views.utils import *


class ContractListView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all contracts.
        """
        format = request.accepted_renderer.format

        role = request.GET.get('role', '')
        if role == 'judge':
            judge_national_id = request.GET.get('judge', '')
            judged_contracts = get_judged_normal_contracts(judge_national_id)
            not_judged_contracts = get_not_judged_normal_contracts(judge_national_id)

            context = {
                'judge': judge_national_id,
                'judged_contracts': judged_contracts,
                'not_judged_contracts': not_judged_contracts
            }
            return Response(context, template_name='myapp/judge-contracts-list.html')


class NewContractView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('owner')
        owner_type = request.query_params.get('type')
        owner = get_user_public_owner(national_code, bank_account_id, raise_error=True)
        new_contract_form = forms.NewContractForm(src_owner=owner)

        context = {
            'user': national_code,
            'type': owner_type,
            'owner': bank_account_id,
            'new_contract_form': new_contract_form
        }
        return render(request, 'myapp/new-contract.html', context)

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('owner')
        owner_type = request.query_params.get('type')

        if format == 'html':
            new_contract_form = forms.NewContractForm(data=data)
            if new_contract_form.is_valid():
                new_contract = new_contract_form.save(commit=False)
                # new_contract.save()
                created_contract = post_user_public_owner_normal_contract(national_code, bank_account_id, new_contract)
                query_param = '?' + \
                              'role=user' + '&' + \
                              'user=' + national_code + '&' + \
                              'owner=' + bank_account_id + '&' + \
                              'type=' + owner_type
                return redirect(reverse('myapp:contract_detail', kwargs={'pk': created_contract.id}) + query_param)
            else:
                context = {
                    'user': national_code,
                    'owner': bank_account_id,
                    'type': owner_type,
                    'new_contract_form': new_contract_form,
                }

                return render(request, 'myapp/new-contract.html', context)

        # else:
        #     serializer = NormalContractSerializer(data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):

        role = request.query_params.get('role')
        format = request.accepted_renderer.format

        if role == 'user':
            national_code = request.query_params.get('user')
            bank_account_id = request.query_params.get('owner')
            owner_type = request.query_params.get('type')
            action = request.query_params.get('action', '')

            if action:

                if format == "html":
                    context = {}

                    contract = None
                    if owner_type == OwnerType.IMPORTER:
                        contract = get_user_public_owner_out_normal_contract(national_code, bank_account_id, pk,
                                                                             raise_error=True)
                        contract_detail_form = forms.ContractDetailForm(instance=contract)
                        contract_detail_form.perform_importer_point_of_view()

                    elif owner_type == OwnerType.EXCHANGER:
                        contract = get_user_public_owner_in_normal_contract(national_code, bank_account_id, pk,
                                                                            raise_error=True)
                        contract_detail_form = forms.ContractDetailForm(instance=contract)

                        contract_detail_form.perform_exchanger_point_of_view()
                        subcontracts = get_user_public_owner_in_normal_contract_subcontracts(national_code,
                                                                                             bank_account_id,
                                                                                             pk)
                        context['subcontracts'] = subcontracts

                    elif owner_type == OwnerType.EXPORTER:
                        contract = get_user_public_owner_in_subcontract(national_code, bank_account_id, pk,
                                                                        raise_error=True)
                        parent = get_normal_contract(contract.parent_id, raise_error=True)
                        contract_detail_form = forms.SubcontractDetailForm(instance=contract, parent=parent)
                        contract_detail_form.perform_exporter_point_of_view()

                    context.update(
                        {
                            'role': role,
                            "user": national_code,
                            "owner": bank_account_id,
                            "type": owner_type,
                            'contract': contract.id,
                            'contract_detail_form': contract_detail_form,
                            'status': contract.status
                        }
                    )
                    return render(request, 'myapp/contract-detail.html', context)

                # else:
                #     if owner_type == OwnerType.IMPORTER:
                #         contract = get_user_public_owner_out_normal_contract(national_code, bank_account_id, pk,
                #                                                              raise_error=True)
                #
                #     elif owner_type == OwnerType.EXCHANGER:
                #         contract = get_user_public_owner_in_normal_contract(national_code, bank_account_id, pk,
                #                                                             raise_error=True)
                #     elif owner_type == OwnerType.EXPORTER:
                #         contract = get_user_public_owner_in_subcontract(national_code, bank_account_id, pk,
                #                                                         raise_error=True)
                #
                #     serializer = NormalContractSerializer(contract)
                #     data = serializer.data
                #     return Response(data)

            else:  # with action

                if owner_type == OwnerType.IMPORTER:
                    contract = get_user_public_owner_out_normal_contract(national_code, bank_account_id, pk,
                                                                         raise_error=True)
                    if action == ContractAction.CONFIRM.value:
                        contract.status = ContractStatus.CONFIRMED_BY_IMPORTER
                        updated_contract = put_user_public_owner_out_normal_contract(national_code,
                                                                                     bank_account_id,
                                                                                     pk,
                                                                                     contract)
                    elif action == ContractAction.CLAIM.value:
                        updated_contract = claim_user_public_owner_out_normal_contract(national_code,
                                                                                       bank_account_id,
                                                                                       pk,
                                                                                       OperatorType.NORMAL_USER)
                    elif action == ContractAction.CHARGE.value:
                        updated_contract = charge_user_public_owner_out_normal_contract(national_code,
                                                                                        bank_account_id,
                                                                                        pk,
                                                                                        OperatorType.NORMAL_USER)

                elif owner_type == OwnerType.EXCHANGER:
                    contract = get_user_public_owner_in_normal_contract(national_code, bank_account_id, pk,
                                                                        raise_error=True)
                    if action == ContractAction.ACCEPT.value:
                        contract.status = ContractStatus.WAITING_FOR_IMPORTER_PAYMENT
                    elif action == ContractAction.REJECT.value:
                        contract.status = ContractStatus.REJECTED_BY_EXCHANGER
                    elif action == ContractAction.END.value:
                        contract.status = ContractStatus.WAITING_FOR_IMPORTER_CONFIRMATION
                        subcontracts = get_user_public_owner_in_normal_contract_subcontracts(national_code,
                                                                                             bank_account_id,
                                                                                             pk)
                        for subcontract in subcontracts:
                            subcontract.status = ContractStatus.WAITING_FOR_IMPORTER_CONFIRMATION
                            put_user_public_owner_in_normal_contract_subcontract(national_code, bank_account_id, pk,
                                                                                 subcontract.id, subcontract)
                    updated_contract = put_user_public_owner_in_normal_contract(national_code, bank_account_id, pk,
                                                                                contract)

                elif owner_type == OwnerType.EXPORTER:

                    contract = get_user_public_owner_in_subcontract(national_code, bank_account_id, pk,
                                                                    raise_error=True)
                    if action == ContractAction.ACCEPT.value:
                        contract.status = ContractStatus.WAITING_FOR_EXCHANGER_PAYMENT
                    elif action == ContractAction.REJECT.value:
                        contract.status = ContractStatus.REJECTED_BY_EXPORTER
                    elif action == ContractAction.END.value:
                        contract.status = ContractStatus.WAITING_FOR_PARENT
                    updated_contract = put_user_owner_in_subcontract(national_code, bank_account_id, pk, contract)

                if format == 'html':
                    query_param = '?' + \
                                  'role=user' + '&' + \
                                  'user=' + national_code + '&' + \
                                  'owner=' + bank_account_id + '&' + \
                                  'type=' + owner_type
                    return redirect(
                        reverse('myapp:contract_detail', kwargs={'pk': updated_contract.id}) + query_param)

                # else:
                #     serializer = NormalContractSerializer(updated_contract)
                #     data = serializer.data
                #     return Response(data)

        elif role == 'judge':
            national_id = request.query_params.get('judge')
            to = request.query_params.get('to')
            # contract = load_contract(pk)
            if format == 'html':
                context = {
                    'role': 'judge',
                    'judge': national_id,
                    'contract': pk,
                }

                if to == 'view':
                    contract = get_judged_normal_contract(national_id, pk, True)
                    subcontracts = get_judged_normal_contract_subcontracts(national_id, pk, )

                    context.update({
                        'subcontracts': subcontracts,
                    })
                else:
                    contract = get_not_judged_normal_contract(national_id, pk, True)
                    judged_subcontracts = get_not_judged_normal_contracts_judged_subcontracts(national_id, pk)
                    not_judge_subcontracts = get_not_judged_normal_contracts_not_judged_subcontracts(national_id, pk)
                    context.update({
                        'judged_subcontracts': judged_subcontracts,
                        'not_judged_subcontracts': not_judge_subcontracts,
                    })

                contract_detail_form = forms.ContractDetailForm(instance=contract)
                contract_detail_form.perform_judge_point_of_view()
                context.update({
                    'contract_detail_form': contract_detail_form,
                    'status': contract.status,
                })
                return render(request, 'myapp/judge-contract-detail.html', context)

            # else:
            #     serializer = NormalContractSerializer(contract)
            #     data = serializer.data
            #     return Response(data)


def get_judge_name(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        judge_national_id = request.GET.get('judge_national_id', None)
        if judge_national_id is not None:
            judge = get_judge(judge_national_id)

            if judge:
                return JsonResponse({"valid": True, 'judge_name': judge.name}, status=200)
            else:
                return JsonResponse({"valid": False}, status=200)

    return JsonResponse({}, status=400)
