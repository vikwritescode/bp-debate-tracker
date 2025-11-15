import requests
def get_results(tab_url: str, slug: str, speaker_object :dict):
    # TODO: implement error handling
    # call API for team
    response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/teams/standings/rounds")
    data = response.json()
    # filter to get team stats
    team_url = speaker_object["team"]
    relevant = [team["rounds"] for team in data if team["team"] == team_url]
    if len(relevant) == 0:
        return []
    return relevant