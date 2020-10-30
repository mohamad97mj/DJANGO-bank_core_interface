from myapp.views.utils import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .views_user import UserDetailView
from .views_judge import JudgeDetailView
from .views_auth import generate_token


class SpecialLoginView(APIView):

    def get(self, request):

        special_login_form = forms.SpecialLoginForm()
        context = {'special_login_form': special_login_form}
        return render(request, 'myapp/special-login.html', context)

    def post(self, request, format=None):

        special_login_form = forms.SpecialLoginForm(data=request.data)
        if special_login_form.is_valid():
            role = request.data.get('role')
            username = request.data.get('username')
            payload = {
                'username': username,
                'role': role,
            }
            token = generate_token(payload)
            response = None
            if role == 'reporter':
                response = redirect(reverse('myapp:reporter_detail', kwargs={'pk': username}))
            # elif role == 'admin':
            #     response = redirect('myapp:admin_detail', pk=username)

            payload.update({
                'token': token,
            })
            set_cookies(response, payload)
            return response

        context = {'special_login_form': special_login_form}
        return render(request, 'myapp/special-login.html', context)




