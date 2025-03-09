import requests

# Your JWT token (keep it private!)
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6IjE2MTk3ODciLCJlbWFpbCI6Impvc2h1YXN1am8yQGdtYWlsLmNvbSIsIlZlcnNpb24iOiIxIiwiRGV2aWNlTG9naW5JZCI6IjIzMDg4MTAxIiwibmJmIjoxNzQxMDQzODE3LCJleHAiOjE3NDM2MzU4MTcsImlhdCI6MTc0MTA0MzgxN30.-AB1iflZOrxiUVuSJqy_Ah7-6mdHtXByOHFgGIjZLwA"


headers = {
    "Authorization": f"Bearer {jwt_token}"
}

ucla_player = "Alexander Hoogmartens"
# Search for {ucla_player}'s user ID
search_url = "https://app.universaltennis.com/api/v2/search/players?query=Alexander%20Hoogmartens"
response = requests.get(search_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Look for the players inside the 'hits' key
    players = data.get('hits', [])  # Use .get() to avoid KeyError
    if players:
        # Get the user ID
        user_id = players[0].get('id')  # Adjust based on correct structure
        if user_id:
            print(f"{ucla_player}'s User ID: {user_id}")
            
            # Get match results
            results_url = f"https://app.universaltennis.com/api/v1/player/{user_id}/results?year=last&type=singles"
            results_response = requests.get(results_url, headers=headers)

            if results_response.status_code == 200:
                match_data = results_response.json()

                # Iterate through the events
                for event in match_data.get('events', []):
                    event_name = event.get('name', 'Unknown event')
                    print(f"Event: {event_name}")
                    
                    # Iterate through the draws within each event
                    for draw in event.get('draws', []):
                        draw_name = draw.get('name', 'Unknown draw')
                        print(f"  Draw: {draw_name}")
                        
                        # Iterate through the results of each draw
                        for result in draw.get('results', []):
                            # Extracting the score and players
                            score = result.get('score', {})
                            winner1_first_name = result.get('players', {}).get('winner1', {}).get('firstName', 'Unknown Winner')
                            winner1_last_name = result.get('players', {}).get('winner1', {}).get('lastName', 'Unknown Winner')
                            loser1_first_name = result.get('players', {}).get('loser1', {}).get('firstName', 'Unknown Loser')
                            loser1_last_name = result.get('players', {}).get('loser1', {}).get('lastName', 'Unknown Loser')

                            # Score format: winner, loser, and their scores
                            score_text = f"{score.get('1', {}).get('winner', 'N/A')} - {score.get('1', {}).get('loser', 'N/A')} , {score.get('2', {}).get('winner', 'N/A')} - {score.get('2', {}).get('loser', 'N/A')}"
                            
                            print(f"    Match: {winner1_first_name} {winner1_last_name} vs {loser1_first_name} {loser1_last_name}")
                            print(f"    Score: {score_text}")
                            
            else:
                print(f"Error fetching match results: {results_response.status_code} - {results_response.text}")
        else:
            print("User ID not found in player data.")
    else:
        print("Player not found.")
else:
    print(f"Error searching for player: {response.status_code} - {response.text}")