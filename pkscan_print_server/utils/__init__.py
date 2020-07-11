import requests
import xmltodict
import pandas as pd
import os

def get_history():
    url = "http://192.168.1.198:30081/clrc/services/CLRC"
    payload = "<?xml version='1.0' encoding='UTF-8'?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header /><soapenv:Body><GetHistoryList xmlns=\"http://web.clrc.bskk.konicaminolta.jp/xsd\" /></soapenv:Body></soapenv:Envelope>"
    headers = {}
    response = requests.request("POST", url, headers=headers, data = payload)

    response_xml = response.text.encode('utf8')

    response_dict = xmltodict.parse(response_xml)["soapenv:Envelope"]["soapenv:Body"]
    response_dict = response_dict["ns:GetHistoryListResponse"]["ns:return"]
    history_list = xmltodict.parse(response_dict)["CommonAPI_Response"]["JobHistoryCtrl"]["HistoryList"]["History"]
    return history_list

def clean_history(history_list):
    df = pd.DataFrame(history_list)
    df = df[["@jobid", "@user", "@name", "@pages", "@printpages", "@pagesmono", "@pagescolor",
             "@copies", "@printtime"]]
    df.columns = ["ID", "User", "Name", "Pages", "Total Prints", "B/W Pages", "Colour Pages",
                  "Copies", "DateTime"]
    df = df[["ID", "User", "Name", "Pages", "B/W Pages", "Colour Pages",
             "Copies", "Total Prints", "DateTime"]]
    df = df[df["Total Prints"] != ""]
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df = df.sort_values(by="ID", ascending=True)
    df["Total Prints"] = df["Total Prints"].astype(int)
    df["ID"] = df["ID"].astype(int)
    df["Paper Name"] = df["Name"].str.extract(".*\((.*)\).*").fillna("")
    df["Amount"] = df["Name"].str.extract(".*\[(.*)\].*").fillna("")
    return df

class Convert:
    def __init__(self, filename):
        self.filename = filename

    def paper(self):
        df = pd.read_csv(self.filename)
        df = df.groupby(['Paper Name'])["Total Prints"].sum()
        df = df.to_frame().reset_index()
        directory = os.path.split(self.filename)[0]
        df.to_csv(os.path.join(directory, "paper_report.csv"), index=False)
        print("Converted")

    def paper_daily(self):
        df = pd.read_csv(self.filename, parse_dates=["DateTime"], infer_datetime_format=True)
        df["Date"] = df["DateTime"].dt.date
        df = df.groupby(['Date','Paper Name'])["Total Prints"].sum()
        df = df.to_frame().reset_index()
        directory = os.path.split(self.filename)[0]
        df = df.sort_values(by=["Date", "Paper Name"], ascending=False)
        df.to_csv(os.path.join(directory, "paper_daily_report.csv"), index=False)
        print("Converted")

    def paper_monthly(self):
        df = pd.read_csv(self.filename, parse_dates=["DateTime"], infer_datetime_format=True)
        df["Month"] = df["DateTime"].dt.strftime('%m/%Y')
        df = df.groupby(['Month','Paper Name'])["Total Prints"].sum()
        df = df.to_frame().reset_index()
        directory = os.path.split(self.filename)[0]
        df = df.sort_values(by=["Month", "Paper Name"], ascending=False)
        df.to_csv(os.path.join(directory, "paper_monthly_report.csv"), index=False)
        print("Converted")

    def counter_daily(self):
        df = pd.read_csv(self.filename, parse_dates=["DateTime"], infer_datetime_format=True)
        df["Date"] = df["DateTime"].dt.date
        df = df.groupby(['Date']).agg({"Colour Pages": "sum",
                                       "B/W Pages": "sum",
                                       "Total Prints": "sum"})
        df = df.reset_index()
        directory = os.path.split(self.filename)[0]
        df = df.sort_values(by=["Date"], ascending=False)
        df.to_csv(os.path.join(directory, "counter_daily_report.csv"), index=False)
        print("Converted")
        
    

if __name__ == "__main__":
    history = get_history()
    print(clean_history(history))
