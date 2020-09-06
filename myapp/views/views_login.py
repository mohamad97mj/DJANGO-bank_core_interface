from myapp.views.utils import *


class LoginView(ObtainAuthToken):

    def get(self, request):
        login_form = forms.LoginForm()
        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)

    def post(self, request, **kwargs):
        # print("post request received")

        login_form = forms.LoginForm(request.data)
        if login_form.is_valid():
            role = request.data['role']
            username = request.data['username']
            password = request.data['password']

            if request.data['role'] == 'user':
                # print(request.data)
                return redirect(
                    reverse('myapp:my_user_detail', kwargs={'pk': request.data['username']}))
            else:
                return redirect('myapp:my_judge_detail', pk=request.data['username'])

            # return redirect(
            #     reverse('myapp:auth', kwargs={'role': role, 'username': username, 'password': password}))

        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)


# class AuthView(ObtainAuthToken):

    # def authenticate(self, request):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     # tmp = request.META['HTTP_AUTHORIZATION']
    #     is_valid = serializer.is_valid()
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({
    #         'token': token.key,
    #         'user_id': user.pk,
    #         'email': user.email
    #     })

    # def get(self, request):
    #     if request.data['role'] == 'user':
    #         # print(request.data)
    #         return redirect(
    #             reverse('myapp:my_user_detail', kwargs={'pk': request.data['username']}))
    #     else:
    #         return redirect('myapp:my_judge_detail', pk=request.data['username'])
    #
    # def post(self, request, *args, **kwargs):
    #     pass
