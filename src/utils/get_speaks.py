import requests
def get_speaks(tab_url: str, slug: str, speaker_object :dict):
    # TODO: implement error handling
    # call API for team
    speaks = {}
    response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/speakers/standings/rounds")
    data = response.json()
    # filter to get team stats
    speaker_url = speaker_object["url"]
    relevant = [speaker["rounds"] for speaker in data if speaker["speaker"] == speaker_url]
    if len(relevant) == 0:
        return dict()
    for round in relevant[0]:
        speaks.update({round["round"]: round["speeches"][0]["score"]})
    return speaks
    
