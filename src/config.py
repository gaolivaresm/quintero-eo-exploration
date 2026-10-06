"""Shared configuration and Earth Engine initialisation."""
import os

import ee

# Region of interest: Quintero-Puchuncavi-Concon bay, central Chile (lon_min, lat_min, lon_max, lat_max)
CQP_BBOX = [-71.60, -32.95, -71.35, -32.70]

# Averaging window used for the annual Sentinel-5P composites (end date exclusive in GEE)
WINDOW_END = "2025-07-14"

# Transect used for profile plots, (lon, lat): south-west (Concon) to north-east (Ventanas)
TRANSECT_START = (-71.55, -32.90)
TRANSECT_END = (-71.43, -32.76)

DRIVE_FOLDER = "EarthEngine_Quintero_CQP"


def init_ee():
    """Initialise Earth Engine with the project given in EE_PROJECT.

    Run `earthengine authenticate` once beforehand (or ee.Authenticate() in a notebook).
    """
    project = os.environ.get("EE_PROJECT")
    if not project:
        raise SystemExit("Set the EE_PROJECT environment variable to your Google Earth Engine project ID.")
    ee.Initialize(project=project)
    return ee.Geometry.Rectangle(CQP_BBOX)
