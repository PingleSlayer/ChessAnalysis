import requests
import time
import json

def get_opening_data(fen):
    # Make the GET request
    params = {"fen": fen}
    lichess_url = "https://explorer.lichess.ovh/lichess"
    response = requests.get(lichess_url, params=params)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        opening_data = data.get("opening")
        eco = None
        name = None
        if opening_data is not None:
            # Extract 'eco' and 'name' keys if present
            eco = opening_data.get("eco")
            name = opening_data.get("name")

        # Extract 'white wins', 'draws', and 'black wins' keys if present
        white = data.get("white")
        draws = data.get("draws")
        black = data.get("black")

        return eco, name, white, draws, black
    # Check if too many requests (status code 429)
    elif response.status_code == 429:
        print("Opening explorer: Too many requests -> Waiting 1 minute")
        time.sleep(60)
        return get_opening_data(fen)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
        

def get_tablebase_result(fen):
    # Make the GET request
    params = {"fen": fen}
    tablebase_url = "https://tablebase.lichess.ovh"
    response = requests.get(tablebase_url, params=params)
    print(response)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        category = data.get("category")
        mate_dist = data.get("dtm")
        return category, mate_dist
    elif response.status_code == 429:
        print("Tablebase: Too many requests -> Waiting 1 minute")
        time.sleep(60)
        return get_tablebase_result(fen)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    

