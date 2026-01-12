import requests
def get_speaks(tab_url: str, slug: str, speaker_url: str):
    # TODO: implement error handling
    # call API for team
    speaks = {}
    try:
        response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/speakers/standings/rounds")
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Could not make a request to URL")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] unwanted response: {response.reason}")
    data = response.json()
    # filter to get team stats
    relevant = [speaker["rounds"] for speaker in data if speaker["speaker"] == speaker_url]
    if len(relevant) == 0:
        return dict()
    for round in relevant[0]:
        speaks.update({round["round"]: round["speeches"][0]["score"]})
    return speaks
    
