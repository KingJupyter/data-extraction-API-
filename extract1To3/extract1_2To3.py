import json

def extract1_2To3():
    # Load the first JSON file
    with open('output3.json', 'r') as file:
        data_output3 = json.load(file)

    # Load the second JSON file
    with open('output1_2.json', 'r') as file:
        data_output1_2 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output3:
        ssl_value = element1.get('SSL')
        if ssl_value:
            matching_elements[ssl_value] = element1

    # Iterate through the elements in the second JSON file
    output_data = []
    for element2 in data_output1_2:
        ssl_value = element2.get('SSL')
        if ssl_value and ssl_value in matching_elements:
            output_data.append(matching_elements[ssl_value])

    with open('match1_2&3.json', 'w') as file:
        json.dump(output_data, file, indent = 4)

    print(f'Extract MAR_ID using SSL(1_2 to 3) : {len(output_data)}')

    # Create a dictionary mapping SSL values to MAR_ID values
    ssl_marid_map = {entry['SSL']: entry['MAR_ID'] for entry in data_output3}

    # Update the entries in the first data with MAR_ID values
    for entry in data_output1_2:
        ssl = entry['SSL']
        if ssl in ssl_marid_map:
            entry['MAR_ID'] = ssl_marid_map[ssl]

    filtered_data = [element for element in data_output1_2 if 'MAR_ID' in element]

    with open('addAddress_2.json', 'w') as file:
        json.dump(filtered_data, file, indent = 4)

    print(f'Add address 2 : {len(filtered_data)}')

if __name__ == '__main__':
    extract1_2To3()