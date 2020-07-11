import pandas as pd
from pkscan_print_server.utils import get_history, clean_history
import os
import time
from shutil import copyfile

def start(filename, backup_filename):
    print("Creating a backup")
    copyfile(filename, backup_filename)
    while(True):
        print("Pinging -->", end=" ")
        history = get_history()
        history = clean_history(history)
        max_counter = 0
        past_history = None
        if type(past_history) is not pd.DataFrame:
            if os.path.isfile(filename):
                print("Reading from machine -->", end=" ")
                past_history = pd.read_csv(filename, parse_dates=["DateTime"], infer_datetime_format=True)
                max_past_id = past_history["ID"].max()
                max_counter = past_history["Counter"].max()
                history = history[history["ID"] > max_past_id]
        else:
            max_past_id = past_history["ID"].max()
            max_counter = past_history["Counter"].max()
            history = history[history["ID"] > max_past_id]
        history["Counter"] = history["Total Prints"].cumsum() + max_counter
        history = history[::-1]
        if type(past_history) is pd.DataFrame:
            print("found ", str(len(history)), " new", " rows -->", end=" ")
            history = pd.concat([history, past_history])
        history.to_csv(filename, index=False)
        print("Going to sleep")
        time.sleep(60)
        past_history = history.copy(deep=True)


if __name__ == "__main__":
    start()
