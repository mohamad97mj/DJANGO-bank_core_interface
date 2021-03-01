from myapp.views.utils import *


class ReporterDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):
        reporter_profile = get_reporter(pk)
        reporter_profile_form = forms.ReporterProfileForm(instance=reporter_profile)
        context = {'reporter': pk, 'reporter_profile_form': reporter_profile_form}
        return render(request, 'myapp/reporter-profile.html', context)


class ContradictionReportView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        reporter_id = request.query_params.get('reporter')
        report_form = forms.ContradictionReportForm()
        context = {
            'reporter': reporter_id,
            'report_form': report_form
        }
        return render(request, 'myapp/contradiction-report.html', context)

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        reporter_id = request.query_params.get('reporter')

        if format == 'html':
            report_form = forms.ContradictionReportForm(data=data)
            context = {
                'reporter': reporter_id,
                'report_form': report_form,
            }
            if report_form.is_valid():
                owner_type = report_form.cleaned_data.get('owner_type').lower()
                from_date = report_form.cleaned_data.get('from_date')
                to_date = report_form.cleaned_data.get('to_date')

                # in_external_transactions = get_operational_owner_in_external_transactions(owner_type)
                in_external_transactions = get_operational_owner_in_external_transactions_time_interval(owner_type,
                                                                                                        from_date,
                                                                                                        to_date)
                # out_external_transactions = get_operational_owner_out_external_transactions(owner_type)
                out_external_transactions = get_operational_owner_out_external_transactions_time_interval(owner_type,
                                                                                                          from_date,
                                                                                                          to_date)

                context.update(
                    {
                        'in_external_transactions': in_external_transactions,
                        'out_external_transactions': out_external_transactions,
                        'show': True
                    }
                )

                return render(request, 'myapp/contradiction-report.html', context)
            else:

                context.update(
                    {
                        'show': False
                    }
                )

                return render(request, 'myapp/contradiction-report.html', context)
        # else:
        #     serializer = NormalContractSerializer(data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OutputReportView(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, format=None):
        reporter_id = request.query_params.get('reporter')
        report_form = forms.OutputReportForm()
        context = {
            'reporter': reporter_id,
            'report_form': report_form
        }

        return render(request, 'myapp/output-report.html', context)

    def post(self, request, format=None):
        data = request.data
        format = request.accepted_renderer.format
        reporter_id = request.query_params.get('reporter')

        if format == 'html':
            report_form = forms.OutputReportForm(data=data)
            context = {
                'reporter': reporter_id,
                'report_form': report_form,
            }
            if report_form.is_valid():
                from_date = report_form.cleaned_data.get('from_date')
                to_date = report_form.cleaned_data.get('to_date')
                content = get_system_output(from_date, to_date)
                response = HttpResponse()
                response.write(content)
                response['Content-Type'] = 'application/vnd.ms-excel'
                response['Content-Disposition'] = 'attachment; filename={0}'.format("system_output.xlsx")
                return response
            else:
                return render(request, 'myapp/output-report.html', context)
