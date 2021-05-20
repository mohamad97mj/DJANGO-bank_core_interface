from myapp.views.utils import *
from rest_framework import permissions


class LogoutView(APIView):
    permission_classes = [mypermissions.MyCustomIsAuthenticated]

    def get(self, request):

        if role in LOGIN_ROLES:
            response = redirect(reverse('myapp:login'))
        elif role in SPECIAL_LOGIN_ROLES:
            response = redirect(reverse('myapp:special_login'))
        else:
            raise Http404

        return response
