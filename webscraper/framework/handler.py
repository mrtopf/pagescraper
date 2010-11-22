import os
from paste.urlparser import StaticURLParser
from paste.fileapp import FileApp

from context import PageContext

class Handler(object):
    """a request handler which is also the base class for an application"""
    
    def __init__(self, app=None, request=None, settings={}, start_response = None):
        """initialize the Handler with the calling application and the request
        it has to handle."""
        
        self.app = app
        self.request = request
        self.settings = settings
        self.start_response = start_response
        
    @property
    def context(self):
        """returns a AttributeMapper of default variables to be passed to templates such as the
        base CSS and JS components. It can be overridden in subclasses and appended to in views for 
        different templates.
        
        For instance you can do the following::
        
            return self.app.settings.templates['templates/master.pt'].render(
                something = "foobar",
                **self.tmpl_params
            )

        """
        
        d = dict(
            handler = self,
            js_jquery_link = self.settings['js_resources']("jquery"),            
            js_head_link = self.settings['js_resources']("head"),
            jslinks = self.settings['js_resources'](),
            csslinks = self.settings['css_resources'](),
        )
        return PageContext(d)

class StaticHandler(Handler):
    """a handler for static files. It usually will be instantiated by the :class:`StaticHandlerFactory`.
    """
    
    def __init__(self, filepath=None, **kw):
        self.filepath = filepath
        super(StaticHandler, self).__init__(**kw)
    
    def get(self, path_info):
        return FileApp(os.path.join(self.filepath,path_info))
        
        
class StaticHandlerFactory(object):
    """a Handler factory for static resources such as JS, CSS and template files.
    You need to initialize it with the path to the directory you want to serve"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        
    def __call__(self, **kw):
        return StaticHandler(filepath = self.filepath, **kw)
        
