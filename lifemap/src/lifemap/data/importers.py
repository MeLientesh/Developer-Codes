def import_data_from_csv(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    return data.to_dict(orient='records')

def import_data_from_json(file_path):
    import json
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def import_data_from_excel(file_path):
    import pandas as pd
    data = pd.read_excel(file_path)
    return data.to_dict(orient='records')

def import_data_from_api(api_url):
    import requests
    response = requests.get(api_url)
    return response.json()