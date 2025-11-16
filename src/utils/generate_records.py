from .get_speaker import get_speaker
from .get_results import get_results
from .get_positions import get_positions
from .get_speaks import get_speaks

def generate_records(tab_url, slug, name, index=0):
    records = []
    try:
        s_list = get_speaker(tab_url, slug, name)
        if len(s_list) <= index:
            raise RuntimeError("No Matching Speakers Found!")
        s = s_list[index]
    except Exception as e:
        raise RuntimeError("Could Not Fetch")
 
    r = get_results(tab_url, slug, s)[0]
    sp = get_speaks(tab_url, slug, s) 
    p = get_positions(tab_url, "_", r, s["team"])

    for round in r:
        records.append({"pos": p.get(round["round"], "ABS"), "points": round["points"], "speaks": sp.get(round["round"], 0)})
    return records
##        print(
##            f"speaker got {round['points']} points and "
##            f"{round['speaks']} speaks as {round['pos']} "
##            f"in round {round['round']}."