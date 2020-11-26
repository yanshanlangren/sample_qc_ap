from yaml import load
from yaml import Loader


def yaml_load(stream):
    ''' load from yaml stream and create a new python object

    @return object or None if failed
    '''
    try:
        obj = load(stream, Loader=Loader)
    except Exception, e:
        print("failed to load stream[%s]" % stream)
        obj = None
    return obj


class Config(object):
    def __init__(self):
        with open("/root/config.yaml") as config_file:
            self.config = yaml_load(config_file)

    def get_config(self):
        return self.config


global_config = Config()
