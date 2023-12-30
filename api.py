import requests
import time


# Endpoint URL
masters_url = "https://explorer.lichess.ovh/masters"


def get_position_info(fen):
    params = {"fen": fen}

    # Make the GET request
    response = requests.get(masters_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        opening_data = data.get("opening")
        eco = None
        opening = None
        if opening_data is not None:
            # Extract 'eco' and 'name' keys if present
            eco = opening_data.get("eco")
            opening = opening_data.get("name")

        # Extract 'white_wins', 'draws', and 'black_wins' keys if present
        white_wins = data.get("white")
        draws = data.get("draws")
        black_wins = data.get("black")

        return eco, opening, white_wins, draws, black_wins
    elif response.status_code == 429:
        print("Too many requests -> Waiting 1 minute")
        time.sleep(60)
        return get_position_info(fen)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

