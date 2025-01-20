import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Optional, Union

import numpy as np
from numpy import ndarray
from rasterio.crs import CRS

from glidergun._types import Extent

if TYPE_CHECKING:
    from glidergun._grid import Grid


def create_parent_directory(file_path: str):
    directory = "/".join(re.split(r"/|\\", file_path)[0:-1])
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_crs(crs: Union[int, CRS]):
    return CRS.from_epsg(crs) if isinstance(crs, int) else crs


def format_type(data: ndarray):
    if data.dtype == "float64":
        return np.asanyarray(data, dtype="float32")
    if data.dtype == "int64":
        return np.asanyarray(data, dtype="int32")
    if data.dtype == "uint64":
        return np.asanyarray(data, dtype="uint32")
    return data


def get_nodata_value(dtype: str) -> Union[float, int, None]:
    if dtype == "bool":
        return None
    if dtype.startswith("float"):
        return float(np.finfo(dtype).min)
    if dtype.startswith("uint"):
        return np.iinfo(dtype).max
    return np.iinfo(dtype).min


def batch_process(
    grid: "Grid",
    func: Callable[["Grid"], "Grid"],
    tile_size: int,
    buffer: int,
    max_workers: int,
) -> "Grid":
    cell_x, cell_y = grid.cell_size
    tiles = list(grid.extent.tiles(cell_x * tile_size, cell_y * tile_size))

    if len(tiles) <= 4:
        return func(grid)

    x = buffer * cell_x
    y = buffer * cell_y

    def f(tile: Extent):
        xmin, ymin, xmax, ymax = tile
        g = func(grid.clip(xmin - x, ymin - y, xmax + x, ymax + y))
        if buffer == 0:
            return g
        return g.clip(xmin, ymin, xmax, ymax)

    result: Optional["Grid"] = None

    if max_workers > 1:
        with ThreadPoolExecutor(max_workers or 1) as executor:
            for r in executor.map(f, tiles):
                result = result.mosaic(r) if result else r
    else:
        for i, tile in enumerate(tiles):
            print(f"Processing tile {i + 1} of {len(tiles)}...")
            result = result.mosaic(f(tile)) if result else f(tile)

    assert result
    return result
