Future workflow and content updates will be included here.

# Installation Guide

It's recommended to install Anaconda for this project with the Jupyter Notebook or JupyterLab extension.
https://www.anaconda.com/download

## Requirements
Once Anaconda has been installed, it's recommended to create a new environment. Beyond the above requirements,
Python and the below Python modules/libraries are required to run this program:

  - goes2go
  - matplotlib
  - cartopy
  - xarray
  - ipykernel
  - ipywidgets
  - moviepy
  - dask
  - acgc

## Installalation through Conda environment
There are various ways to quickly install this program and its dependencies:

From command line, navigate to the root directory of sat_viewer where the `environment.yml` file exists.
Use `conda env create -f environment.yml` to create an environment called `sat_viewer`.

## Installation through PIP
From command line, navigate to the root directory of sat_viewer where `requirements.txt` file exists.
Use `pip install -r requirements.txt` under the current environment the user has selected.

## Installation of Jupyter Notebook/JupyterLab
After downloading and installing Anaconda, the user can install JupyterLabs or Jupyter Notebook through
the `Anaconda Navigator` app. Ensure the proper environment (i.e., `sat_viewer`) is selected at the top next to *Applications on*.

![Image of Anaconda Navigator app and dependencies that can be installed.](https://i.imgur.com/U9brEFs.png)

# Usage Guide
Launch Jupyter Notebook or Jupyter Lab and navigate to the sat_viewer root directory in the program.
Open `program.ipynb`
![Image of Jupyter Notebook app and the root directory of sat_viewer.](https://i.imgur.com/4rlQmhB.png)

After running the first cell, the display UI should be available to select parameters:
![Image of Jupyter Notebook running the display module for sat_viewer.](https://i.imgur.com/AhMP95E.png)

After parameters have been set (default parameters are given for CONUS extent), run the second cell 
that contains `main.handle_data(display)`to initiate the program.

This will create a display output that includes a Play (Animation) widget to sequence the images.
Videos are saved in an .mp4 format. See *Output Structure* section below on saved directory.
![Image of output display for sat_viewer.](https://i.imgur.com/y1uZVRF.png)

## Main Parameters
![Image of Main Parameters for sat_viewer.](https://i.imgur.com/iatL6s7.png)
- **RGB Product** - various RGB recipes can be selected
- **Location** - Preset locations are available for all US states, Canadian providences, Mexico, Caribbean regions, and South American countries
- **Time Range** - A start and end time/date can be set to retrieve data from GOES-16, GOES-17, and GOES-18 satellite feed through AWS buckets

## Projection Settings
![Image of Projection Settings for sat_viewer.](https://i.imgur.com/x96wrlZ.png)
- **Projection** - Available projections can be applied through Cartopy library (https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html)
- **Satellite** - Available options include GOES-16 (East), GOES-18 (West), and GOES-17 (West-legacy)
- **Domain** - Available domain options from GOES includes CONUS view, Full Disk, and Mesoscale
- **Custom Lat/Lon** - Set a custom extent box for the plot 
  - (this option will overide the **Location** from the *Main Parameters*)
- **Border Color** - Color picker to change border colors for overlays
- **Border Width** - Set the border width for overlays
- **Lat/Lon Lines** - True/False to include latitude and longitude lines on plot
- **Lat/Lon Labels** - True/False to include latitude and longitude labels
- **State Borders** - True/False to include state borders
- **Country Borders** - True/False to include country borders
- **County Borders** - True/False to include county borders (currently disabled)
- **Lake/River Borders** - True/False to include lake and river outlines

## Utilities
![Image of Utilities for sat_viewer.](https://i.imgur.com/LdjCA4f.png)
- **Upload JSON** - Upload a .json file with keys and values
- **Export JSON** - Export a .json file to `output/json/`
- **Max CPUs** - Set maximum CPUs for parallel processes (currently operational for file downloads)
- **Delete Data Files** - Deletes all data files from the program
- **Delete Media FIles** - Deletes all images and media files from the program

# Output Structure
These directories will be created on first start of the program:

- **Data** - All data files are saved to `output/data/` from AWS buckets using GOES2GO
- **Images** - All created images are saved with hashed ids as image names to `output/images/`
- **JSON** - Export json files will be saved to `output/json/`
- **Media** - Videos and animated GIFs will be saved to `output/media/`