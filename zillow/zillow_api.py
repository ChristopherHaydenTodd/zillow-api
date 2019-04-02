"""
    Purpose:
        Interact with the Zillow API

        This library is used to interact with Minio object storage.
"""

# Python Library Imports
import logging
import os
import requests
import sys
import xml.etree.ElementTree as ET

# Local Library Imports
PROJECT_BASE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, PROJECT_BASE_PATH)
from xml_helpers import xml_parsing_helpers

###
# Base API Call
###


def call_zillow_api(api_endpoint, params, headers):
    """
    Purpose:
        Call a Zillow GET Endpoint. pass in params, headers, and parse
        the results into a Dict
    Args:
        api_endpoint (String): Endpoint to call
        params (Dict of Strings): Params for the endpoint
        headers (Dict of Strings): Headers for the endpoint
    Returns:a
        results_dict (Dicts): Dict results from the endpoint
    """

    raw_results = requests.get(
        api_endpoint,
        params=params,
        headers=headers
    )

    response_code = raw_results.status_code
    if response_code != 200:
        error_msg = f"Request Not Successful: {response_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

    try:
        result_xml_tree = ET.fromstring(raw_results.text)
    except Exception as err:
        logging.error(f"Failed to Parse XML From Zillow: {err}")
        raise err

    try:
        results_dict = xml_parsing_helpers.convert_xml_tree_to_dict(result_xml_tree)
    except Exception as err:
        logging.error(f"Failed to Convert XML To Dict: {err}")
        raise err

    response_text = results_dict.get("message", {}).get("text", "")
    if not response_text:
        error_msg = f"Request Not Successful: No Message Found"
        logging.error(error_msg)
        raise Exception(error_msg)
    elif not "Request successfully processed" in response_text:
        print(results_dict)
        error_msg = f"Request Not Successful: {response_text}"
        logging.error(error_msg)
        raise Exception(error_msg)

    return results_dict


###
# Specific API Calls
###


def get_regions_by_state(zws_id, state):
    """
    Purpose:
        Get Zillow Regions By State
    Args:
        zws_id (String): Zillow API Key
        state (String): 2 character string code of state
    Returns:
        zillow_regions (List of Dicts): List of region dicts with
            information of each Region
    """

    zillow_endpoint =\
        "http://www.zillow.com/webservice/GetRegionChildren.htm"

    params = {
        "zws-id": zws_id,
        "state": state,
    }

    headers = {
        "Content-Type": "application/json",
    }

    result_dict = call_zillow_api(
        zillow_endpoint,
        params,
        headers,
    )

    return result_dict


def get_listing_by_address(zws_id, address, city, state, zip_code):
    """
    Purpose:
        Get Zillow Listings By Zip Code
    Args:
        zws_id (String): Zillow API Key
        zip_code (String): 5 character string code of zip code (not
            int as 0 would be trimmed)
    Returns:
        zillow_listings (List of Dicts): List of listing dicts with
            information of each Listing
    """

    zillow_endpoint =\
        "http://www.zillow.com/webservice/GetSearchResults.htm"

    params = {
        "zws-id": zws_id,
        "address": address,
        "citystatezip": f"{city}, {state} {zip_code}",
    }

    headers = {
        "Content-Type": "application/json",
    }

    result_dict = call_zillow_api(
        zillow_endpoint,
        params,
        headers,
    )

    return result_dict


