import copy
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from pygridsio.grid_operations import resample_xarray_grid_to_other_grid_resolution
from pygridsio.grid_to_xarray import isValidDataArrayGrid
from pygridsio.pygridsio import read_grid
from pygridsio.resources.netherlands_shapefile.shapefile_plot_util import get_netherlands_shapefile


def zoom_on_grid(ax,  z, x, y, zoom_buffer=10000):
    # if all values are nan simply return
    if np.isnan(z).all():
        return

    not_nan_locs = np.argwhere(~np.isnan(z))
    x_all = []
    y_all = []
    for coords in not_nan_locs:
        x_all.append(coords[1])
        y_all.append(coords[0])

    minx = x[np.min(x_all)]
    maxx = x[np.max(x_all)]
    miny = y[np.min(y_all)]
    maxy = y[np.max(y_all)]
    ax.set_xlim([minx - zoom_buffer, maxx + zoom_buffer])
    ax.set_ylim([miny - zoom_buffer, maxy + zoom_buffer])
    ax.set_xlim([minx - zoom_buffer, maxx + zoom_buffer])
    ax.set_ylim([miny - zoom_buffer, maxy + zoom_buffer])


def plot_grid(grid: xr.DataArray, axes=None, outfile=None, show=False, cmap="viridis", vmin=None, vmax=None, zoom=True, zoom_buffer=10000, custom_shapefile=None, add_netherlands_shapefile=False,
              shapefile_alpha=0.5):
    """
    Plot a custom grid class

    Parameters
    ----------
    grid
        The grid object; either custom or a xarray.DataArray
    ax (optional)
        An axes object to plot the grid onto; if not provided a figure and axes object will be created
    outfile (optional)
        The file to save the figure to; if not provided then will show instead of save the figure
    cmap (optional)
        The colour map to use; if not provided matplotlib default will be used
    vmin (optional)
        The minimum value for the colourmap
    vmax (optional)
        The maximum value for the colourmap
    zoom (optional)
        Zoom onto the non-nan part of the grid.
    zoom_buffer (optional)
        A space around the non-nan part of the grid to be added if zoom is applied
    add_netherlands_shapefile (optional)
        Adds a shapefile of the netherlands to the background of the plot
    shapefile_alpha (optional)
        Controls the transparency of the shapefile

    Returns
    -------

    """
    if not isValidDataArrayGrid(grid):
        raise TypeError("This method only accepts a xarray DataArray with dimensions x and y")

    if axes is None:
        fig, axes = plt.subplots(1, 1, figsize=(6, 5))

    # plot each grid
    grid.plot(ax=axes, x="x", y="y", cmap=cmap, vmin=vmin, vmax=vmax)

    if zoom:
        zoom_on_grid(axes, grid.data, grid.x, grid.y, zoom_buffer=zoom_buffer)
    axes.tick_params(axis='both', which='major', labelsize=8)

    if add_netherlands_shapefile:
        shapefile = get_netherlands_shapefile()
        shapefile.plot(ax=axes, alpha=shapefile_alpha, edgecolor="k", zorder=-1)

    if custom_shapefile is not None:
        custom_shapefile.plot(ax=axes, alpha=shapefile_alpha, edgecolor="k", zorder=-1)

    if outfile is not None:
        plt.savefig(outfile)

    if show:
        plt.show()


def plot_grid_comparison(grid1: xr.DataArray | str | Path, grid2: xr.DataArray | str | Path, outfile: str | Path, custom_shapefile=None, add_netherlands_shapefile=False, title1=None, title2=None, suptitle=None):
    """
    Compare two grids to eachother, making a plot with 6 panels; two plots of the grids as maps, one of the difference of grid1 - grid2, and on the bottom row their respective histograms of the non-nan values
    Parameters
    ----------
    grid1
    grid2
    outfile
    custom_shapefile - a shapefile to plot behind the grids
    add_netherlands_shapefile - if true, plot a shapefile of the Netherlands
    title1 - the title of the top left panel
    title2 - the title of the top middle panel
    suptitle - the overall title

    Returns
    -------

    """
    if isinstance(grid1,Path) or isinstance(grid1,str):
        grid1 = read_grid(grid1)
    if isinstance(grid2, Path) or isinstance(grid2, str):
        grid2 = read_grid(grid2)
    if not isValidDataArrayGrid(grid1) or not isValidDataArrayGrid(grid2):
        raise TypeError("This method only accepts a xarray DataArray with dimensions x and y")

    # setup figure
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(20, 8), height_ratios=[1, 0.5])
    grid_axes = [axes[0][0], axes[0][1], axes[0][2]]
    hist_axes = [axes[1][0], axes[1][1], axes[1][2]]
    fig.tight_layout(pad=5)

    # resample grid2 to have the same resolution as grid1 for calculating the difference grid
    grid2_resampled = copy.deepcopy(grid2)
    grid2_resampled = resample_xarray_grid_to_other_grid_resolution(grid2_resampled,grid1)
    diff_grid = grid1 - grid2_resampled
    grid_list = [grid1, grid2_resampled, diff_grid]

    # plotting the individual grids with the same values on the colour bars
    cmaps = ["viridis", "viridis", "coolwarm"]
    mins = []
    maxs = []
    if not np.isnan(grid1.data).all():
        mins.append(np.nanmin(grid1.data))
        maxs.append(np.nanmax(grid1.data))
    if not np.isnan(grid2.data).all():
        mins.append(np.nanmin(grid2.data))
        maxs.append(np.nanmax(grid2.data))
    if len(mins) == 0:
        mins = [1.0]
        maxs = [1.0]
    vmin, vmax = np.min(mins), np.max(maxs)

    if not np.isnan(diff_grid.data).all():
        max_abs_val = np.nanmax(np.abs(diff_grid.data))
    else:
        max_abs_val = 1.0

    plot_grid(grid1, axes=grid_axes[0], cmap=cmaps[0], vmin=vmin, vmax=vmax, zoom=True, custom_shapefile=custom_shapefile, add_netherlands_shapefile=add_netherlands_shapefile)
    plot_grid(grid2, axes=grid_axes[1], cmap=cmaps[1], vmin=vmin, vmax=vmax, zoom=True, custom_shapefile=custom_shapefile, add_netherlands_shapefile=add_netherlands_shapefile)
    plot_grid(diff_grid, axes=grid_axes[2], cmap=cmaps[2], vmin=-max_abs_val, vmax=max_abs_val, zoom=True, custom_shapefile=custom_shapefile, add_netherlands_shapefile=add_netherlands_shapefile)

    # make histograms
    vmins = [vmin, vmin, -max_abs_val]
    vmaxs = [vmax, vmax, max_abs_val]
    for i in range(3):
        data = grid_list[i].data
        data = data[~np.isnan(data)]
        data = data.flatten()
        n, bins, patches = hist_axes[i].hist(data, bins=20)
        if i < 2 and vmin != vmax:
            hist_axes[i].set_xlim(left=vmin, right=vmax)

        # Create a gradient color effect
        for j, p in enumerate(patches):
            cm = plt.get_cmap(cmaps[i])
            norm = mpl.colors.Normalize(vmin=vmins[i], vmax=vmaxs[i])
            plt.setp(p, 'facecolor', cm(norm(bins[j])))

    # add in the histogram from the other grid in the background:
    def add_background_hist(ax, data):
        data = data[~np.isnan(data)]
        data = data.flatten()
        ax.hist(data, bins=20, zorder=-1, color="lightgrey")

    add_background_hist(hist_axes[0], grid2_resampled.data)
    hist_axes[0].set_title(f"Grid 1 dx: {grid1.x.data[1] - grid1.x.data[0]}m, dy: {grid1.y.data[1] - grid1.y.data[0]}m")
    add_background_hist(hist_axes[1], grid1.data)
    hist_axes[1].set_title(f"Grid 2 dx: {grid2.x.data[1] - grid2.x.data[0]}m, dy: {grid2.y.data[1] - grid2.y.data[0]}m")

    # make titles
    minmax_string1 = f"min: {np.nanmin(grid1.data):.3f} max: {np.nanmax(grid1.data):.3f}"
    if title1 is None:
        grid_axes[0].set_title(f"grid 1\n{minmax_string1}")
    else:
        grid_axes[0].set_title(f"{title1}\n{minmax_string1}")

    minmax_string2 = f"min: {np.nanmin(grid1.data):.3f} max: {np.nanmax(grid1.data):.3f}"
    if title2 is None:
        grid_axes[1].set_title(f"grid 2\n{minmax_string2}")
    else:
        grid_axes[1].set_title(f"{title2}\n{minmax_string2}")

    if suptitle is not None:
        plt.suptitle(suptitle)
    addon = ""
    if not np.isnan(diff_grid.data).all():
        addon = f"\nmin: {np.nanmin(diff_grid.data):.3f} max: {np.nanmax(diff_grid.data):.3f}"
    grid_axes[2].set_title(f"difference (grid1 - grid2)" + addon)
    plt.savefig(outfile)
    plt.close()
