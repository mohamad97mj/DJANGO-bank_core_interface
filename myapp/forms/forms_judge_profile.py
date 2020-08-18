from .utils import *


class JudgeProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_id'].widget.attrs['disabled'] = True
        self.fields['name'].widget.attrs['disabled'] = True

    class Meta:
        model = JudgeProfile
        fields = ['national_id', 'name']
        labels = {
            'national_id': 'شناسه ملی',
            'name': 'نام',
        }
