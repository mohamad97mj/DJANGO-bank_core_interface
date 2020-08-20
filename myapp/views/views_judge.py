from myapp.views.utils import *
from myapp import forms


class JudgeDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, pk, format=None):
        judge_profile = get_judge(pk)
        judge_profile_form = forms.JudgeProfileForm(instance=judge_profile)
        context = {'judge': pk, 'judge_profile_form': judge_profile_form}
        return Response(context, template_name='myapp/judge-profile.html')


class JudgeListView(generics.ListAPIView):
    queryset = models.JudgeProfile.objects.all()
    serializer_class = serializers.JudgeSerializer
    pass
