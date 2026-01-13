import requests

def get_data(tab_url: str, slug: str, speaker_url: str):
    # get the speaker object
    s_r = requests.get(speaker_url)
    s = s_r.json()
    
    team_url = s["team"]
    
    resp = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/teams/standings/rounds")
    round_stands = resp.json()
    
    results = dict()
    # get our specific entry in round_stands
    team_round_wise = next(team for team in round_stands if team["team"] == team_url)
    for round in team_round_wise["rounds"]:
        if round["score"] is None:
            # ignore outrounds
            continue 
        result = dict()
        result["round"] = round["round"]
        result["points"] = round["points"]
        result["info_slide"] = ""
        result["motion"] = "blank..?"
        result["speaks"] = 0 # default, if not replaced by round
        
        # getting data from round URL
        round_request_response = requests.get(round["round"])
        round_data = round_request_response.json()
        round_motion_set = round_data["motions"]
        if len(round_motion_set) > 0:
            result["info_slide"] = round_motion_set[0]["info_slide_plain"]
            result["motion"] = round_motion_set[0]["text"]
        
        
        # get positions from motion draw
        pairing_request_response = requests.get(round_data["_links"]["pairing"])
        pairings_data = pairing_request_response.json()
        for room in pairings_data:
            for team in room["teams"]:
                if team["team"] == team_url:
                    result["position"] = team["side"]
        
        results[round["round"]] = result
    
    # get speaks and append to our results
    speak_standings_response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/speakers/standings/rounds")
    speak_standings = speak_standings_response.json()
    # get our speaker
    relevant = next((speaker["rounds"] for speaker in speak_standings if speaker["speaker"] == speaker_url), [])
    for round in relevant:
        speeches = round["speeches"]
        if len(speeches) > 0:
            speaker_score = speeches[0]["score"]
            results[round["round"]]["speaks"] = speaker_score
    
    return list(results.values())
    
        
           