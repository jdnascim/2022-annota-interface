import yaml
import os
from yaml.loader import SafeLoader

CONFIG_PATH = "/home/app/config.yml"

def read_config():
    """
        Open and return the config file
    """ 

    with open(CONFIG_PATH) as f:
        data = yaml.load(f, Loader=SafeLoader)

    return data
