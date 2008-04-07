"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('', controller='root', action='index')
    map.connect('plot/:action', controller='plot', action='index')
    map.connect('store/:action/:id', controller='store', action='index',
            requirements=dict(action='index|list|search|view|create')
            )
    map.connect('store/:id/:action', controller='store', action='view')
    map.connect(':action', controller='root')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')

    return map
