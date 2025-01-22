import requests

from .exceptions import FaultsAPIError

FAULTS_URL = "https://citypower.mobi/forcelink/za4/rest/calltakemanager"


def get_all_faults(cookie: str) -> list[dict]:
    """
    Fetch all logged faults from the API.
    """
    url = f"{FAULTS_URL}/getAllCustomerCalls"
    headers = {"Content-Type": "application/json", "Cookie": cookie}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise FaultsAPIError(f"Failed to fetch faults: {str(e)}") from e


def log_fault_my_address(cookie: str, fault_data: dict) -> dict:
    """
    Log a fault to the API.
    """
    url = f"{FAULTS_URL}/logCallMyAddress"
    headers = {
        "Accept": "*/*",
        "Referer": "https://citypower.mobi/logFaultMyAddress",
        "Content-Type": "application/problem+json",
        "Origin": "https://citypower.mobi",
        "Connection": "keep-alive",
        "Cookie": cookie,
    }

    try:
        response = requests.post(url, headers=headers, json=fault_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise FaultsAPIError(f"Failed to log fault: {str(e)}") from e

def log_fault_other_address(cookie: str, fault_data: dict) -> dict:
    """
    Log a fault to the API.
    """
    url = f"{FAULTS_URL}/logCallOtherAddress"
    headers = {
        "Accept": "*/*",
        "Referer": "https://citypower.mobi/logFaultOtherAddress",
        "Content-Type": "application/problem+json",
        "Origin": "https://citypower.mobi",
        "Connection": "keep-alive",
        "Cookie": cookie,
    }

    try:
        response = requests.post(url, headers=headers, json=fault_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise FaultsAPIError(f"Failed to log fault: {str(e)}") from e