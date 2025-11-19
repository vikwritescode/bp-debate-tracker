from utils import *
from storage import *
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("e: too few arguments!")
        return
    
    PICKLE_PATH = "perf.pkl"
    
    tab_url = sys.argv[1]
    name = sys.argv[2]
    
    slugs = get_slugs(tab_url)
    if len(slugs) < 1:
        print("There are no tournaments.")
        return
    slug_index = -1
    if len(slugs) > 1:
        print(f"There are multiple tournaments.")
        print("".join([f"{i}: {slug}\n" for i, slug in enumerate(slugs)]))
        valid_slug = False
        
        while not valid_slug:
            try:
                slug_index = int(input("select an entry\n> "))
            except Exception as e:
                    pass
            if slug_index >= 0 and slug_index < len(slugs):
                    valid_slug = True
                    
    slug = slugs[slug_index]
    
    
    s_list = get_speaker(tab_url, slug, name)
    index = -1
    if len(s_list) == 0:
        print("no such speaker")
        return
    if len(s_list) > 1:
            print(f"There are multiple speakers.")
            print("".join([f"{i}: {speaker["name"]}\n" for i, speaker in enumerate(s_list)]))
            valid_input = False
            while not valid_input:
                try:
                    index = int(input("select an entry\n> "))
                except Exception as e:
                    pass
                if index >= 0 and index < len(s_list):
                    valid_input = True
    
    new_records = generate_records(tab_url, slug, name, (0 if index == -1 else index))
    
    perf = DataStore()
    # if there are records, 
    if Path(PICKLE_PATH).is_file():
        perf.load_from_pickle(PICKLE_PATH)
        print("loading from pickle")
    else:
        perf.make_new()
    perf.add_entries(new_records)
    print(perf.get_store())
    perf.store_to_pickle(PICKLE_PATH)
if __name__ == "__main__":
    main()