import werkzeug
import routes

import handler

class Application(object):
    """a base class for dispatching WSGI requests"""
    
    def __init__(self, settings={}, prefix=""):
        """initialize the Application with a settings dictionary and an optional
        ``prefix`` if this is a sub application"""
        self.settings = settings
        self.mapper = routes.Mapper()
        self.setup_handlers(self.mapper)

    def __call__(self, environ, start_response):
        request = werkzeug.Request(environ)
        path = environ['PATH_INFO']
        
        if len(path)>0 and path[-1]=="/" and path!='/':
            path = path[:-1]

        m = self.mapper.match(path)
        if m is not None:
            handler = m['handler'](app=self, request=request, settings=self.settings, start_response=start_response)
            method = request.method.lower()
            if hasattr(handler, method):
                self.settings.log.debug("calling method %s on handler '%s' " %(request.method, m['handler']))
                del m['handler']
                response = getattr(handler, method)(**m)
            else:
                return werkzeug.exceptions.MethodNotAllowed()(environ, start_response)
            # call the response
            return response(environ, start_response)        
        # no view found => 404
        return werkzeug.exceptions.NotFound()(environ, start_response)
