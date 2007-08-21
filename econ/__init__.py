__application_name__ = 'econ'
__version__ = '0.4'
__description__ = 'An open set of economics related tools, data and services.'
__long_description__ = \
'''
'''

def setup_config():
    conf = get_config()
    CONFIG.push_process_config({'app_conf': conf.local_conf,
                                'global_conf': conf.global_conf}) 

def get_config(default_path='development.ini'):
    """Load config file and return configobj containing that information.
    
    Config file is located using 'ECONCONF' environment variable or, if that
    does not exist, looking for a file 'development.ini' (note that this path
    is taken in relation to the current directory.
    """
    import os
    default_path = os.path.abspath(default_path)
    env_var_name = __application_name__.upper() + 'CONF'
    config_file = os.environ.get(env_var_name, default_path)
    if not os.path.exists(config_file):
        raise ValueError('No Configuration file exists at: %s' % config_file)
    # do it this round-about way so as to go through paste
    import paste.deploy
    conf = paste.deploy.appconfig('config:' + config_file)
    return conf

