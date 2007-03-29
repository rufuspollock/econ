"""
econ.www

This file loads the finished app from econ.www.config.middleware.

"""

# this leads to an error
# from econ.www.config.middleware import make_app
# ...
#   import econ.www.lib.app_globals as app_globals
# AttributeError: 'module' object has no attribute 'www'

def make_app(global_conf, full_stack=True, **app_conf):
    from econ.www.config.middleware import make_app
    return make_app(global_conf, full_stack, **app_conf)
