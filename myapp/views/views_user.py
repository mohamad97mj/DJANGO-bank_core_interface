from myapp.views.utils import *
from myapp import forms


class UserDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, pk, format=None):
        user_profile = get_user(pk)
        user_profile_form = forms.UserProfileForm(instance=user_profile)
        context = {'user': pk, 'user_profile_form': user_profile_form}
        # TODO rest api
        return Response(context, template_name='myapp/user-profile.html')


class UserListView(generics.ListAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer
    pass
