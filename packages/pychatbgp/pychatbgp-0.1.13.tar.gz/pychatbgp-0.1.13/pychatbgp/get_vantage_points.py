import requests

def get_vantage_points( \
    ip_protocol=None, \
    vantage_points=None, \
    details=None):
    
    """
    Calls the ChatBGP API and returns the response.

    Parameters:
    ip_protocol (str): The IP protocol version. It can be 'ipv4' or 'ipv6' (default is both).
    vantage_points (str): String with the VPs identified by their IP (comma separated). Only VPs in the list can be returned.

    Returns:
    dict: The response from the API in JSON format.
    """

    # url = "https://chatbgp.duckdns.org/vantage_points"
    url = "https://chatbgp.site/vantage_points"
    
    # If vantage_points is a list, convert it to a comma-separated string
    if isinstance(vantage_points, list):
        vantage_points = ",".join(vantage_points)

    # If both 'ipv4' and 'ipv6' are in ip_protocol, set ip_protocol to None
    if ip_protocol is not None and 'ipv4' in ip_protocol and 'ipv6' in ip_protocol:
        ip_protocol = None

    # Prepare the data to send with the POST request
    data = {
        'ip_protocol': ip_protocol,
        'vantage_points': vantage_points,
        'details': details,
    }
    
    try:
        # Send the POST request to the API
        response = requests.post(url, json=data)  # Use 'json=data' to send JSON payload

        # Check if the request was successful
        if response.status_code == 200:
            # Return the response as JSON if the request was successful
            return response.json()
        else:
            # Handle unsuccessful requests
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__": 
    # Example usage
    r = get_vantage_points(details=True)
    print(r)