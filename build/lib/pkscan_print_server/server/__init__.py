import pandas as pd
from pkscan_print_server.utils import get_history, clean_history
import os
import time

def start(counter=None, filename="C://print_logs/logs.csv"):
    while(True):
        history = get_history()
        history = clean_history(history)
        if os.path.isfile(filename):
            past_history = pd.read_csv(filename, infer_datetime_format=True)
            history = pd.concat([history, past_history])
        try:
            history.to_csv(filename, index=False)
        except:
            print("Close the file")
            time.sleep(10)
            continue
        time.sleep(10)


if __name__ == "__main__":
    start()