# process_data.py

from imports import *
from middleware import get_rgb, get_projection
from utils import save_params_to_json
from plot_data import plot_timestep

import config

# Define a variable to hold hashed filenames
_hashed_filenames = []
data_dir = config.data_dir
save_dir = config.img_dir

# Main processing function to fetch and process the GOES data
def process_goes_data(selected_location, selected_extent, selected_satellite,
                      selected_domain, selected_projection, selected_rgb, selected_start_time,
                      selected_end_time, selected_cpus, selected_border_color, selected_border_width,
                      selected_lat_lon_lines, selected_lat_lon_labels,
                      selected_state_border, selected_country_border, selected_lake_border, selected_county_border,
                      selected_projection_type, selected_satellite_type, selected_domain_type, selected_central_latitude, selected_central_longitude,
                      selected_lat1, selected_lat2, selected_lon1, selected_lon2, selected_json_file):
    
    if config.widget_values['selected_json_file'] == False:    
        selected_location = config.widget_values['selected_location']
        selected_extent = config.widget_values['selected_extent']
        selected_satellite = config.widget_values['selected_satellite']
        selected_domain = config.widget_values['selected_domain']
        selected_projection = config.widget_values['selected_projection']
        selected_rgb = config.widget_values['selected_rgb']
        selected_start_time = config.widget_values['selected_start_time']
        selected_end_time = config.widget_values['selected_end_time']
        selected_cpus = config.widget_values['selected_cpus']
        selected_border_color = config.widget_values['selected_border_color']
        selected_border_width = config.widget_values['selected_border_width']
        selected_lat_lon_lines = config.widget_values['selected_lat_lon_lines']
        selected_lat_lon_labels = config.widget_values['selected_lat_lon_labels']
        selected_state_border = config.widget_values['selected_state_border']
        selected_country_border = config.widget_values['selected_country_border']
        selected_lake_border = config.widget_values['selected_lake_border']
        selected_county_border = config.widget_values['selected_county_border']
        selected_projection_type = config.widget_values['selected_projection_type']
        selected_satellite_type = config.widget_values['selected_satellite_type']
        selected_domain_type = config.widget_values['selected_domain_type']
        selected_central_latitude = config.widget_values['selected_central_latitude']
        selected_central_longitude = config.widget_values['selected_central_longitude']
        selected_lat1 = config.widget_values['selected_lat1']
        selected_lat2 = config.widget_values['selected_lat2']
        selected_lon1 = config.widget_values['selected_lon1']
        selected_lon2 = config.widget_values['selected_lon2']
        selected_json_file = config.widget_values['selected_json_file']


    # Check if a custom extent was selected
    if config.widget_values['selected_lat1'] != 0 or config.widget_values['selected_lat2'] != 0:
        selected_extent = [
            config.widget_values['selected_lon1'],
            config.widget_values['selected_lon2'],
            config.widget_values['selected_lat1'],
            config.widget_values['selected_lat2']
        ]
        selected_location_title = f'Custom Extent'
        selected_central_latitude = (config.widget_values['selected_lat1'] + config.widget_values['selected_lat2']) / 2
        selected_central_longitude = (config.widget_values['selected_lon1'] + config.widget_values['selected_lon2']) / 2

        if config.widget_values['selected_lon2'] > -65 or config.widget_values['selected_lon1'] < -110:
            selected_domain = 'F'
            print("Domain changed to Full Disk.")
        else:
            selected_domain = 'C'
            print("Domain changed to CONUS.")

        if config.widget_values['selected_lon1'] > -100:
            print("Satellite changed to GOES-East (16).")
            selected_satellite = 16
        else:
            print("Satellite changed to GOES-West (18).")
            selected_satellite = 18

    if selected_domain_type == 'CONUS':
        selected_domain = 'C'
    if selected_domain_type == 'Full Disk':
        selected_domain = 'F'
    if selected_domain_type == 'Mesoscale':
        selected_domain = 'M'

    if selected_satellite_type == 'GOES-East (16)':
        selected_satellite = 16
    elif selected_satellite_type == 'GOES-West (17)':
        selected_satellite = 17
    elif selected_satellite_type == 'GOES-West (18)':
        selected_satellite = 18
        


    elif selected_lat1 != 0 or selected_lat2 != 0:
        selected_extent = [selected_lon1, selected_lon2, selected_lat1, selected_lat2]
        selected_location_title = f'Custom Extent'
    else:
        selected_location_title = selected_location

    def fetch_data(start_time, end_time):
        selected_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        selected_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Attempt to fetch the GOES data
            G = GOES(satellite=int(selected_satellite),
                     product="ABI-L2-MCMIP",
                     domain=selected_domain).timerange(
                start=selected_start_time,
                end=selected_end_time,
                return_as='filelist',
                save_dir=data_dir
            )

            file_paths = [os.path.join(data_dir, f)
                          for f in G['file'].to_list()]
            ds = xr.open_mfdataset(file_paths, concat_dim='t',
                                   combine='nested')

        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            print("Attempting to adjust the time range...")

            # Adjust time range and try again
            start_time = pd.Timestamp.now(tz='UTC') - pd.Timedelta('35 minutes')
            end_time = pd.Timestamp.now(tz='UTC') - pd.Timedelta('5 minutes')

            selected_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
            selected_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

            # Retry fetching data with adjusted time range
            G = GOES(satellite=int(selected_satellite),
                     product="ABI-L2-MCMIP",
                     domain=selected_domain).timerange(
                start=selected_start_time,
                end=selected_end_time,
                return_as='filelist',
                save_dir=data_dir
            )

            file_paths = [os.path.join(data_dir, f)
                          for f in G['file'].to_list()]
            ds = xr.open_mfdataset(file_paths, concat_dim='t',
                                   combine='nested')

        filenames = [os.path.basename(path) for path in file_paths]
        filenames_array = np.array(filenames)

        appended_filenames = [
            f"{filename}_{selected_location}_{selected_extent}_"
            f"{selected_satellite}_{selected_domain}_"
            f"{selected_projection}_{selected_rgb}_"
            f"{selected_border_color}_{selected_border_width}_"
            f"{selected_lat_lon_lines}_{selected_lat_lon_labels}_"
            f"{selected_state_border}_{selected_country_border}_"
            f"{selected_lake_border}_{selected_county_border}_"
            f"{selected_projection_type}_{selected_satellite_type}_{selected_domain_type}_"
            f"{selected_central_latitude}_{selected_central_longitude}_"
            f"{selected_lat1}_{selected_lat2}_{selected_lon1}_{selected_lon2}"
            for filename in filenames_array
        ]

        hashed_filenames = [
            hashlib.md5(f.encode()).hexdigest() for f in appended_filenames
        ]

        # Update the global variable with the hashed filenames
        global _hashed_filenames
        _hashed_filenames = hashed_filenames

        return ds, hashed_filenames

    rgb_name, rgb_params = get_rgb(selected_rgb)

    if selected_start_time is None:
        start_time = pd.Timestamp.now(tz='UTC') - pd.Timedelta('30 minutes')
        end_time = pd.Timestamp.now(tz='UTC')
    else:
        start_time = pd.Timestamp(selected_start_time)
        end_time = pd.Timestamp(selected_end_time)

    ds, hashed_filenames = fetch_data(start_time, end_time)
    projection = get_projection(
        selected_projection_type, central_lat=selected_central_latitude, central_lon=selected_central_longitude)

    for i, filename in enumerate(hashed_filenames):
        plot_timestep(ds, i, projection, selected_extent, selected_border_color, selected_border_width,
                      selected_lat_lon_lines, selected_lat_lon_labels, selected_state_border, selected_country_border,
                      selected_projection_type, selected_satellite_type, selected_domain_type,
                      selected_lake_border, selected_county_border, rgb_name, rgb_params, selected_satellite,
                      selected_rgb, selected_location_title, save_dir, filename)

    return ds


# Function to get the hashed filenames
def get_hashed_filenames():
    return _hashed_filenames
