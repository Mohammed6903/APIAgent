import requests
from agno.tools import tool

@tool(show_result=True)
def get(url: str, params: dict = None, headers: dict = None) -> dict:
    """
    Send a GET request to the specified URL with optional parameters and headers.

    Args:
        url (str): The URL to send the GET request to.
        params (dict, optional): A dictionary of query parameters to include in the request.
        headers (dict, optional): A dictionary of headers to include in the request.

    Returns:
        dict: The JSON response from the server, or an empty dictionary if the response is not JSON.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}
    except ValueError:
        print("Response is not in JSON format.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
    
@tool(show_result=True)
def post(url: str, data: dict = None, headers: dict = None) -> dict:
    """
    Send a POST request to the specified URL with optional data and headers.

    Args:
        url (str): The URL to send the POST request to.
        data (dict, optional): A dictionary of data to include in the request body.
        headers (dict, optional): A dictionary of headers to include in the request.

    Returns:
        dict: The JSON response from the server, or an empty dictionary if the response is not JSON.
    """
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() 
        return response.status_code
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}
    except ValueError:
        print("Response is not in JSON format.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
