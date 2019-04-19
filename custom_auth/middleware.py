from . views import *

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # import pdb;pdb.set_trace()
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not (request.path.__contains__('login') or request.path.__contains__('admin')):
            response = index(request)
        else:
            response = get_response(request)
        # response = "called"
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware