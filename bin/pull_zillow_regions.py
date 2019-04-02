#!/usr/bin/env python3
"""
    Purpose:
        Pull Regions From Zillow

    Steps:
        -

    function call: python3.6 pull_zillow_regions.py {--api-key=api-key}
"""

# Python Library Imports
import logging
import os
import sys
from argparse import ArgumentParser

# Local Library Imports
PROJECT_BASE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, PROJECT_BASE_PATH)
from zillow import zillow_api


def main():
    """
    Purpose:
        Read an .avro File
    """
    logging.info("Starting Pull Zillow Regions")

    cli_arguments = get_cli_arguments()

    regions_by_state =\
        zillow_api.get_regions_by_state(cli_arguments.api_key, cli_arguments.state)

    import pdb; pdb.set_trace()

    logging.info("Pull Zillow Regions Complete")


###
# General/Helper Methods
###


def get_cli_arguments():
    """
    Purpose:
        Parse CLI arguments for script
    Args:
        N/A
    Return:
        N/A
    """
    logging.info("Getting and Parsing CLI Arguments")

    parser = ArgumentParser(description="Pull Zillow Regions")
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')

    # Required Arguments\
    required.add_argument(
        "--api-key",
        dest="api_key",
        help="Zillow API Key",
        required=True,
    )
    required.add_argument(
        "--state",
        dest="state",
        help="State",
        required=True,
    )

    # Optional Arguments
    # N/A

    return parser.parse_args()



if __name__ == "__main__":

    log_level = logging.INFO
    logging.getLogger().setLevel(log_level)
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="[profile_functions] %(asctime)s %(levelname)s %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )

    try:
        main()
    except Exception as err:
        print(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise err
