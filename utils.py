# utils.py

from imports import *
from middleware import get_widgets
import config


def unpack_widgets(widgets_list):
    widget_names = get_widgets()
    widget_dict = dict(zip(widget_names, widgets_list))
    return widget_dict

# Save and load parameters to/from a JSON file
def save_params_to_json(json_filename, **kwargs):
    def convert_value(value):
        if isinstance(value, (np.int64, np.int32, np.int16, np.int8)):
            return int(value)
        elif isinstance(value, (np.float64, np.float32)):
            return float(value)
        elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
            return str(value)
        elif isinstance(value, (datetime, pd.Timestamp)):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (list, tuple)):
            return [convert_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: convert_value(v) for k, v in value.items()}
        else:
            return value

    converted_kwargs = {k: convert_value(v) for k, v in kwargs.items()}

    with open(json_filename, 'w') as f:
        json.dump(converted_kwargs, f, indent=4)
        user_values = config.widget_values
        print("Widget values", config.widget_values['lat1_widget'])

# Load parameters from a JSON file
def load_params_from_json(json_filename):
    with open(json_filename, 'r') as f:
        params = json.load(f)
    return params

def create_directories():
    # List of directories to check and create
    directories = [
        config.img_dir,
        config.data_dir,
        config.json_dir,
        config.media_dir
    ]
    
    # Iterate through each directory
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
