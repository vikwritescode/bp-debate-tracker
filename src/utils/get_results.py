import requests
def get_results(tab_url: str, slug: str, speaker_object :dict):
    
    # TODO: implement error handling
    # call API for team
    try:
        response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/teams/standings/rounds")
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Could not make a request to URL")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] failed to get speaker: {response.reason}")
    data = response.json()
    # filter to get team stats
    team_url = speaker_object["team"]
    relevant = [team["rounds"] for team in data if team["team"] == team_url]
    if len(relevant) == 0:
        return []
    return relevant