import functools
import xarray as xr
from importlib_resources import files


@functools.cache
def _read_coeffs(file):
    return xr.open_dataset(files('reference_spectra._spectra').joinpath(file))


def get_f76ref():
    return _read_coeffs('f76ref.nc').copy()


def get_f74113():
    return _read_coeffs('f74113.nc').copy()


def get_r74113():
    return _read_coeffs('r74113.nc').copy()


def get_sc21refw():
    return _read_coeffs('sc21refw.nc').copy()