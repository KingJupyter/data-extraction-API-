import requests
import json
import threading
from time import sleep
import os

decision = input('Do you want to delete other files? Please input "yes" or "no" : ')

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

def api_step1_2():
    resultOffset = 0
    resultRecordCount = 2000
    all_data = []

    while True:
        response = requests.get(f'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Property_and_Land_WebMercator/MapServer/24/query?where=1%3D1&outFields=*&returnGeometry=false&resultOffset={resultOffset}&resultRecordCount={resultRecordCount}&outSR=4326&f=json')
        
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

    with open('output1_2.json', 'w') as file:
        json.dump(transformed_data, file, indent = 4)

    print(f'Step1_2. Condo : {len(transformed_data)}')

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

def api_step4():
    resultOffset = 0
    resultRecordCount = 2000
    all_data = []

    while True:
        response = requests.get(f'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/0/query?where=1%3D1&outFields=ADDRESS,MAR_ID&returnGeometry=false&resultOffset={resultOffset}&resultRecordCount={resultRecordCount}&outSR=4326&f=json')

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

    with open('output4.json', 'w') as file:
        json.dump(transformed_data, file, indent = 4)

    print(f'Step4. Address Points : {len(transformed_data)}')

def main():
    # Load the first JSON file
    with open('output3.json', 'r') as file:
        data_output3 = json.load(file)

    # Load the second JSON file
    with open('output1_1.json', 'r') as file:
        data_output1_1 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements1_1 = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output3:
        ssl_value1_1 = element1.get('SSL')
        if ssl_value1_1:
            matching_elements1_1[ssl_value1_1] = element1

    # Iterate through the elements in the second JSON file
    output_data1_1 = []
    for element2 in data_output1_1:
        ssl_value1_1 = element2.get('SSL')
        if ssl_value1_1 and ssl_value1_1 in matching_elements1_1:
            output_data1_1.append(matching_elements1_1[ssl_value1_1])

    with open('match1_1&3.json', 'w') as file:
        json.dump(output_data1_1, file, indent = 4)

    print(f'Extract MAR_ID using SSL(1_1 to 3) : {len(output_data1_1)}')

    # Create a dictionary mapping SSL values to MAR_ID values
    ssl_marid_map1_1 = {entry['SSL']: entry['MAR_ID'] for entry in data_output3}

    # Update the entries in the first data with MAR_ID values
    for entry in data_output1_1:
        ssl = entry['SSL']
        if ssl in ssl_marid_map1_1:
            entry['MAR_ID'] = ssl_marid_map1_1[ssl]

    filtered_data1_1 = [element for element in data_output1_1 if 'MAR_ID' in element]

    with open('addAddress_1.json', 'w') as file:
        json.dump(filtered_data1_1, file, indent = 4)

    print(f'Add address 1 : {len(filtered_data1_1)}')

    # Load the second JSON file
    with open('output1_2.json', 'r') as file:
        data_output1_2 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements1_2 = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output3:
        ssl_value1_2 = element1.get('SSL')
        if ssl_value1_2:
            matching_elements1_2[ssl_value1_2] = element1

    # Iterate through the elements in the second JSON file
    output_data1_2 = []
    for element2 in data_output1_2:
        ssl_value1_2 = element2.get('SSL')
        if ssl_value1_2 and ssl_value1_2 in matching_elements1_2:
            output_data1_2.append(matching_elements1_2[ssl_value1_2])

    with open('match1_2&3.json', 'w') as file:
        json.dump(output_data1_2, file, indent = 4)

    print(f'Extract MAR_ID using SSL(1_2 to 3) : {len(output_data1_2)}')

    # Create a dictionary mapping SSL values to MAR_ID values
    ssl_marid_map1_2 = {entry['SSL']: entry['MAR_ID'] for entry in data_output3}

    # Update the entries in the first data with MAR_ID values
    for entry in data_output1_2:
        ssl = entry['SSL']
        if ssl in ssl_marid_map1_2:
            entry['MAR_ID'] = ssl_marid_map1_2[ssl]

    filtered_data1_2 = [element for element in data_output1_2 if 'MAR_ID' in element]

    with open('addAddress_2.json', 'w') as file:
        json.dump(filtered_data1_2, file, indent = 4)

    print(f'Add address 2 : {len(filtered_data1_2)}')

    # Load the first JSON file
    with open('output4.json', 'r') as file:
        data_output4 = json.load(file)

    # Load the second JSON file
    with open('match1_1&3.json', 'r') as file:
        data_match1_1To3 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements1_1To3 = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output4:
        ssl_value = element1.get('MAR_ID')
        if ssl_value:
            matching_elements1_1To3[ssl_value] = element1

    # Iterate through the elements in the second JSON file
    output_data1_1To3 = []
    for element2 in data_match1_1To3:
        ssl_value = element2.get('MAR_ID')
        if ssl_value and ssl_value in matching_elements1_1To3:
            output_data1_1To3.append(matching_elements1_1To3[ssl_value])

    # Save the matching elements to a new JSON file
    with open('extractAddress_1.json', 'w') as file:
        json.dump(output_data1_1To3, file, indent = 4)

    print(f'Extract Address using MAR_ID 1 : {len(output_data1_1To3)}')

    # Load the second JSON file
    with open('match1_2&3.json', 'r') as file:
        data_match1_2To3 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements1_2To3 = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output4:
        ssl_value = element1.get('MAR_ID')
        if ssl_value:
            matching_elements1_2To3[ssl_value] = element1

    # Iterate through the elements in the second JSON file
    output_data1_2To3 = []
    for element2 in data_match1_2To3:
        ssl_value = element2.get('MAR_ID')
        if ssl_value and ssl_value in matching_elements1_2To3:
            output_data1_2To3.append(matching_elements1_2To3[ssl_value])

    # Save the matching elements to a new JSON file
    with open('extractAddress_2.json', 'w') as file:
        json.dump(output_data1_2To3, file, indent = 4)

    print(f'Extract Address using MAR_ID 2 : {len(output_data1_2To3)}')

    # Load data from the first JSON file
    with open('addAddress_1.json', 'r') as file:
        data_addAddress_1 = json.load(file)

    # Load data from the second JSON file
    with open('extractAddress_1.json', 'r') as file:
        data_extractAddress_1 = json.load(file)

    # Create a dictionary mapping SSL values to MAR_ID values
    marid_address_map1_1 = {entry['MAR_ID']: entry['ADDRESS'] for entry in data_extractAddress_1}

    # Update the entries in the first data with MAR_ID values
    for entry in data_addAddress_1:
        marid = entry['MAR_ID']
        if marid in marid_address_map1_1:
            entry['ADDRESS'] = marid_address_map1_1[marid]

    # Save the updated data to a new JSON file
    with open(f'Residential({len(data_addAddress_1)}).json', 'w') as file:
        json.dump(data_addAddress_1, file, indent = 4)

    print(f'Final result (Residential) 1 : {len(data_addAddress_1)}')

    # Load data from the first JSON file
    with open('addAddress_2.json', 'r') as file:
        data_addAddress_2 = json.load(file)

    # Load data from the second JSON file
    with open('extractAddress_2.json', 'r') as file:
        data_extractAddress_2 = json.load(file)

    # Create a dictionary mapping SSL values to MAR_ID values
    marid_address_map1_2 = {entry['MAR_ID']: entry['ADDRESS'] for entry in data_extractAddress_2}

    # Update the entries in the first data with MAR_ID values
    for entry in data_addAddress_2:
        marid = entry["MAR_ID"]
        if marid in marid_address_map1_2:
            entry['ADDRESS'] = marid_address_map1_2[marid]

    # Save the updated data to a new JSON file
    with open(f'Condo({len(data_addAddress_2)}).json', 'w') as file:
        json.dump(data_addAddress_2, file, indent = 4)

    print(f'Final result (Condo) 2 : {len(data_addAddress_2)}')

def delete_file():
    # Delete other JSON files.
    file_paths = [
        './output1_1.json',
        './output1_2.json',
        './output3.json',
        './output4.json',
        './match1_1&3.json',
        './match1_2&3.json',
        './addAddress_1.json',
        './addAddress_2.json',
        './extractAddress_1.json',
        './extractAddress_2.json',
        ]

    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been removed.")
        else:
            print('Failed run script.')

if __name__ == '__main__':
    # Create threads for each functions.
    thread1 = threading.Thread(target = api_step1_1)
    thread2 = threading.Thread(target = api_step1_2)
    thread3 = threading.Thread(target = api_step3)
    thread4 = threading.Thread(target = api_step4)

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    sleep(3)

    main()

    if decision == 'yes':
        delete_file()