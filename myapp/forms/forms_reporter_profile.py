from .utils import *


class ReporterProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['disabled'] = True
        self.fields['full_name'].widget.attrs['disabled'] = True

    class Meta:
        model = ReporterProfile
        fields = ['username', 'full_name']
        labels = {
            'username': 'نام کاربری',
            'full_name': 'نام',
        }
