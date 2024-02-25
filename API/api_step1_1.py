import requests
import json

def api_step1_1():
    resultOffset = 0
    resultRecordCount = 2000
    all_data = []

    while True:
        response = requests.get(f'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Property_and_Land_WebMercator/MapServer/25/query?where=1%3D1&outFields=*&returnGeometry=false&resultOffset={resultOffset}&resultRecordCount={resultRecordCount}&outSR=4326&f=json')

        # Check the response status code.
        if response.status_code == 200:
            data = response.json()
            records = data.get("features", [])
            # print(len(records))
            all_data.extend(records)
        else:
            # An error occurred.
            print("Error sending message: {}".format(response.status_code))

        if len(records) < resultRecordCount:
            break

        resultOffset += resultRecordCount

    transformed_data = []
    for item in all_data:
        attributes = item.get('attributes', {})
        transformed_data.append(attributes)

    with open('output1_1.json', 'w') as file:
        json.dump(transformed_data, file, indent = 4)

    print(f'Step1_1. Residential : {len(transformed_data)}')

if __name__ == '__main__':
    api_step1_1()