from framework import Handler, Application
from framework.decorators import html, json, image

import webscraper
import werkzeug
import simplejson
import setup

class MainHandler(Handler):
    """serve some index document"""

    def get(self):
        url = self.request.values["url"]
        ws = webscraper.WebScraper(url)
        res = ws.process()
        print res
        callback = self.request.args.get("callback", None)
        if callback is not None:
            print "using jsonp with callback ", callback
            # jsonp
            s = "%s(%s)" %(callback, simplejson.dumps(res))
            response = werkzeug.Response(s)
            response.content_type = "application/javascript"
            return response
        response = werkzeug.Response(simplejson.dumps(res))
        response.content_type = "application/json"
        return response

class StaticHandler(Handler):
    def get(self, path_info):
        return self.settings.staticapp

class ImageHandler(Handler):
    def get(self, path_info):
        return self.settings.imageapp

class CSSResourceHandler(Handler):
    def get(self, path_info):
        return self.settings['css_resources'].render_wsgi
        
class JSResourceHandler(Handler):
    def get(self, path_info):
        return self.settings['js_resources'].render_wsgi


class App(Application):

    def setup_handlers(self, map):
        """setup the mapper"""
        map.connect(None, "/", handler=MainHandler)
        #map.connect(None, "/js2/{path_info:.*}", handler=StaticHandler)
        #map.connect(None, "/css/{path_info:.*}", handler=CSSResourceHandler)
        #map.connect(None, "/js/{path_info:.*}", handler=JSResourceHandler)
        map.connect(None, "/images/{path_info:.*}", handler=ImageHandler)
        #map.connect(None, "/jst/{path_info:.*}", handler=StaticHandler)

    
def main():
    port = 9992
    app = App(setup.setup())
    return webserver(app, port)

def app_factory(global_config, **local_conf):
    settings = setup.setup(**local_conf)
    return App(settings)

def webserver(app, port):
    import wsgiref.simple_server
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if __name__=="__main__":
    main()

