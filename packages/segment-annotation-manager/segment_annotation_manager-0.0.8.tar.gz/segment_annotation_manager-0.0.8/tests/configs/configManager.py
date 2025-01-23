from YOLOv8.model.config import Config
import yaml
import os

# def create_comparison_configs():





config_dir = os.getcwd()
batch_dir = os.path.join(config_dir, 'batch')

base_config_path = os.path.join(config_dir, 'baseConfig.yaml')
base_config = yaml.load(open(base_config_path), yaml.Loader)

base_keys = list(base_config.keys())
print(base_keys)
