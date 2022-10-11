import yaml
from yaml.loader import SafeLoader

CONFIG_PATH = "../config.yml"

def read_config():
    # Open the file and load the file
    with open(CONFIG_PATH) as f:
        data = yaml.load(f, Loader=SafeLoader)

    return data

def list_images():
