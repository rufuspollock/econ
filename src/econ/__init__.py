__version__ = '0.1a'

def get_config():
    """Load config file and return configobj containing that information.
    
    Config file is located using 'ECONCONF' environment variable or, if that
    does not exist, looking for a file './etc/econ.conf' (note that this path
    is taken in relation to the current directory.
    """
    import os
    import configobj
    configFilePath = os.path.abspath('./etc/econ.conf')
    if os.environ.has_key('ECONCONF'):
        configFilePath = os.environ['ECONCONF']
    config = configobj.ConfigObj(configFilePath)
    return config

conf = get_config()
