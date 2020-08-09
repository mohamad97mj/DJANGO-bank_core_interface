from .utils import *


class SubcontractListView(generics.ListAPIView):
    queryset = models.Subcontract.objects.all()
    serializer_class = serializers.SubcontractSerializer
    pass


class NewSubcontractView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        new_subcontract_form = forms.NewSubcontractForm()
        context = {'new_subcontract_form': new_subcontract_form}
        return Response(context, template_name='myapp/new-subcontract.html')

    # TODO define post method


class MyNewSubcontractView(APIView):
    pass


class MySubcontractListView(APIView):
    pass


class MySubcontractDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):
        national_code = request.GET.get('user', '')
        bank_account_id = request.GET.get('account', '')
        contract_id = request.GET.get('contract', '')

        subcontract = get_subcontract(pk)
        subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract)
        subcontract_detail_form.add_extra_fields()
        context = {'user': national_code, 'owner': bank_account_id, 'contract': contract_id,
                   'subcontract_detail_form': subcontract_detail_form}
        return Response(context, template_name='myapp/subcontract-detail.html')
