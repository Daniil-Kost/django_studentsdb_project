# -*- coding: utf-8 -*-

from datetime import datetime
from django.http import HttpResponse

from studentsdb.settings import DEBUG


class RequestTimeMiddleware(object):
    """Display request time on a page """

    def process_request(self, request):
        request.start_time = datetime.now()
        return None

    def process_response(self, request, response):
        # if our process_request was canceled somewhere within
        # middleware stack, we can not calculate request time
        if not hasattr(request, 'start_time'):
            return response

        # check settings of DEBUG,
        # if True - write request time in Template
        if DEBUG == True:
            # calculate request execution time
            request.end_time = datetime.now()
            if 'text/html' in response.get('Content-Type', ''):
                response.write(
                    '<div id="request-took">Request took: %s; DEBUG = True</div>' %
                    str(request.end_time - request.start_time))

        return response

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)
