from rest_framework import permissions
import myapp.views.utils as utils


class MyCustomIsAuthenticated(permissions.BasePermission):
    """
    Custom permission
    """

    def has_permission(self, request, view):
        token = utils.get_token_from_cookies(request)
        if token:
            data = utils.get_date_from_cookies(request)

            # if data.get('islogin') != 'true':
            #     return False

            decoded_data = utils.decode_token(token=token)
            old_hashed_data = decoded_data.get("hashed")
            new_hashed_data = utils.calculate_hash(data)
            view_type = type(view).__name__

            if view_type == 'UserDetailView' or view_type == 'JudgeDetailView' or view_type == 'ReporterDetailView':
                requested_username = view.kwargs.get('pk')
            else:
                role = data.get('role')
                requested_username = request.query_params.get(role)

            username = data.get('username')
            return old_hashed_data == new_hashed_data and username == requested_username
        else:
            return False
