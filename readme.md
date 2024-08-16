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
Use `conda env create -f environment.yml` to create an environment called `sat_viewer`

## Installation through PIP
From command line, navigate to the root directory of sat_viewer where `requirements.txt` file exists.
Use `pip install -r requirements.txt` under the current environment the user has selected.

## Installation of Jupyter Notebook/JupyterLab
After downloading and installing Anaconda, the user can install JupyterLabs or Jupyter Notebook through
the `Anaconda Navigator` app. Ensure the proper environment is selected at the top `Applications on`.

![Image of Anaconda Navigator app and dependencies that can be installed.](https://i.imgur.com/U9brEFs.png)