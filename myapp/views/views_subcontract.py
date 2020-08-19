from myapp.utils import *
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


        pass


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
                subcontract_detail_form.add_exporter_fields()
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
                subcontract_detail_form.add_judge_fields()
                context = {'judge': judge.national_id, 'contract': contract.id,
                           'subcontract_detail_form': subcontract_detail_form, 'to': to}
                return Response(context, template_name='myapp/judge-subcontract-detail.html')

            elif to == 'view':
                serializer = serializers.SubcontractSerializer(subcontract)
                data = serializer.data
                return Response(data)

    def put(self, request, pk, format=None):
        subcontract = get_subcontract(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
