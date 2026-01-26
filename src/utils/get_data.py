import requests
import asyncio
import aiohttp

def get_data(tab_url: str, slug: str, speaker_url: str):
    """
    Make API requests, getting the data for a speaker at a tournament
    
    :param tab_url: the tab URL
    :type tab_url: str
    :param slug: the tournament slug
    :type slug: str
    :param speaker_url: the speaker URL
    :type speaker_url: str
    """
    
    async def fetch(session, url):
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
    
    async def get_pairings(urls):
        async with aiohttp.ClientSession() as session:
            tasks = {u: fetch(session, u) for u in urls}
            results = await asyncio.gather(*tasks.values())
            data_map = dict(zip(tasks.keys(), results))
            return data_map
    
    
    
    s_r = requests.get(speaker_url)
    s = s_r.json()
    
    team_url = s["team"]
    
    speak_standings_response = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/speakers/standings/rounds")
    speak_standings = speak_standings_response.json()
    
    resp = requests.get(f"{tab_url}/api/v1/tournaments/{slug}/teams/standings/rounds")
    round_stands = resp.json()
    
    print("(1) gotten round standings")
    
    results = dict()
    # get our specific entry in round_stands
    team_round_wise = next(team for team in round_stands if team["team"] == team_url)
    
    # fetch all rounds concurrently
    pairings_urls = [r["round"] for r in team_round_wise["rounds"]]
    pairings_jsons = asyncio.run(get_pairings(pairings_urls))
    
    
    # processing for each round
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
        
        # getting data from round URL (already fetched tho)
        round_data = pairings_jsons[round["round"]]
        print("(2) gotten round data")
        
        round_motion_set = round_data["motions"]
        if len(round_motion_set) > 0:
            result["info_slide"] = round_motion_set[0]["info_slide_plain"]
            result["motion"] = round_motion_set[0]["text"]
        
        
        # get positions from motion draw
        pairing_request_response = requests.get(round_data["_links"]["pairing"])
        pairings_data = pairing_request_response.json()
        print("(3) gotten pairing data")
        for room in pairings_data:
            for team in room["teams"]:
                if team["team"] == team_url:
                    result["position"] = team["side"]
        
        results[round["round"]] = result
    
    # get speaks and append to our results
    print("(4) gotten speaks data")
    # get our speaker
    relevant = next((speaker["rounds"] for speaker in speak_standings if speaker["speaker"] == speaker_url), [])
    for round in relevant:
        speeches = round["speeches"]
        if len(speeches) > 0:
            speaker_score = speeches[0]["score"]
            results[round["round"]]["speaks"] = speaker_score
    
    return list(results.values())
    
        
           