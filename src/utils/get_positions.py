import requests

def get_positions(tab_url: str, slug: str, team_rounds :dict, team_url :str):
    r_dict = {}
    # for each round
        # get the pairings
        # for each set of pairings find our
    for round in team_rounds:
        try:
            round_response = requests.get(round["round"])
            pairing_url = round_response.json()["_links"]["pairing"]
            pairing_response = requests.get(pairing_url)
        except requests.exceptions.RequestException as e:
            raise RuntimeError("Could not make a request to URL")
        if pairing_response.status_code != 200:
            raise RuntimeError(f"[{pairing_response.status_code}] unwanted response: {pairing_response.reason}")
        data = pairing_response.json()
        for pairing in data:
            for team in pairing["teams"]:
                if team["team"] == team_url:
                    r_dict.update({round["round"]: team["side"]})
    return r_dict
    

