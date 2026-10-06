"""CAMS near-real-time surface PM over the CQP bay: daily or multi-day means for selected dates.

CAMS global fields are ~0.4 degrees (~40 km), so the CQP bay (~25 km wide) falls inside one or two
grid cells. Statistics are therefore computed at 5-10 km scale, never at the 400 m the export grid
could suggest. CAMS NRT PM bands are in kg/m3; multiply by 1e9 for ug/m3.

Usage: python cams_pm.py 2024-02-10 [2024-02-11]
"""
import sys

import ee

from config import init_ee

BAND = {"pm10": "particulate_matter_d_less_than_10_um_surface",
        "pm25": "particulate_matter_d_less_than_25_um_surface"}


def mean_ugm3(start, end, roi, species="pm10"):
    band = BAND[species]
    img = (
        ee.ImageCollection("ECMWF/CAMS/NRT")
        .filterDate(start, end)
        .select(band)
        .mean()
        .multiply(1e9)
        .clip(roi)
    )
    stats = img.reduceRegion(
        reducer=ee.Reducer.mean().combine(ee.Reducer.max(), sharedInputs=True),
        geometry=roi,
        scale=5000,
    ).getInfo()
    return stats[f"{band}_mean"], stats[f"{band}_max"]


if __name__ == "__main__":
    roi = init_ee()
    start = sys.argv[1]
    end = sys.argv[2] if len(sys.argv) > 2 else ee.Date(start).advance(1, "day")
    for sp in ("pm10", "pm25"):
        mean, mx = mean_ugm3(start, end, roi, sp)
        print(f"{sp}: regional mean {mean} ug/m3, max {mx} ug/m3")
