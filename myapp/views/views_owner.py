from myapp.views.utils import *


class OwnerListView(APIView):
    permission_classes = [mypermissions.MyCustomIsAuthenticated]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)

    def get(self, request, format=None):
        national_code = request.query_params.get('user')

        # user_profile = get_user(national_code)
        owners = get_user_public_owners(national_code)

        if request.accepted_renderer.format == 'html':
            context = {"user": national_code, "owners": owners}
            return Response(context, template_name='myapp/owners-list.html')

        serializer = serializers.OwnerSerializer(owners, many=True)
        data = serializer.data
        return Response(data)


class OwnerDetailView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):

        role = request.query_params.get('role')
        owner_type = request.query_params.get('type')
        national_code = request.query_params.get('user')

        contracts = None
        if owner_type == OwnerType.IMPORTER:
            contracts = get_user_public_owner_out_normal_contracts(national_code, pk)
        elif owner_type == OwnerType.EXCHANGER:
            contracts = get_user_public_owner_in_normal_contracts(national_code, pk)
        elif owner_type == OwnerType.EXPORTER:
            contracts = []
            subcontracts = get_user_public_owner_in_subcontracts(national_code, pk)
            for subcontract in subcontracts:
                parent = get_normal_contract(subcontract.parent_id)
                contracts.append((subcontract, parent))

        if request.accepted_renderer.format == 'html':
            context = {
                'role': role,
                'user': national_code,
                'type': owner_type,
                'owner': str(pk),
                "contracts": contracts
            }
            return Response(context, template_name='myapp/owner-detail.html')

        # serializer = NormalContractSerializer(contracts, many=True)
        # data = serializer.data
        #
        # return Response(data)
