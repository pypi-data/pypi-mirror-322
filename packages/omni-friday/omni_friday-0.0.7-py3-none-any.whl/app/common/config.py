import os
import yaml

CONFIG_FILE_NAME = 'project.settings.yml'

def get_project_settings():
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        settings = yaml.safe_load(file)
    
    return settings