import requests
from agno.tools import tool

@tool()
def wrapperforrequests(url: str, method: str, params: dict = None, data: dict = None, headers: dict = None) -> dict:
    """
    Send a request to the specified URL with the given method, parameters, data, and headers.

    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use (GET or POST).
        params (dict, optional): A dictionary of query parameters to include in the request.
        data (dict, optional): A dictionary of data to include in the request body.
        headers (dict, optional): A dictionary of headers to include in the request.

    Returns:
        dict: The JSON response from the server, or an empty dictionary if the response is not JSON.
    """
    try:
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method. Use 'GET' or 'POST'.")
        
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