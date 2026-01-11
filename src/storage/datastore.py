import pandas as pd
class DataStore:
    def __init__(self):
        pass
    def make_new(self):
        # create a frame
        self.__store = pd.DataFrame(columns=["pos", "points", "speaks"])
    def load_from_pickle(self, filepath: str):
        self.__store = pd.read_pickle(filepath)
    def get_store(self):
        return self.__store
    def store_to_pickle(self, filepath: str):
        self.__store.to_pickle(filepath)
    def add_entries(self, entries: list):
        temp_df = pd.DataFrame(entries)
        if not temp_df.empty:
            self.__store = pd.concat([self.__store, temp_df], ignore_index=True)
    
    def get_position_averages(self):
        return self.__store.groupby(["pos"]).mean()