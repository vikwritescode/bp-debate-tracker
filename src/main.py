from utils import *
import sys

def main():
    if len(sys.argv) < 4:
        print("e: too few arguments!")
        return
    tab_url = sys.argv[1]
    slug = sys.argv[2]
    name = sys.argv[3]
    s = get_speaker(tab_url, slug, name)[0] 
    r = get_results(tab_url, slug, s)[0]
    sp = get_speaks(tab_url, slug, s) 
    p = get_positions(tab_url, "_", r, s["team"])

    for round_ in r:
        round_["pos"] = p.get(round_["round"], "ABS")
        round_["speaks"] = sp.get(round_["round"], 0)
        print(
            f"speaker got {round_['points']} points and "
            f"{round_['speaks']} speaks as {round_['pos']} "
            f"in round {round_['round']}."
        )

if __name__ == "__main__":
    main()