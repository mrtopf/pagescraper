import sys
import os
import pkg_resources
import logbook

from framework.utils import get_static_urlparser, TemplateHandler
from quantumcore.storages import AttributeMapper

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    settings['imageapp'] = get_static_urlparser("/tmp")
    #tmpls = settings['templates'] = TemplateHandler(__name__)
    
    settings['log'] = logbook.Logger("quantumlounge")

    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)
    return settings






