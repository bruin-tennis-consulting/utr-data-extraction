import requests

# Paste your JWT token here (keep it private)
jwt_token = ""

def fetch_ranked_teams():
    url = "https://api.utrsports.net/v1/club/team-rating/top"
    params = {
        "divisionName": "NCAA - Division I",
        "gender": "M",
        "snapshotDateLabel": "Week of Apr 30, 25",
        "descending": "false"
    }
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch rankings: {response.status_code}")
        return []

def get_club_id_from_school_name(school_name_input):
    teams = fetch_ranked_teams()
    school_name_input = school_name_input.lower()

    for team in teams:
        club_name = team.get("clubName", "").lower()
        if school_name_input in club_name:
            club_id = team.get("clubId")
            print(f"Match found: {team.get('clubName')} (Club ID: {club_id})")
            return club_id, team.get("clubName")
    print("No matching school found.")
    return None, None

def get_roster(club_id, school_name_display):
    url = f"https://api.utrsports.net/v1/club/{club_id}/school"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        roster = data.get("roster", [])
        year = data.get("rosterYear", "Unknown Year")

        print(f"\n{school_name_display} Roster ({year}):\n" + "-"*40)
        for player in roster:
            name = player.get("displayName", "N/A")
            gender = player.get("gender", "N/A")
            singles_utr = player.get("singlesUtrDisplay", "N/A")
            doubles_utr = player.get("doublesUtrDisplay", "N/A")
            print(f"{name:25} | Gender: {gender:6} | Singles UTR: {singles_utr:5} | Doubles UTR: {doubles_utr:5}")
    else:
        print(f"Failed to retrieve roster. Status code: {response.status_code}")
        print(response.text)

# Main program
if __name__ == "__main__":
    school_input = input("Enter school name (e.g., Texas, Wake Forest): ").strip()
    club_id, school_name_display = get_club_id_from_school_name(school_input)

    if club_id:
        get_roster(club_id, school_name_display)
