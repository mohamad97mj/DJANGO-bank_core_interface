from .utils import *
from django.contrib.auth import authenticate


class SpecialLoginForm(Form):
    role = forms.CharField(label='ورود به سامانه به عنوان', widget=forms.Select(choices=SPECIAL_LOGIN_ROLES),
                           help_text="")
    username = forms.CharField(max_length=255, label="نام کاربری*", required=False,)
    password = forms.CharField(max_length=255, label="گذرواژه*", widget=forms.PasswordInput, required=False,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        role = self.cleaned_data['role']
        if role == 'reporter':
            reporter = get_reporter(username)
            if not reporter:
                self.add_error("username", "خطا: گزارش دهنده با این مشخصات در سامانه ثبت نشده است!")
        # elif role == 'admin':
        #     admin = get_admin(username)
        #     if not admin:
        #         self.add_error("username", "خطا: ادمین با این مشخصات در سامانه ثبت نشده است!")

        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error("password", "خطا: نام کاربری یا گذرواژه اشتباه است!")
