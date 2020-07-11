import requests
import xmltodict
import pandas as pd

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
    df = df.sort_values(by="ID", ascending=False)
    return df

if __name__ == "__main__":
    history = get_history()
    print(clean_history(history))