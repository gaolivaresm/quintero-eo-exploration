"""Map the exported GeoTIFFs over a basemap and plot a SW-NE transect through the industrial area.

Usage: python plot_maps_transects.py path/to/cqp_no2_annual_mean_*.tif
"""
import sys
import warnings

import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show
from shapely.geometry import LineString

from config import TRANSECT_END, TRANSECT_START

warnings.filterwarnings("ignore", category=FutureWarning)


def plot_map(path, title, label, cmap="plasma"):
    with rasterio.open(path) as src:
        data = src.read(1, masked=True)
        if data.mask.all():
            print(f"no valid data in {path}")
            return
        vmin, vmax = np.nanpercentile(data, 5), np.nanpercentile(data, 95)
        if np.isclose(vmin, vmax):
            vmax = vmin + 1e-9
        fig, ax = plt.subplots(figsize=(10, 10))
        show(data, transform=src.transform, ax=ax, cmap=cmap, vmin=vmin, vmax=vmax, alpha=0.7, zorder=10)
        ctx.add_basemap(ax, crs=src.crs.to_string(), source=ctx.providers.CartoDB.Positron, zorder=1)
        fig.colorbar(ax.images[0], ax=ax, orientation="horizontal", fraction=0.04, pad=0.05, shrink=0.8).set_label(label)
        ax.set_title(title)
        ax.set_axis_off()
        plt.tight_layout()
        plt.show()


def plot_transect(path, title, ylabel, n=100):
    with rasterio.open(path) as src:
        line = LineString([TRANSECT_START, TRANSECT_END])
        pts = [line.interpolate(d) for d in np.linspace(0, line.length, n)]
        values = np.array([v[0] for v in src.sample([(p.x, p.y) for p in pts])], dtype=np.float32)
        length_km = line.length * 111.32 * np.cos(np.radians(TRANSECT_START[1]))  # approximate
        plt.figure(figsize=(10, 5))
        plt.plot(np.linspace(0, length_km, n), values, ".-", markersize=4)
        plt.title(title)
        plt.xlabel("Distance along transect (approx. km)")
        plt.ylabel(ylabel)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    tif = sys.argv[1]
    plot_map(tif, f"{tif}", "column density (mol/m2) or index")
    plot_transect(tif, "SW-NE transect", "column density (mol/m2) or index")
