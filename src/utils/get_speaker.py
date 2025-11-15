import requests
def get_speaker(link :str, slug: str, name: str):
    # TODO: 
    # get the speakers
    response = requests.get(f"{link}/api/v1/tournaments/{slug}/speakers")
    data = response.json()
    # filter out unnecessary entries
    relevant = [entry for entry in data if ((not entry["anonymous"]) and (name in entry["name"]))]
    return relevant