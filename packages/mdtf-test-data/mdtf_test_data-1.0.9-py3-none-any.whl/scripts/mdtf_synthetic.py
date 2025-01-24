#!/usr/bin/env python
""" mdtf_test_data driver program """
import sys
import mdtf_test_data
from mdtf_test_data.synthetic.synthetic_setup import synthetic_main
from mdtf_test_data.util.cli import cli_holder
import argparse
import pkg_resources as pkgr
from envyaml import EnvYAML

MDTF_PACKAGE_PATH = mdtf_test_data.__path__[0]


def read_yaml(file_name):
    """A function to read YAML files"""
    config = EnvYAML(file_name)
    return config


def main():
    """The the central nervous system of the mdtf_test_data package"""
    print("Starting mdtf_test_data")
    # Define the the CLI arguments and call the parser.
    parser = argparse.ArgumentParser(
        description="parse mdtf_test_data command-line arguments"
    )
    parser.add_argument(
        "--convention",
        "-c",
        type=str,
        help="Model convention",
        choices=["GFDL", "CESM", "NCAR", "CMIP"],
        required=True,
        default="",
    )
    parser.add_argument(
        "--startyear",
        type=int,
        help="Start year of time period",
        required=False,
        default=1,
    )
    parser.add_argument(
        "--nyears",
        type=int,
        help="Total length of time period in years",
        required=False,
        default=10,
    )
    parser.add_argument(
        "--freq",
        nargs='+',
        help="Frequency of data",
        choices=["1hr", "3hr", "day", "mon"],
        required=False,
        default=["1hr", "3hr", "day", "mon"],
    )
    parser.add_argument(
        "--dlat",
        type=float,
        help="Latitude resolution in degrees (will not change default value for NCAR daily data)",
        required=False,
        default=20.0,
    )
    parser.add_argument(
        "--dlon",
        type=float,
        help="Longitude resolution in degrees (will not change default value for NCAR daily data)",
        required=False,
        default=20.0,
    )
    parser.add_argument(
        "--unittest", "-ut", action="store_true", help="Run unit tests", required=False
    )
    args = parser.parse_args()
    cli_info = cli_holder(
        args.convention,
        args.startyear,
        args.nyears,
        args.freq,
        args.dlat,
        args.dlon,
        args.unittest,
    )

    assert (
        cli_info.dlat <= 30.0 and cli_info.dlat >= 0.5
    ), "Error: dlat value is invalid; valid range is [0.5 30.0]"
    assert (
        cli_info.dlon <= 60.0 and cli_info.dlon >= 0.5
    ), "Error: dlon value is invalid; valid range is [0.5 60.0]"

    if cli_info.unittest:
        try:
            import pytest
        except:
            raise Exception("Please install `pytest` in order to run unit tests.")
        retcode_1 = pytest.main(
            ["-x", f"{MDTF_PACKAGE_PATH}/tests/test_synthetic_data.py"]
        )
        if retcode_1 != 0:
            print(
                "test_synthetic_data failed. Check output log for details. Exiting program"
            )
            sys.exit(retcode_1)
        retcode_2 = pytest.main(["-x", f"{MDTF_PACKAGE_PATH}/tests/test_generators.py"])
        if retcode_2 != 0:
            print(
                "test_generators failed. Check output log for details. Exiting program."
            )
            sys.exit(retcode_2)
        retcode_3 = pytest.main(
            ["-x", f"{MDTF_PACKAGE_PATH}/tests/test_construct_tripolar_grid.py"]
        )
        if retcode_3 != 0:
            print(
                "test_construct_tripolar_grid failed. Check output log for details. Exiting program."
            )
            sys.exit(retcode_3)
        retcode_4 = pytest.main(
            ["-x", f"{MDTF_PACKAGE_PATH}/tests/test_construct_rect_grid.py"]
        )
        if retcode_4 != 0:
            print(
                "test_construct_rect_grid failed. Check output log for details. Exiting program."
            )
            sys.exit(retcode_4)

    # output for multiple frequencies if requested by user 
    for freq in cli_info.freq:    
        
        # handle requirements for NCAR and CESM
        conv = cli_info.convention
        dlat = cli_info.dlat
        dlon = cli_info.dlon
        if cli_info.convention == "CESM" or cli_info.convention == "NCAR":
            conv = "NCAR"
            if freq == 'day':
                dlat = 5.0
                dlon = 5.0

        # import variable information
        print(f"Importing {cli_info.convention} variable for information for {freq} frequency")
        input_file = f"{conv.lower()}_{freq}.yml"
        input_data = pkgr.resource_filename("mdtf_test_data", "config/"+input_file)
        try:
            input_data = read_yaml(input_data)
        except FileNotFoundError:
            print(f"ERROR: Could not find {input_file} in config dir! Skipping this request.")
            continue 
   
        # call generator
        print(f"Calling Synthetic Data Generator for {input_file}") 
        synthetic_main(
            input_data,
            DLAT=dlat,
            DLON=dlon,
            STARTYEAR=cli_info.startyear,
            NYEARS=cli_info.nyears,
            CASENAME=f"{cli_info.convention}.Synthetic",
            TIME_RES=freq,
            DATA_FORMAT=conv.lower(),
        )
        
        print(f"Generated data from {input_file}!")
   
    # all done! 
    print(f"Done generating {cli_info.convention} data!")
    sys.exit(0)    

if __name__ == "__main__":
    main()
    sys.exit()
