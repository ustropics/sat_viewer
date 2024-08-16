# create_display.py

from imports import *
from utils import unpack_widgets, save_params_to_json

import config

# Function to export the JSON file
def export_json_function(button):
    file_path = config.json_dir + 'GOES_viewer_params.json'

    params = {key: config.widget_values[key] for key in config.widget_values}

    save_params_to_json(file_path, **params)

def delete_data_function(button):
    data_dir = config.data_dir
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print(f"Directory {data_dir} and all its contents have been deleted.")

def delete_media_function(button):
    img_dir = config.img_dir
    media_dir = config.media_dir
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
        print(f"Directory {img_dir} and all its contents have been deleted.")
    if os.path.exists(media_dir):
        shutil.rmtree(media_dir)
        print(f"Directory {media_dir} and all its contents have been deleted.")

# Function to create the widgets
def create_widgets(get_location_data_func):
    location_df = get_location_data_func()

    current_time_naive = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0, tzinfo=None)

    previous_time_naive = current_time_naive - dt.timedelta(minutes=30)

    rgb_widget = widgets.Select(
        options=['Air Mass (Normal)', 'Air Mass (Tropical)', 'Ash', 'Cloud Convection (Day)','Cloud Phase (Day)', 'Convection (Day)', 
                 'Dust', 'Fire Detection Land Cloud (Day)', 'Fire Temperature', 'Land Cloud (Day)', 'Natural Color (Day) + IR (Night)', 
                 'Night Fog (Differential)', 'Nighttime Microphysics','Rocket Plume', 'Sea Spray', 'Snow and Fog (Day)',
                 'Sulfur Dioxide', 'Water Vapor (Differential)'],
        value='Natural Color (Day) + IR (Night)',
        description='RGB Product',
        rows=12
    )

    cpu_widget = widgets.IntSlider(
        value=1,
        min=1,
        max=12,
        step=1,
        description='Max CPUs',
        disabled=False,
        continuous_update=False,
        style={'description_width': 'initial'}
    )

    dropdown_options = location_df['location'].tolist()
    location_widget = widgets.Dropdown(
        options=dropdown_options,
        value=dropdown_options[0],
        description='Location'
    )

    start_time_widget = widgets.NaiveDatetimePicker(
        description='Start Time',
        value=previous_time_naive
    )

    end_time_widget = widgets.NaiveDatetimePicker(
        description='End Time', value=current_time_naive)

    border_color_widget = widgets.ColorPicker(
        concise=False,
        description='Border Color',
        value='orange',
        disabled=False
    )

    border_width_widget = widgets.BoundedFloatText(
        value=0.4,
        min=0,
        max=10.0,
        step=0.1,
        description='Border Width',
        disabled=False
    )

    lat_lon_lines_widget = widgets.Checkbox(
        value=True,
        description='Lat/Lon Lines',
        disabled=False,
        indent=False
    )

    lat_lon_labels_widget = widgets.Checkbox(
        value=True,
        description='Lat/Lon Labels',
        disabled=False,
        indent=False
    )

    country_border_widget = widgets.Checkbox(
        value=True,
        description='Country Borders',
        disabled=False,
        indent=False
    )

    state_border_widget = widgets.Checkbox(
        value=True,
        description='State Borders',
        disabled=False,
        indent=False
    )

    lake_border_widget = widgets.Checkbox(
        value=True,
        description='Lake/River Borders',
        disabled=False,
        indent=False
    )

    county_border_widget = widgets.Checkbox(
        value=False,
        description='County Borders',
        disabled=True,
        indent=False
    )

    projection_type_widget = widgets.Select(
        options=['Autoselect', 'AlbersEqualArea', 'AzimuthalEquidistant', 'EquidistantConic',
                'LambertConformal', 'LambertCylindrical', 'LambertAzimuthalEqualArea', 'Mercator', 'Miller', 'Mollweide',
                'Orthographic', 'PlateCarree', 'Robinson', 'Sinusoidal', 'StereoGraphic',
                'TransverseMercator'],
        value='Autoselect',
        description='Projection',
        rows=8
    )

    satellite_type_widget = widgets.Dropdown(
        options=['Autoselect', 'GOES-East (16)', 'GOES-West (18)', 'GOES-West (17)'],
        value='Autoselect',
        description='Satellite',
        rows=4
    )

    domain_type_widget = widgets.Dropdown(
        options=['Autoselect', 'CONUS', 'Full Disk','Mesoscale'],
        value='Autoselect',
        description='Domain',
        rows=4
    )

    lat1_widget = widgets.BoundedFloatText(
        min=-90,
        max=90,
        step=1,
        description='North Lat',
        disabled=False
    )

    lat2_widget = widgets.BoundedFloatText(
        min=-90,
        max=90,
        step=1,
        description='South Lat',
        disabled=False
    )

    lon1_widget = widgets.BoundedFloatText(
        min=-360,
        max=360,
        step=1,
        description='West Lon',
        disabled=False
    )

    lon2_widget = widgets.BoundedFloatText(
        min=-360,
        max=360,
        step=1,
        description='East Lon',
        disabled=False
    )

    upload_json_widget = widgets.FileUpload(
        accept='.json',
        multiple=False
    )

    export_json_widget = widgets.Button(
        description='Export JSON',
        disabled=False,
        button_style='info',
        tooltip='Export JSON file.',
        icon='download'
    )

    delete_data_widget = widgets.Button(
        description='Delete Data Files',
        disabled=False,
        button_style='',
        tooltip='Permanently delete all data files.',
        icon='file'
    )

    delete_media_widget = widgets.Button(
        description='Delete Image Files',
        disabled=False,
        button_style='danger',
        tooltip='Permanently delete all image and media files.',
        icon='image'
    )

    export_json_widget.on_click(export_json_function)
    delete_data_widget.on_click(delete_data_function)
    delete_media_widget.on_click(delete_media_function)

    return [rgb_widget, cpu_widget, location_widget, start_time_widget,
            end_time_widget, lat_lon_lines_widget, lat_lon_labels_widget,
            state_border_widget, country_border_widget, lake_border_widget, county_border_widget, border_color_widget,
            border_width_widget, projection_type_widget, satellite_type_widget, domain_type_widget,
            lat1_widget, lat2_widget, lon1_widget, lon2_widget, upload_json_widget, export_json_widget,
            delete_data_widget, delete_media_widget]


def create_tabs(get_location_data_func):
    widgets_list = create_widgets(get_location_data_func)
    widgets_dict = unpack_widgets(widgets_list)

    label_settings1 = widgets.Label(
        value="Select the projection, satellite, and domain type.",
        layout=Layout(margin='0px 0px 0px 0px')
    )
    
    label_settings2 = widgets.Label(
        value="Set custom latitude and longitude extent box.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    label_settings3 = widgets.Label(
        value="Select border color and width.",
        layout=Layout(margin='10px 0px 0px 0px')
    )

    label_settings4 = widgets.Label(
        value="Select which overlays to display.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    label_main1 = widgets.Label(
        value="Quickly select a product type and preset location.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    label_main2 = widgets.Label(
        value="Set start and ending times (values are in UTC).",
        layout=Layout(margin='0px 0px 0px 25px')
    )

    label_utilities1 = widgets.Label(
        value="Upload/Export a json file with parameters.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    label_utilities2 = widgets.Label(
        value="Set the number of CPUs to use.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    label_utilities3 = widgets.Label(
        value="Delete data or media files.",
        layout=Layout(margin='0px 0px 0px 0px')
    )

    vbox_main1 = widgets.VBox(
        [label_main1, widgets_dict['rgb_widget'], widgets_dict['location_widget']])

    vbox_main2 = widgets.VBox(
        [label_main2, widgets_dict['start_time_widget'], widgets_dict['end_time_widget']], layout=Layout(margin='0px 0px 0px 20px'))

    vbox_settings1 = widgets.VBox(
        [label_settings1, widgets_dict['projection_type_widget'], widgets_dict['satellite_type_widget'], widgets_dict['domain_type_widget']])
    
    vbox_settings2 = widgets.VBox([
        label_settings2, widgets_dict['lat1_widget'], widgets_dict['lat2_widget'], widgets_dict['lon1_widget'], widgets_dict['lon2_widget'], 
        label_settings3, widgets_dict['border_color_widget'], widgets_dict['border_width_widget']], layout=Layout(margin='0px 0px 0px 20px'))

    vbox_settings3 = widgets.VBox([
        label_settings4, widgets_dict['lat_lon_lines_widget'], widgets_dict['lat_lon_labels_widget'], widgets_dict['state_border_widget'], 
        widgets_dict['country_border_widget'], widgets_dict['lake_border_widget'], widgets_dict['county_border_widget']], layout=Layout(margin='0px 0px 20px 20px'))

    vbox_utilities1 = widgets.VBox(
        [label_utilities1, widgets_dict['upload_json_widget'], widgets_dict['export_json_widget']])

    vbox_utilities2 = widgets.VBox([label_utilities2, widgets_dict['cpu_widget']], layout=Layout(margin='0px 0px 0px 20px'))

    vbox_utilities3 = widgets.VBox([label_utilities3, widgets_dict['delete_data_widget'], widgets_dict['delete_media_widget']], layout=Layout(margin='0px 0px 0px 20px'))

    hbox1 = widgets.HBox([vbox_main1, vbox_main2])
    hbox2 = widgets.HBox([vbox_settings1, vbox_settings2, vbox_settings3])
    hbox3 = widgets.HBox([vbox_utilities1, vbox_utilities2, vbox_utilities3])

    tab_contents = [hbox1, hbox2, hbox3]

    tab_widget = widgets.Tab(children=tab_contents)
    tab_widget.set_title(0, 'Main Parameters')
    tab_widget.set_title(1, 'Projection Settings')
    tab_widget.set_title(2, 'Utilities')

    return tab_widget, widgets_list


def create_layout(get_data_frame_func):
    widgets_list = create_widgets(get_data_frame_func)
    widgets_dict = unpack_widgets(widgets_list)

    return (widgets_dict['rgb_widget'], widgets_dict['cpu_widget'], widgets_dict['location_widget'], widgets_dict['start_time_widget'],
            widgets_dict['end_time_widget'], widgets_dict['lat_lon_lines_widget'], widgets_dict['lat_lon_labels_widget'],
            widgets_dict['state_border_widget'], widgets_dict['country_border_widget'],
            widgets_dict['lake_border_widget'], widgets_dict['county_border_widget'], widgets_dict['border_color_widget'],
            widgets_dict['border_width_widget'], widgets_dict['projection_type_widget'], widgets_dict['satellite_type_widget'], widgets_dict['domain_type_widget'],
            widgets_dict['lat1_widget'], widgets_dict['lat2_widget'], widgets_dict['lon1_widget'], widgets_dict['lon2_widget'],
            widgets_dict['upload_json_widget'], widgets_dict['export_json_widget'], widgets_dict['delete_data_widget'], widgets_dict['delete_media_widget'])
