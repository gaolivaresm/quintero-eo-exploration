"""Annual mean Sentinel-5P TROPOMI composites (NO2, SO2, absorbing aerosol index) over the CQP bay.

Exports 1 km GeoTIFFs to Google Drive.

Quality filtering: the GEE L3 OFFL collections do not expose a `qa_value` band. Filtering is applied
upstream when GEE converts L2 to L3 (see the dataset pages in the GEE catalog for the thresholds per
product), so no extra mask is applied here.
"""
import time

import ee

from config import DRIVE_FOLDER, WINDOW_END, init_ee

PRODUCTS = {
    "no2": ("COPERNICUS/S5P/OFFL/L3_NO2", "tropospheric_NO2_column_number_density"),
    "so2": ("COPERNICUS/S5P/OFFL/L3_SO2", "SO2_column_number_density"),
    "aer_ai": ("COPERNICUS/S5P/OFFL/L3_AER_AI", "absorbing_aerosol_index"),
}


def annual_mean(collection_id, band, roi):
    end = ee.Date(WINDOW_END)
    start = end.advance(-1, "year")
    return (
        ee.ImageCollection(collection_id)
        .filterDate(start, end)
        .filterBounds(roi)
        .select(band)
        .mean()
        .clip(roi)
    )


def main():
    roi = init_ee()
    stamp = time.strftime("%Y%m%d_%H%M%S")
    tasks = {}
    for key, (collection_id, band) in PRODUCTS.items():
        name = f"cqp_{key}_annual_mean_{stamp}"
        task = ee.batch.Export.image.toDrive(
            image=annual_mean(collection_id, band, roi),
            description=name,
            folder=DRIVE_FOLDER,
            fileNamePrefix=name,
            region=roi,
            scale=1000,
            crs="EPSG:4326",
            maxPixels=1e10,
        )
        task.start()
        tasks[key] = task
        print(f"started: {name}")

    while True:
        states = {k: t.status()["state"] for k, t in tasks.items()}
        print(time.strftime("%H:%M:%S"), states)
        if not any(s in ("READY", "RUNNING") for s in states.values()):
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
