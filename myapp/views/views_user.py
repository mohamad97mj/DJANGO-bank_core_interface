from myapp.views.utils import *


class UserDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request, pk, format=None):
        user_profile = get_user(pk)
        user_profile_form = forms.UserProfileForm(instance=user_profile)
        context = {'user': pk, 'user_profile_form': user_profile_form}
        return Response(context, template_name='myapp/user-profile.html')
