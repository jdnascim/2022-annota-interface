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

def list_images():
    config = read_config()

    dataset_path = config["dataset_path"]

    images = os.listdir(dataset_path)

    return images[:10]
