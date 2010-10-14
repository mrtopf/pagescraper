"""
some useful decorators
"""

import werkzeug
import functools
import simplejson

def html(method):
    """takes a string output of a view and wraps it into a text/html response"""
    
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        response = werkzeug.Response(method(*args, **kwargs))
        response.content_type = "text/html"
        return response

    return wrapper
        

class json(object):
    
    def __init__(self, **headers):
        self.headers = {}
        for a,v in headers.items():
            ps = a.split("_")
            ps = [p.capitalize() for p in ps]
            self.headers["-".join(ps)] = v
    
    def __call__(self, method):
        """takes a dict output of a handler method and returns it as JSON"""
    
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            data = method(*args, **kwargs)
            response = werkzeug.Response(simplejson.dumps(data))
            response.content_type = "application/json"
            for a,v in self.headers.items():
                response.headers[a] = v
            return response

        return wrapper
        