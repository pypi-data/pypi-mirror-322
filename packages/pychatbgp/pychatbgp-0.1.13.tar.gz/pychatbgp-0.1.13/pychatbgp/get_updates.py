import requests
import json 

def get_updates( \
    vantage_point, \
    start_date, \
    end_date, \
    type_regexp=None, \
    prefix_regexp=None, \
    aspath_regexp=None, \
    community_regexp=None, \
    chronological_order=True, \
    max_updates_to_return=None, \
    return_count=False):
    
    """
    Calls the ChatBGP API and returns the response.

    Parameters:
    vantage_point (str): The IP of the vantage point from which to get the RIB.
    start_date (str): Start date for the updates in 'MM/DD/YYYY-HH:MM:SS' format.
    end_date (str): End date for the updates in 'MM/DD/YYYY-HH:MM:SS' format.
    type_regexp (str): Regular expression for filtering on the type (Announcement 'A', Withdrawals 'W').
    prefix_regexp (str): Regular expression for filtering on prefixes.
    aspath_regexp (str): Regular expression for filtering on AS paths.
    community_regexp (str): Regular expression for filtering on BGP communities.
    chronological_order (boolean): True means return updates in the chronological order (otherwise False).
    max_updates_to_return (int): Maximum number of updates to return.
    return_count (boolean): Whether to return only the number of updates (True means only return the count).

    Returns:
    dict: The response from the API in JSON format.
    """

    # url = "https://chatbgp.duckdns.org/updates"
    url = "https://chatbgp.site/updates"


    # Prepare the parameters to send with the request
    params = {
        'vantage_point': vantage_point,
        'start_date': start_date,
        'end_date': end_date,
        'type_regexp': type_regexp,
        'prefix_regexp': prefix_regexp,
        'aspath_regexp': aspath_regexp,
        'community_regexp': community_regexp,
        'chronological_order': chronological_order,
        'max_updates_to_return': max_updates_to_return,
        'return_count': return_count
    }
    
    try:
        # Use stream=True to process the response in chunks
        with requests.get(url, params=params, stream=True) as response:
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            response_data = b"".join(chunk for chunk in response.iter_content(chunk_size=8192))

            if return_count:
                return json.loads(response_data)[0]
            else:
                return json.loads(response_data)
    
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
    #         if return_count is True:
    #             return response.json()[0]
    #         else:
    #             return response.json()
    #     else:
    #         # Handle unsuccessful requests
    #         response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     # Handle any exceptions that occur during the request
    #     print(f"An error occurred: {e}")
    #     return None

if __name__ == "__main__": 
    # r = get_updates(vantage_point='80.81.194.190', start_date="01/01/2024-00:00:00", end_date="01/11/2024-00:00:00", return_count=True)
    # print (r)

    l = get_updates('202.249.2.20', start_date="07/01/2024-00:00:00", end_date="07/03/2024-00:00:00")  #, prefix_regexp='^'+"181\.225\.48\.0/24"+'$', type_regexp='A', chronological_order=False, max_updates_to_return=10):
    print (len(l))

    # print (len(list(l)))

    # print (len(list(get_updates(vantage_point='80.81.194.190', start_date="01/01/2024-00:00:00", end_date="01/11/2024-00:00:00"))))
    # for u in get_updates(vantage_point='80.81.194.190', start_date="01/01/2024-00:00:00", end_date="01/11/2024-00:00:00"):
    #     print (u)