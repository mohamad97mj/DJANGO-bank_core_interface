from .utils import *

class LoginView(APIView):

    def get(self, request):
        login_form = forms.LoginForm()
        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)

    def post(self, request):
        print("post request received")

        login_form = forms.LoginForm(request.data)
        if login_form.is_valid():
            if request.data['role'] == 'user':
                print(request.data)
                return redirect('myapp:my_user_detail', pk=request.data['username'])
            else:
                return redirect('myapp:my_judge_detail', pk=request.data['username'])

        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)
