__application_name__ = 'econ'
__version__ = '0.5a'
__description__ = 'An open set of economics related tools, data and services.'
__long_description__ = \
'''
'''

def get_config():
    from pylons import config
    conf = config
    return conf

def register_config(config_path):
    import os
    config_path = os.path.abspath(config_path)
    import paste.deploy
    pasteconf = paste.deploy.appconfig('config:' + config_path)
    import econ.config.environment
    econ.config.environment.load_environment(pasteconf.global_conf,
        pasteconf.local_conf)

