# middleware.py

from imports import *

# Get the list of widgets to be displayed on the page
def get_widgets():
    return ['rgb_widget', 'cpu_widget', 'location_widget', 'start_time_widget',
            'end_time_widget', 'lat_lon_lines_widget', 'lat_lon_labels_widget',
            'state_border_widget', 'country_border_widget',
            'lake_border_widget', 'county_border_widget', 'border_color_widget',
            'border_width_widget', 'projection_type_widget', 'satellite_type_widget', 'domain_type_widget',
            'lat1_widget', 'lat2_widget', 'lon1_widget', 'lon2_widget', 'upload_json_widget', 'export_json_widget',
            'delete_data_widget', 'delete_media_widget']

# Set the default values for the widgets
def get_values():
    values = {
        "selected_location": "default_location",
        "selected_extent": "default_extent",
        "selected_satellite": "default_satellite",
        "selected_domain": "default_domain",
        "selected_projection": "default_projection",
        "selected_rgb": "default_rgb",
        "selected_start_time": "default_start_time",
        "selected_end_time": "default_end_time",
        "selected_cpus": "default_cpus",
        "selected_border_color": "default_border_color",
        "selected_border_width": "default_border_width",
        "selected_lat_lon_lines": "default_lat_lon_lines",
        "selected_lat_lon_labels": "default_lat_lon_labels",
        "selected_state_border": "default_state_border",
        "selected_country_border": "default_country_border",
        "selected_lake_border": "default_lake_border",
        "selected_county_border": "default_county_border",
        "selected_projection_type": "default_projection_type",
        "selected_satellite_type": "default_satellite_type",
        "selected_domain_type": "default_domain_type",
        "selected_lat1": "default_lat1",
        "selected_lat2": "default_lat2",
        "selected_lon1": "default_lon1",
        "selected_lon2": "default_lon2",
        "selected_json_file": "default_uploaded_json",
    }
    return values

# Update the user values based on the selected widgets
def update_user_values(widget_container, df):

    selected_location = widget_container.get_widgets()["location_widget"].value

    # Ensure that the selected_location exists in the dataframe
    if selected_location in df['location'].values:
        location_data = df[df['location'] == selected_location].iloc[0]

        user_values = get_values()

        user_values.update({
            "selected_location": selected_location,
            "selected_extent": location_data['extent'],
            "selected_satellite": location_data['satellite'],
            "selected_domain": location_data['domain'],
            "selected_projection": location_data['projection'],
            "selected_rgb": widget_container.get_widgets()["rgb_widget"].value,
            "selected_start_time": widget_container.get_widgets()["start_time_widget"].value,
            "selected_end_time": widget_container.get_widgets()["end_time_widget"].value,
            "selected_cpus": widget_container.get_widgets()["cpu_widget"].value,
            "selected_border_color": widget_container.get_widgets()["border_color_widget"].value,
            "selected_border_width": widget_container.get_widgets()["border_width_widget"].value,
            "selected_lat_lon_lines": widget_container.get_widgets()["lat_lon_lines_widget"].value,
            "selected_lat_lon_labels": widget_container.get_widgets()["lat_lon_labels_widget"].value,
            "selected_state_border": widget_container.get_widgets()["state_border_widget"].value,
            "selected_country_border": widget_container.get_widgets()["country_border_widget"].value,
            "selected_lake_border": widget_container.get_widgets()["lake_border_widget"].value,
            "selected_county_border": widget_container.get_widgets()["county_border_widget"].value,
            "selected_projection_type": widget_container.get_widgets()["projection_type_widget"].value,
            "selected_satellite_type": widget_container.get_widgets()["satellite_type_widget"].value,
            "selected_domain_type": widget_container.get_widgets()["domain_type_widget"].value,
            "selected_central_latitude": location_data['central_latitude'],
            "selected_central_longitude": location_data['central_longitude'],
            "selected_lat1": widget_container.get_widgets()["lat1_widget"].value,
            "selected_lat2": widget_container.get_widgets()["lat2_widget"].value,
            "selected_lon1": widget_container.get_widgets()["lon1_widget"].value,
            "selected_lon2": widget_container.get_widgets()["lon2_widget"].value,
            "selected_json_file": widget_container.get_widgets()["upload_json_widget"].value
        })

    return user_values


# Get the RGB function based on the selected RGB type
def get_rgb(selected_rgb):

    # Define RGB functions and their parameters
    rgb_options = {
        'Air Mass (Normal)': ('AirMass', {}),
        'Air Mass (Tropical)': ('AirMassTropical', {}),
        'Ash': ('Ash', {}),
        'Cloud Convection (Day)': ('DayCloudConvection', {}),
        'Cloud Phase (Day)': ('DayCloudPhase', {}),
        'Convection (Day)': ('DayConvection', {}),
        'Dust': ('Dust', {}),
        'Fire Detection Land Cloud (Day)': ('DayLandCloudFire', {}),
        'Fire Temperature': ('FireTemperature', {}),
        'Land Cloud (Day)': ('DayLandCloud', {}),
        'Natural Color (Day) + IR (Night)': ('NaturalColor', {'gamma': 1.2, 'pseudoGreen': True, 'night_IR': True}),
        'Night Fog (Differential)': ('NightFogDifference', {}),
        'Nighttime Microphysics': ('NighttimeMicrophysics', {}),
        'Rocket Plume': ('RocketPlume', {'night': True}),
        'Sea Spray': ('SeaSpray', {}),
        'Sulfur Dioxide': ('SulfurDioxide', {}),
        'Snow and Fog (Day)': ('DaySnowFog', {}),
        'Water Vapor (Differential)': ('DifferentialWaterVapor', {}),
    }

    # Default to 'NaturalColor'
    return rgb_options.get(selected_rgb, ('NaturalColor', {'gamma': 1.2, 'pseudoGreen': True, 'night_IR': True}))

# Get the projection based on the selected projection type
def get_projection(selected_projection, central_lat=None, central_lon=None):
    projection_options = {
        'LambertConformal': ccrs.LambertConformal(),
        'LambertCylindrical': ccrs.LambertCylindrical(),
        'LambertAzimuthalEqualArea': ccrs.LambertAzimuthalEqualArea(central_latitude=central_lat, central_longitude=central_lon),
        'Mercator': ccrs.Mercator(),
        'Miller': ccrs.Miller(),
        'Mollweide': ccrs.Mollweide(),
        'Orthographic': ccrs.Orthographic(central_latitude=central_lat, central_longitude=central_lon),
        'PlateCarree': ccrs.PlateCarree(),
        'TransverseMercator': ccrs.TransverseMercator(central_latitude=central_lat, central_longitude=central_lon),
        'Robinson': ccrs.Robinson(),
        'Sinusoidal': ccrs.Sinusoidal(central_longitude=central_lon),
        'StereoGraphic': ccrs.Stereographic(central_latitude=central_lat, central_longitude=central_lon),
        'AlbersEqualArea': ccrs.AlbersEqualArea(central_latitude=central_lat, central_longitude=central_lon),
        'AzimuthalEquidistant': ccrs.AzimuthalEquidistant(central_latitude=central_lat, central_longitude=central_lon),
        'EquidistantConic': ccrs.EquidistantConic(central_latitude=central_lat, central_longitude=central_lon),

    }

    # Default to 'Plate Carree'
    return projection_options.get(selected_projection, ccrs.PlateCarree())
