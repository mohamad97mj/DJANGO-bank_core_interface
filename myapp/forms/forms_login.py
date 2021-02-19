from .utils import *
from django.contrib.auth import authenticate


class LoginForm(Form):
    role = forms.CharField(label='ورود به سامانه به عنوان',
                           widget=forms.Select(choices=LOGIN_ROLES),
                           help_text="")
    username = forms.CharField(max_length=255,
                               label="نام کاربری*",
                               required=False,
                               help_text="به صورت پیش فرض همان کد ملی شماست")
    password = forms.CharField(max_length=255,
                               label="گذرواژه*",
                               widget=forms.PasswordInput, required=False,
                               help_text="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        role = self.cleaned_data['role']
        password = cleaned_data.get("password")
        credential_provided = True

        if not username:
            credential_provided = False
            self.add_error('username', 'خطا: لطفا نام کاربری را وارد کنید!')
        if not password:
            credential_provided = False
            self.add_error('password', 'خطا: لطفا گذرواژه را وارد کنید!')
        if credential_provided:
            if role == 'user':
                user = get_user(username)
                if not user:
                    self.add_error("username", "خطا: کاربر با این مشخصات در سامانه ثبت نشده است!")
            elif role == 'judge':
                judge = get_judge(username)
                if not judge:
                    self.add_error("username", "خطا: داور با این مشخصات در سامانه ثبت نشده است!")

            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error("password", "خطا: نام کاربری یا گذرواژه اشتباه است!")
