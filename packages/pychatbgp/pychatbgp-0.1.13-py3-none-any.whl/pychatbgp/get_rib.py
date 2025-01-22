import requests
import json 

def get_rib( \
    vantage_point, \
    date, \
    prefix_regexp=None, \
    aspath_regexp=None, \
    community_regexp=None, \
    return_count=False):
    
    """
    Calls the ChatBGP API and returns the response.

    Parameters:
    vantage_point (str): The IP of the vantage point from which to get the RIB.
    date (str): The date at which to get the RIB (format: MM/DD/YYYY-HH:MM:SS).
    prefix_regexp (str): Regular expression for filtering on prefixes.
    aspath_regexp (str): Regular expression for filtering on AS paths.
    community_regexp (str): Regular expression for filtering on BGP communities.
    return_count (boolean): Whether to return only the number of updates (True means only return the count).

    Returns:
    dict: The response from the API in JSON format.
    """

    # url = "https://chatbgp.duckdns.org/rib"
    url = "https://chatbgp.site/rib"

    
    # Prepare the parameters to send with the request
    params = {
        'vantage_point': vantage_point,
        'date': date,
        'prefix_regexp': prefix_regexp,
        'aspath_regexp': aspath_regexp,
        'community_regexp': community_regexp,
        'return_count': return_count
    }
    
    try:
        # Use stream=True to process the response in chunks
        with requests.get(url, params=params, stream=True) as response:
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Process the response in chunks and reassemble it
            response_data = b"".join(chunk for chunk in response.iter_content(chunk_size=8192))
            
            # Decode the response into a Python dictionary (JSON format)
            return json.loads(response_data)  # Convert the raw bytes to JSON
            
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except json.JSONDecodeError:
        print("Failed to decode the response as JSON.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None

    # try:
    #     # Send the request to the API
    #     response = requests.get(url, params=params)
        
    #     # Check if the request was successful
    #     if response.status_code == 200:
    #         # Return the response as JSON if the request was successful

    #         return response.json()
    #     else:
    #         # Handle unsuccessful requests
    #         response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     # Handle any exceptions that occur during the request
    #     print(f"An error occurred: {e}")
    #     return None

if __name__ == "__main__": 
    r = get_rib(vantage_point='193.203.0.63', date="07/02/2024-01:00:00")#, prefix_regexp="^150.107.120.0/24$")
    print (len(r))