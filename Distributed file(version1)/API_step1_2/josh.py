import requests

# API endpoint
# url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Property_and_Land_WebMercator/MapServer/25/query"
url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/0/query"

# Parameters for the API request
params = {
    "where" : "1=1",
    "outFields" : "*",
    "outSR" : "4326",
    "f" : "json",
    "returnGeometry" : "false",
    "resultOffset" : 0,
    "resultRecordCount" : 2000  # Adjust if the API allows more/less
}

# Function to fetch data
def fetch_data(url, params):
    response = requests.get(url, params = params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Main loop to paginate through the data
def main():
    all_data = []
    while True:
        data = fetch_data(url, params)
        records = data.get("features", [])
        all_data.extend(records)

        if len(records) < params["resultRecordCount"]:
            break

        params["resultOffset"] += params["resultRecordCount"]

    return all_data

# Run the script
try:
    data = main()
    # This line prints the total number of records fetched
    print(f"Total records fetched: {len(data)}")
except Exception as e:
    print(str(e))