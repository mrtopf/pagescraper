from framework import Handler, Application
from framework.decorators import html, json

import webscraper
import setup

class MainHandler(Handler):
    """serve some index document"""

    @json()
    def get(self):
        url = self.request.values["url"]
        print url
        ws = webscraper.WebScraper(url)
        res = ws.process()
        return res

class StaticHandler(Handler):
    def get(self, path_info):
        return self.settings.staticapp

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
        #map.connect(None, "/img/{path_info:.*}", handler=StaticHandler)
        #map.connect(None, "/jst/{path_info:.*}", handler=StaticHandler)

    
def main():
    port = 9991
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

