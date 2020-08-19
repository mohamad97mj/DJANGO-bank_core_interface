from .utils import *


class UserProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_code'].widget.attrs['disabled'] = True
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True

    class Meta:
        model = UserProfile
        fields = ['national_code', 'first_name', 'last_name']
        labels = {
            'national_code': 'کد ملی',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }
