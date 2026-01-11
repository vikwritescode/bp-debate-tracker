import requests
def get_speaker(link :str, slug: str, name: str):
    # TODO: 
    # get the speakers
    try:
        response = requests.get(f"{link}/api/v1/tournaments/{slug}/speakers")
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Could not make a request to URL")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] unwanted response: {response.reason}")
    data = response.json()
    # filter out unnecessary entries
    relevant = [{"name": entry["name"], "team": entry["team"], "url": entry["url"]} for entry in data if ((not entry["anonymous"]) and (name in entry["name"]))]
    return relevant