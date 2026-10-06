# quintero-eo-exploration

Exploratory processing of satellite and reanalysis air-quality products over the
Quintero-Puchuncaví-Concón (CQP) industrial bay in central Chile, using Google Earth Engine and Python.
It was written while scoping the observation side of my MSc thesis on PM10 emission-source recovery
(WRF-ARW / FEniCSx coupling, Tikhonov and Kalman/RTS inversion), which uses ground stations.

## What it does

| Script | Purpose |
|---|---|
| `src/s5p_annual_means.py` | Annual means of Sentinel-5P TROPOMI tropospheric NO2, SO2 and UV absorbing aerosol index; exports 1 km GeoTIFFs |
| `src/cams_pm.py` | CAMS NRT surface PM10 / PM2.5 means and maxima for chosen dates, in µg/m³, evaluated at a physically sensible scale |
| `src/plot_maps_transects.py` | Maps over a basemap and a SW-NE transect through the industrial area |
| `src/config.py` | ROI, averaging window, transect, Earth Engine initialisation |

## Usage

```bash
pip install -r requirements.txt
earthengine authenticate
export EE_PROJECT=<your-gee-project-id>
python src/s5p_annual_means.py        # exports GeoTIFFs to Google Drive
python src/cams_pm.py 2024-02-10
python src/plot_maps_transects.py path/to/cqp_no2_annual_mean_*.tif
```

## Limitations (please read)

This is exploratory data processing, not a retrieval or inversion study.

- No averaging kernels, no vertical-profile or air-mass-factor treatment, no atmospheric chemistry.
  Column densities are used as delivered by the GEE L3 products.
- Quality filtering of the S5P L3 collections is applied upstream by GEE (the collections expose no
  `qa_value` band); thresholds per product are documented in the GEE catalog. Nothing is added here.
- CAMS global fields have ~0.4° (~40 km) resolution, so the whole bay lies inside one or two cells.
  They represent regional background, not local concentrations; statistics are taken at 5-10 km scale.
- No quantitative validation against ground stations is included. Comparisons with SINCA stations were
  done qualitatively during exploration and the numbers are not reproduced here.
- Annual means are simple unweighted means of daily images over one year, without accounting for
  cloud-related sampling bias.

## License

MIT
