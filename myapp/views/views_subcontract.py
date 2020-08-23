from myapp.views.utils import *
from myapp import forms


class SubcontractListView(generics.ListAPIView):
    queryset = models.Subcontract.objects.all()
    serializer_class = serializers.SubcontractSerializer
    pass


class MyNewSubcontractView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        contract_id = request.GET.get('contract', '')
        user = get_user(national_code)
        owner = get_owner(bank_account_id)
        contract = get_contract(contract_id)
        new_subcontract_form = forms.NewSubcontractForm()
        context = {'new_subcontract_form': new_subcontract_form, 'user': user.national_code,
                   'owner': owner.bank_account_id, 'contract': contract.id}
        return Response(context, template_name='myapp/new-subcontract.html')

    # TODO define post method

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        national_code = request.query_params['user']
        bank_account_id = request.query_params['account']
        contract_id = request.query_params['contract']

        user = get_user(national_code)
        owner = get_owner(bank_account_id)
        contract = get_contract(contract_id)

        if format == 'html':
            new_subcontract_form = forms.NewSubcontractForm(data=data)
            if new_subcontract_form.is_valid():
                new_subcontract = new_subcontract_form.save(commit=False)
                new_subcontract.parent = contract
                new_subcontract.save()
                query_param = '?' + 'role=user' + '&' + 'user=' + user.national_code + '&' + 'account=' \
                              + str(owner.bank_account_id) + "&" + 'contract=' + str(contract.id)
                return redirect(reverse('myapp:my_subcontract_detail', kwargs={'pk': new_subcontract.id}) + query_param)
            else:
                context = {'user': user.national_code, 'owner': owner.bank_account_id, 'contract': contract.id,
                           'new_subcontract_form': new_subcontract_form}

                return render(request, 'myapp/new-subcontract.html', context)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # TODO test later
            serializer = serializers.ContractSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySubcontractListView(APIView):
    pass


class MySubcontractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):
        role = request.GET.get('role', '')
        contract_id = request.GET.get('contract', '')
        subcontract = get_subcontract(pk)
        subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract)
        contract = get_contract(contract_id)

        format = request.accepted_renderer.format

        if role == 'user':
            if format == 'html':
                national_code = request.GET.get('user', '')
                bank_account_id = request.GET.get('account', '')
                user = get_user(national_code)
                owner = get_owner(bank_account_id)
                if owner.owner_type == '2':  # not necessary
                    subcontract_detail_form.perform_exchanger_point_of_view()

                context = {'user': user.national_code, 'owner': owner.bank_account_id, 'contract': contract.id,
                           'subcontract_detail_form': subcontract_detail_form}

                return Response(context, template_name='myapp/subcontract-detail.html')
            serializer = serializers.SubcontractSerializer(subcontract)
            data = serializer.data
            return Response(data)

        elif role == 'judge':
            national_id = request.GET.get('judge', '')
            to = request.GET.get('to', '')
            judge = get_judge(national_id)
            if format == 'html':
                subcontract_detail_form.perform_judge_point_of_view()
                context = {'judge': judge.national_id, 'contract': contract.id, 'subcontract': subcontract.id,
                           'subcontract_detail_form': subcontract_detail_form, 'to': to}
                return Response(context, template_name='myapp/judge-subcontract-detail.html')

            elif to == 'view':
                serializer = serializers.SubcontractSerializer(subcontract)
                data = serializer.data
                return Response(data)

    def post(self, request, pk, format=None):
        role = request.GET.get('role', '')
        subcontract = get_subcontract(pk)
        contract_id = request.GET.get('contract', '')
        contract = get_contract(contract_id)
        data = request.data
        format = request.accepted_renderer.format

        if role == 'judge':
            national_id = request.GET.get('judge', '')
            judge = get_judge(national_id)
            # to = request.GET.get('to', '')
            vote = data['vote']
            subcontract.status = '4'
            if vote == 'yes':
                subcontract.judge_vote = '1'
            elif vote == 'no':
                subcontract.judge_vote = '2'
            subcontract.save()

            if format == 'html':
                subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract)
                subcontract_detail_form.perform_judge_point_of_view()
                context = {'judge': judge.national_id, 'contract': contract.id, 'subcontract': subcontract.id,
                           'subcontract_detail_form': subcontract_detail_form, 'to': 'view'}
                return Response(context, template_name='myapp/judge-subcontract-detail.html')
