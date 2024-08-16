# plot_data.py

from imports import *
from acgc import figstyle

import config


def plot_timestep(ds, i, projection, selected_extent, selected_border_color, selected_border_width,
                  selected_lat_lon_lines, selected_lat_lon_labels, selected_state_border, selected_country_border,
                  selelected_projection_type, selected_satellite_type, selected_domain_type,
                  selected_lake_border, selected_county_border, rgb_name, rgb_params, selected_satellite,
                  selected_rgb, selected_location_title, save_dir, filename):

    if selected_satellite_type == 'GOES-East (16)':
        selected_satellite = 16
    elif selected_satellite_type == 'GOES-West (17)':
        selected_satellite = 17
    elif selected_satellite_type == 'GOES-West (18)':
        selected_satellite = 18

    if selected_domain_type == 'CONUS':
        selected_domain = 'C'
    if selected_domain_type == 'Full Disk':
        selected_domain = 'F'
    if selected_domain_type == 'Mesoscale':
        selected_domain = 'M'

    # Define the path for the output image
    output_path = os.path.join(save_dir, f'{filename}.png')

    # Check if the image already exists
    if os.path.isfile(output_path):
        print(f"Image already exists for timestep {i}: {output_path}")
        return

    # Create a figure and axis with the desired projection
    fig = plt.figure(figsize=(15, 15))
    ax = plt.subplot(projection=projection)
    # Set the extent of the plot
    ax.set_extent(selected_extent, crs=ccrs.PlateCarree())

    # Get the RGB data and imshow kwargs
    imshow_kwargs = ds.isel(t=i).rgb.imshow_kwargs
    imshow_kwargs.pop('transform', None)

    # Get the RGB data and plot it
    rgb_callable = getattr(ds.isel(t=i).rgb, rgb_name)
    img_data = rgb_callable(**rgb_params)
    if img_data is None:
        print(f"RGB data is None for timestep {i}, skipping...")
        return

    ax.imshow(img_data, transform=ds.isel(t=i).rgb.crs, **imshow_kwargs)

    # Add map features
    states = cfeature.NaturalEarthFeature(
        category='cultural', name='admin_1_states_provinces_lines', scale='50m',
        edgecolor=selected_border_color, facecolor='none', linewidth=selected_border_width
    )

    countries = cfeature.NaturalEarthFeature(
        category='cultural', name='admin_0_countries', scale='50m',
        edgecolor=selected_border_color, facecolor='none', linewidth=selected_border_width
    )

    lakes = cfeature.NaturalEarthFeature(
        category='physical', name='lakes', scale='50m',
        edgecolor=selected_border_color, facecolor='none', linewidth=selected_border_width
    )

    # Add map features to the plot based on user selection
    if selected_state_border:
        ax.add_feature(states)
    if selected_country_border:
        ax.add_feature(countries)
    if selected_lake_border:
        ax.add_feature(lakes)

    # Add latitude and longitude lines and labels
    gl = ax.gridlines(draw_labels=selected_lat_lon_labels,
                      linestyle='--', color='gray')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlines = selected_lat_lon_lines
    gl.ylines = selected_lat_lon_lines
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()
    gl.xlabel_style = {'size': 12, 'color': 'black'}
    gl.ylabel_style = {'size': 12, 'color': 'black'}

    # Add title and timestamp to the plot
    ax.set_title(
        f'GOES-{selected_satellite} {selected_rgb} - {selected_location_title}')
    timestamp = pd.to_datetime(
        ds.isel(t=i).t.values).strftime('%Y-%m-%d %H:%M UTC')
    ax.text(0.92, 1.008, timestamp, transform=ax.transAxes,
            ha='center', va='bottom', fontsize=12)

    # Save the figure
    print(f"Saving figure for timestep {i} to {output_path}...")
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
