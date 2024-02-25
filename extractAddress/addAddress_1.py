import json

def addAddress_1():
    # Load data from the first JSON file
    with open('addAddress_1.json', 'r') as file:
        first_data = json.load(file)

    # Load data from the second JSON file
    with open('extractAddress_1.json', 'r') as file:
        second_data = json.load(file)

    # Create a dictionary mapping SSL values to MAR_ID values
    marid_address_map = {entry['MAR_ID']: entry['ADDRESS'] for entry in second_data}

    # Update the entries in the first data with MAR_ID values
    for entry in first_data:
        marid = entry['MAR_ID']
        if marid in marid_address_map:
            entry['ADDRESS'] = marid_address_map[marid]

    # Save the updated data to a new JSON file
    with open(f'Residential({len(first_data)}).json', 'w') as file:
        json.dump(first_data, file, indent = 4)

    print(f'Final result (Residential) 1 : {len(first_data)}')

if __name__ == '__main__':
    addAddress_1()