import requests
import json

def api_step3():
    resultOffset = 0
    resultRecordCount = 2000
    all_data = []

    while True:
        response = requests.get(f'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/7/query?where=1%3D1&outFields=SSL,MARID&returnGeometry=false&resultOffset={resultOffset}&resultRecordCount={resultRecordCount}&outSR=4326&f=json')

        # Check the response status code.
        if response.status_code == 200:
            data = response.json()
            records = data.get("features", [])

            # Modify the key name 'MARID' to 'MAR_ID' in each record
            for record in records:
                attributes = record.get("attributes", {})
                if 'MARID' in attributes:
                    attributes['MAR_ID'] = attributes.pop('MARID')

            # Add the records to the list.
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

    with open('output3.json', 'w') as file:
        json.dump(transformed_data, file, indent = 4)

    print(f'Step3. Address and Suffix Lot Cross Reference : {len(transformed_data)}')

if __name__ == '__main__':
    api_step3()