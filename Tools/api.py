import requests
from agno.tools import tool
from typing import Optional, Dict, Any


@tool(name="api_request", description="sends requests to an API endpoint")
def APIRequest(
    url: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> dict:
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
        # Ensure params and headers are dictionaries if None
        params = params or {}
        headers = headers or {}

        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, params=params)
        else:
            raise ValueError("Unsupported HTTP method. Use 'GET' or 'POST'.")

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return text content
            return {"response": response.text, "status_code": response.status_code}

    except requests.RequestException as e:
        return {
            "error": f"Request failed: {e}",
            "status_code": getattr(e.response, "status_code", None),
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
