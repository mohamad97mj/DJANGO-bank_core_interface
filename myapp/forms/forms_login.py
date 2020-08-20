from .utils import *


class LoginForm(Form):
    role = forms.CharField(label='ورود به سامانه به عنوان', widget=forms.Select(choices=LOGIN_ROLES),
                           help_text="")
    username = forms.CharField(max_length=255, label="نام کاربری*", required=False,
                               help_text="به صورت پیش فرض همان کد ملی شماست")
    password = forms.CharField(max_length=32, label="گذرواژه*", widget=forms.PasswordInput, required=False,
                               help_text="")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        role = self.cleaned_data['role']
        if role == 'user':
            try:
                return UserProfile.objects.get(pk=username).national_code
            except UserProfile.DoesNotExist:
                raise forms.ValidationError("خطا: کاربر با این مشخصات در سامانه ثبت نشده است!")
        else:
            try:
                return JudgeProfile.objects.get(pk=username).national_id
            except JudgeProfile.DoesNotExist:
                raise forms.ValidationError("خطا: داور با این مشخصات در سامانه ثبت نشده است!")
