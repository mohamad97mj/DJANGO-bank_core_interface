from django.http import HttpResponse
from django.conf import settings
import traceback
from myapp.client.exceptions import *
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError


class ExceptionHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                # Format your message here
                # message = "**{url}**\n\n{error}\n\n````{tb}````".format(
                #     url=request.build_absolute_uri(),
                #     error=repr(exception),
                #     tb=traceback.format_exc()
                # )
                # Do now whatever with this message
                # e.g. requests.post(<slack channel/teams channel>, data=message)

                response = HttpResponseServerError
                if isinstance(exception, Http400):
                    response = HttpResponseBadRequest
                elif isinstance(exception, Http404):
                    response = HttpResponseNotFound
                elif isinstance(exception, Http500):
                    response = HttpResponseServerError
                return response(repr(exception))


