# main.py

from imports import *
from create_display import create_layout, create_widgets, create_tabs
from process_data import process_goes_data
from middleware import update_user_values, get_values
from utils import create_directories

import create_output
import config


create_directories()

# Function to get the location data
def get_location_data(file_path="static/location_data.json"):
    location_data = pd.read_json(file_path)
    return location_data

# Function to create main display
def user_display():
    widget_container = WidgetContainer().get_widgets()
    display(widget_container["tab_widget"])

    # Function to update the global widget values
    def update_global_values(change=None):

        # Get the location data
        df = get_location_data()

        # Get the selected location data
        selected_location = widget_container['location_widget'].value
        if selected_location in df['location'].values:
            location_data = df[df['location'] == selected_location].iloc[0]

        # Update the user values based on the selected widgets (user input for lat/lon)
        if widget_container['lat1_widget'].value != 0 or widget_container['lat2_widget'].value != 0:
            config.widget_values['selected_extent'] = [
                widget_container['lon1_widget'].value,
                widget_container['lon2_widget'].value,
                widget_container['lat1_widget'].value,
                widget_container['lat2_widget'].value
            ]
            config.widget_values['selected_central_latitude'] = (widget_container['lat1_widget'].value + widget_container['lat2_widget'].value) / 2
            config.widget_values['selected_central_longitude'] = (widget_container['lon1_widget'].value + widget_container['lon2_widget'].value) / 2
        else:
            config.widget_values['selected_extent'] = location_data['extent']
            config.widget_values['selected_central_latitude'] = location_data['central_latitude']
            config.widget_values['selected_central_longitude'] = location_data['central_longitude']

        # Update the user values based on the selected widgets for projection type
        if widget_container['projection_type_widget'].value != 'Autoselect':
            config.widget_values['selected_projection_type'] = widget_container['projection_type_widget'].value
            config.widget_values['selected_projection'] = location_data['projection']
        else:
            config.widget_values['selected_projection_type'] = location_data['projection']
            config.widget_values['selected_projection'] = location_data['projection']

        if widget_container['satellite_type_widget'].value != 'Autoselect':
            config.widget_values['selected_satellite_type'] = widget_container['satellite_type_widget'].value
            config.widget_values['selected_satellite'] = location_data['satellite']
        else:
            config.widget_values['selected_satellite_type'] = location_data['satellite']
            config.widget_values['selected_satellite'] = location_data['satellite']

        if widget_container['domain_type_widget'].value != 'Autoselect':
            config.widget_values['selected_domain_type'] = widget_container['domain_type_widget'].value
            config.widget_values['selected_domain'] = location_data['domain']
        else:
            config.widget_values['selected_domain_type'] = location_data['domain']
            config.widget_values['selected_domain'] = location_data['domain']

        if widget_container['upload_json_widget'].value:
            config.widget_values['selected_json_file'] = True
        else:
            config.widget_values['selected_json_file'] = False

        if widget_container['border_color_widget'].value != 'orange':
            config.widget_values['selected_border_color'] = widget_container['border_color_widget'].value
        
        if widget_container['border_width_widget'].value != 0.4:
            config.widget_values['selected_border_width'] = widget_container['border_width_widget'].value

        # Update the user values based on the selected widgets
        config.widget_values['selected_location'] = widget_container['location_widget'].value
        config.widget_values['selected_domain'] = location_data['domain']
        config.widget_values['selected_rgb'] = widget_container['rgb_widget'].value
        config.widget_values['selected_start_time'] = widget_container['start_time_widget'].value
        config.widget_values['selected_end_time'] = widget_container['end_time_widget'].value
        config.widget_values['selected_cpus'] = widget_container['cpu_widget'].value
        config.widget_values['selected_border_color'] = widget_container['border_color_widget'].value
        config.widget_values['selected_border_width'] = widget_container['border_width_widget'].value
        config.widget_values['selected_lat_lon_lines'] = widget_container['lat_lon_lines_widget'].value
        config.widget_values['selected_lat_lon_labels'] = widget_container['lat_lon_labels_widget'].value
        config.widget_values['selected_state_border'] = widget_container['state_border_widget'].value
        config.widget_values['selected_country_border'] = widget_container['country_border_widget'].value
        config.widget_values['selected_lake_border'] = widget_container['lake_border_widget'].value
        config.widget_values['selected_county_border'] = widget_container['county_border_widget'].value
        config.widget_values['selected_lat1'] = widget_container['lat1_widget'].value
        config.widget_values['selected_lat2'] = widget_container['lat2_widget'].value
        config.widget_values['selected_lon1'] = widget_container['lon1_widget'].value
        config.widget_values['selected_lon2'] = widget_container['lon2_widget'].value

    # Attach handlers to update global state when widgets change
    for widget_name, widget in widget_container.items():
        widget.observe(update_global_values, 'value')

    # Update the state once to capture initial values
    update_global_values()

    return widget_container

def handle_data(display):
    json_file = display['upload_json_widget']

    if json_file.value:
        file_content = json_file.value[0]['content'].tobytes()
        json_string = file_content.decode('utf-8')
        json_values = json.loads(json_string)
        config.widget_values['selected_json_file'] = True
        values = json_values
    else:
        values = update_user_values(WidgetContainer(), get_location_data())
        config.widget_values['selected_json_file'] = False

    ds = process_goes_data(**values)
    create_product(ds)

# Function to create the product output display
def create_product(ds):
    create_output.create_widgets(ds)


# Define the class function to initialize the widgets and return values
class WidgetContainer:
    def __init__(self):
        self.tab_widget, widgets_list = create_tabs(get_location_data)
        (self.rgb_widget, self.cpu_widget, self.location_widget, self.start_time_widget,
         self.end_time_widget, self.lat_lon_lines_widget, self.lat_lon_labels_widget,
         self.state_border_widget, self.country_border_widget,
         self.lake_border_widget, self.county_border_widget, self.border_color_widget,
         self.border_width_widget, self.projection_type_widget, self.satellite_type_widget, self.domain_type_widget,
         self.lat1_widget, self.lat2_widget, self.lon1_widget, self.lon2_widget,
         self.upload_json_widget, self.export_json_widget, self.delete_data_widget, self.delete_media_widget) = widgets_list

    # Function to get the widgets
    def get_widgets(self):
        return {
            "tab_widget": self.tab_widget,
            "rgb_widget": self.rgb_widget,
            "cpu_widget": self.cpu_widget,
            "location_widget": self.location_widget,
            "start_time_widget": self.start_time_widget,
            "end_time_widget": self.end_time_widget,
            "lat_lon_lines_widget": self.lat_lon_lines_widget,
            "lat_lon_labels_widget": self.lat_lon_labels_widget,
            "state_border_widget": self.state_border_widget,
            "country_border_widget": self.country_border_widget,
            "lake_border_widget": self.lake_border_widget,
            "county_border_widget": self.county_border_widget,
            "border_color_widget": self.border_color_widget,
            "border_width_widget": self.border_width_widget,
            "projection_type_widget": self.projection_type_widget,
            "satellite_type_widget": self.satellite_type_widget,
            "domain_type_widget": self.domain_type_widget,
            "lat1_widget": self.lat1_widget,
            "lat2_widget": self.lat2_widget,
            "lon1_widget": self.lon1_widget,
            "lon2_widget": self.lon2_widget,
            "upload_json_widget": self.upload_json_widget,
            "export_json_widget": self.export_json_widget,
            "delete_data_widget": self.delete_data_widget,
            "delete_media_widget": self.delete_media_widget
        }
