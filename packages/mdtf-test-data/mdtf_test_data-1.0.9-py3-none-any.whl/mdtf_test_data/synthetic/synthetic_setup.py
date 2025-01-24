#!/usr/bin/env python

import warnings
import xarray as xr
import pkg_resources as pkgr

__all__ = ["create_output_dirs", "synthetic_main"]
""" Script to generate synthetic GFDL CM4 output """
import os
from .synthetic_data import generate_synthetic_dataset
from .synthetic_data import write_to_netcdf


def generate_date_string(STARTYEAR=1, NYEARS=1, TIME_RES=""):
    """formulate the date string in the file name"""
    date_string = (
        str(STARTYEAR).zfill(4),
        str(STARTYEAR + NYEARS - 1).zfill(4),
    )
    if TIME_RES == "mon":
        date_string = (date_string[0] + "01", date_string[1] + "12")
    elif TIME_RES == "day":
        date_string = (date_string[0] + "0101", date_string[1] + "1231")
    date_string = ("-").join(list(date_string))

    return date_string


def create_output_dirs(CASENAME="", STARTYEAR=1, NYEARS=10, TIME_RES="day"):
    """Create output data directories"""
    if "cmip" in str.lower(CASENAME):
        # formulate the date string in the file name
        date_string = generate_date_string(
            STARTYEAR=STARTYEAR, NYEARS=NYEARS, TIME_RES="day"
        )
        # output root directory and file name base must match
        out_dir_root = f"{CASENAME.replace('.', '_')}_r1i1p1f1_gr1_{date_string}"
    else:
        out_dir_root = CASENAME

    print("Creating output data directories")

    if not os.path.exists(f"{out_dir_root}/{TIME_RES}"):
        os.makedirs(f"{out_dir_root}/{TIME_RES}")

def synthetic_main(
    yaml_dict={},
    DLAT=20.0,
    DLON=20.0,
    STARTYEAR=1,
    NYEARS=10,
    CASENAME="",
    TIME_RES="",
    DATA_FORMAT="",
):
    """Main script to generate synthetic data using GFDL naming conventions"""
    create_output_dirs(CASENAME, STARTYEAR=STARTYEAR, NYEARS=NYEARS, TIME_RES=TIME_RES)
    # parse the yaml dictionary
    var_names = yaml_dict["variables.name"]
    # -- Create Data
    print("Generating data")
    for v in var_names:
        static = (
            yaml_dict[v + ".static"]
            if str(v + ".static") in list(yaml_dict.keys())
            else False
        )
        stats = (
            yaml_dict[v + ".stats"]
            if str(v + ".stats") in list(yaml_dict.keys())
            else None
        )
        generator = (
            yaml_dict[v + ".generator.name"]
            if str(v + ".generator.name") in list(yaml_dict.keys())
            else "normal"
        )
        generator_kwargs = (
            yaml_dict[v + ".generator.args"]
            if str(v + ".generator.args") in list(yaml_dict.keys())
            else {}
        )
        grid = (
            yaml_dict[v + ".grid"]
            if str(v + ".grid") in list(yaml_dict.keys())
            else "standard"
        )

        assert grid in [
            "tripolar",
            "standard",
        ], f"Unknown grid `{grid}` specified for variable `{v}`"

        coords = (
            yaml_dict[v]["coordinates"]
            if "coordinates" in yaml_dict[v].keys()
            else None
        )

        def _load_default_static():
            """Function to read packaged static file"""
            _ds = pkgr.resource_filename(
                "mdtf_test_data", f"resources/ocean_static_5deg.nc"
            )
            return xr.open_dataset(_ds)["areacello"].values

        # Load the ocean static file
        if static and grid is "tripolar":
            if str(v + ".source") in list(yaml_dict.keys()):
                staticfilepath = yaml_dict[v + ".source.filename"]
                if os.path.exists(staticfilepath):
                    _ds = xr.open_dataset(staticfilepath)
                    data = _ds[yaml_dict[v + ".source.variable"]].values
                else:
                    raise ValueError(
                        f"Specified ocean static file does not exist: {staticfilepath}"
                    )
            else:
                warnings.warn("Using default 5-degree ocean static file for grid")
                data = _load_default_static()
        else:
            data = None

        dset_out = generate_synthetic_dataset(
            DLON,
            DLAT,
            STARTYEAR,
            NYEARS,
            v,
            timeres=TIME_RES,
            attrs=yaml_dict[v + ".atts"],
            fmt=DATA_FORMAT,
            generator=generator,
            stats=stats,
            static=static,
            coords=coords,
            data=data,
            generator_kwargs=generator_kwargs,
            grid=grid,
        )

        if DATA_FORMAT == "cmip":
            # formulate the date string in the file name
            date_string = generate_date_string(
                STARTYEAR=STARTYEAR, NYEARS=NYEARS, TIME_RES="day"
            )

            outname = f"{CASENAME.replace('.','_')}_r1i1p1f1_gr1_{date_string}.{v}.{TIME_RES}.nc"
            # output root directory and file name base must match
            out_dir_root = f"{CASENAME.replace('.','_')}_r1i1p1f1_gr1_{date_string}"
        else:
            outname = f"{CASENAME}.{v}.{TIME_RES}.nc"
            out_dir_root = CASENAME
        write_to_netcdf(dset_out, f"{out_dir_root}/{TIME_RES}/{outname}")
