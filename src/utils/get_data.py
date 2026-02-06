import requests
import asyncio
import aiohttp
from models import TabAuthError

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
        """
        Get pairings simultaneously
        
        :param urls: list of URL pairings
        """
        async with aiohttp.ClientSession() as session:
            tasks = {u: fetch(session, u) for u in urls}
            results = await asyncio.gather(*tasks.values())
            data_map = dict(zip(tasks.keys(), results))
            return data_map
    
    async def get_standings(tab_url, slug):
        """
        Get both speaker and team standings simultaneously
        
        :param tab_url: the tab URL
        :param slug: tournament slug
        """
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, f"{tab_url}/api/v1/tournaments/{slug}/speakers/standings/rounds"),
                     fetch(session, f"{tab_url}/api/v1/tournaments/{slug}/teams/standings/rounds"),
                     fetch(session, f"{tab_url}/api/v1/tournaments/{slug}")
                     ]
            results = await asyncio.gather(*tasks)
            return results
    

    
    try:
        s_r = requests.get(speaker_url)
        s_r.raise_for_status()
        
        s = s_r.json()
        team_url = s["team"]
        
        # get our data concurrently for everything except pairings
        stand = asyncio.run(get_standings(tab_url, slug))
        speak_standings = stand[0]
        round_stands = stand[1]
        tourney_name = stand[2]["short_name"]
        
        results = dict()
        # get our specific entry in round_stands
        team_round_wise = next(team for team in round_stands if team["team"] == team_url)
    
        # fetch all rounds concurrently
        rounds_urls = [r["round"] for r in team_round_wise["rounds"]]
        rounds_jsons = asyncio.run(get_pairings(rounds_urls))
        
        # fetch all pairings concurrently
        pairings_urls = [r["_links"]["pairing"] for r in rounds_jsons.values()]
        pairings_jsons = asyncio.run(get_pairings(pairings_urls))
    except (requests.exceptions.HTTPError, aiohttp.ClientResponseError) as e:
        # status location differs with async and sync
        status = getattr(e, 'status', None) or (e.response.status_code if hasattr(e, 'response') else None)
        
        if status == 401:
            raise TabAuthError
        else:
            raise
        
        
    
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
        result["spoke"] = False
        
        # getting data from round URL (already fetched tho)
        round_data = rounds_jsons[round["round"]]
        print("(2) gotten round data")
        
        round_motion_set = round_data["motions"]
        if len(round_motion_set) > 0:
            result["info_slide"] = round_motion_set[0]["info_slide_plain"]
            result["motion"] = round_motion_set[0]["text"]
        
        
        # get positions from motion draw
        pairings_data = pairings_jsons.get(round_data["_links"]["pairing"])
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
            speaker_score = max(speeches, key=lambda x: x["score"])["score"]
            results[round["round"]]["speaks"] = speaker_score
            results[round["round"]]["spoke"] = True
    
    return {
        "name": tourney_name,
        "results": list(results.values())
    }

    
        
           