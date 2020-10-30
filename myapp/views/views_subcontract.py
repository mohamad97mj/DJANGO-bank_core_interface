from myapp.views.utils import *


class SubcontractListView(generics.ListAPIView):
    queryset = Subcontract.objects.all()
    serializer_class = SubcontractSerializer
    pass


class NewSubcontractView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('account')
        owner_type = request.query_params.get('type')
        contract_id = request.query_params.get('contract')
        new_subcontract_form = forms.NewSubcontractForm()
        context = {
            'new_subcontract_form': new_subcontract_form,
            'user': national_code,
            'owner': bank_account_id,
            'type': owner_type,
            'contract': contract_id,
        }

        return render(request, 'myapp/new-subcontract.html', context)

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params.get('user')
        bank_account_id = request.query_params.get('account')
        owner_type = request.query_params.get('type')
        contract_id = request.query_params.get('contract')
        parent = get_user_public_owner_in_normal_contract(national_code, bank_account_id, contract_id)

        if format == 'html':
            new_subcontract_form = forms.NewSubcontractForm(parent=parent, data=data)
            if new_subcontract_form.is_valid():
                new_subcontract = new_subcontract_form.save(commit=False)
                new_subcontract.parent_id = contract_id
                # new_subcontract.save()
                created_subcontract = post_user_public_owner_subcontract(national_code, bank_account_id, contract_id,
                                                                         new_subcontract)
                query_param = '?' + \
                              'role=user' + '&' + \
                              'user=' + national_code + '&' + \
                              'account=' + bank_account_id + "&" + \
                              'type=' + owner_type + "&" + \
                              'contract=' + str(contract_id)
                return redirect(
                    reverse('myapp:subcontract_detail', kwargs={'pk': created_subcontract.id}) + query_param)
            else:
                context = {
                    'user': national_code,
                    'owner': bank_account_id,
                    'type': owner_type,
                    'contract': contract_id,
                    'new_subcontract_form': new_subcontract_form,
                }

                return render(request, 'myapp/new-subcontract.html', context)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = NormalContractSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubcontractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):

        role = request.query_params.get('role')
        contract_id = request.query_params.get('contract')
        action = request.query_params.get('action', 'none')

        format = request.accepted_renderer.format

        if role == 'user':

            national_code = request.query_params.get('user')
            bank_account_id = request.query_params.get('account')
            owner_type = request.query_params.get('type')

            subcontract = get_user_public_owner_in_normal_contract_subcontract(national_code, bank_account_id, contract_id, pk,
                                                                               raise_error=True)
            subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract)
            if action == 'none':
                if format == 'html':
                    if owner_type == OwnerType.EXCHANGER:  # not necessary
                        subcontract_detail_form.perform_exchanger_point_of_view()

                    context = {
                        'user': national_code,
                        'owner': bank_account_id,
                        'type': owner_type,
                        'parent': contract_id,
                        'contract': pk,
                        'status': subcontract.status,
                        'subcontract_detail_form': subcontract_detail_form
                    }

                    return render(request, 'myapp/subcontract-detail.html', context)

                serializer = serializers.SubcontractSerializer(subcontract)
                data = serializer.data
                return Response(data)
            else:
                if owner_type == OwnerType.EXCHANGER:  # not necessary
                    if action == ContractAction.PAY.value:
                        updated_subcontract = pay_user_owner_public_in_normal_contract_subcontract(national_code,
                                                                                                   bank_account_id,
                                                                                                   contract_id,
                                                                                                   pk,
                                                                                                   OperatorType.NORMAL_USER)
                if format == 'html':
                    query_param = '?' + \
                                  'role=user' + '&' + \
                                  'user=' + national_code + '&' + \
                                  'account=' + bank_account_id + '&' + \
                                  'type=' + owner_type + '&' + \
                                  'contract=' + contract_id
                    return redirect(
                        reverse('myapp:subcontract_detail', kwargs={'pk': updated_subcontract.id}) + query_param)

        elif role == 'judge':
            national_id = request.query_params.get('judge')
            judge = get_judge(national_id)
            subcontract = get_judge_normal_contract_subcontract(national_id, contract_id, pk,
                                                                raise_error=True)
            contract = get_normal_contract(contract_id, raise_error=False)
            subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract, parent=contract)

            if action == 'none':
                if format == 'html':
                    subcontract_detail_form.perform_judge_point_of_view()
                    context = {
                        'judge': judge.national_id,
                        'contract': contract.id,
                        'subcontract': subcontract.id,
                        'subcontract_detail_form': subcontract_detail_form,
                        'status': subcontract.status,
                    }
                    return render(request, 'myapp/judge-subcontract-detail.html', context)

                serializer = serializers.SubcontractSerializer(subcontract)
                data = serializer.data
                return Response(data)

            else:
                updated_subcontract = None
                if action == ContractAction.CONFIRM.value:
                    updated_subcontract = judge_subcontract(national_id, contract_id, pk, OperatorType.NORMAL_USER,
                                                            JudgeVote.DONE)
                elif action == ContractAction.DENY.value:
                    updated_subcontract = judge_subcontract(national_id, contract_id, pk, OperatorType.NORMAL_USER,
                                                            JudgeVote.NOT_DONE)
            if format == 'html':
                query_param = '?' + \
                              'role=judge' + '&' + \
                              'judge=' + national_id + '&' + \
                              'contract=' + contract_id

                return redirect(
                    reverse('myapp:subcontract_detail', kwargs={'pk': updated_subcontract.id}) + query_param)

            else:
                serializer = SubcontractSerializer(updated_subcontract)
                data = serializer.data
                return Response(data)
