from myapp.views.utils import *
from django.contrib.auth import authenticate
from .views_user import UserDetailView
from .views_judge import JudgeDetailView
from .views_auth import generate_token
from rest_framework import permissions


class LoginView(APIView):

    def get(self, request):
        login_form = forms.LoginForm()
        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)

    def post(self, request, format=None):

        # tmp = request.META['HTTP_AUTHORIZATION']
        login_form = forms.LoginForm(data=request.data)
        if login_form.is_valid():
            role = request.data.get('role')
            username = request.data.get('username')
            payload = {
                'username': username,
                'role': role,
                # 'islogin': 'true',
            }
            token = generate_token(payload)
            response = None
            if role == 'user':
                response = redirect(reverse('myapp:user_detail', kwargs={'pk': username}))
            elif role == 'judge':
                response = redirect('myapp:judge_detail', pk=username)

            payload.update({
                'token': token,
            })
            set_cookies(response, payload)
            return response

        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)




