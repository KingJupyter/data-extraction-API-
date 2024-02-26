import json

def addAddress_2():
    # Load data from the first JSON file
    with open('addAddress_2.json', 'r') as file:
        data_addAddress_2 = json.load(file)

    # Load data from the second JSON file
    with open('extractAddress_2.json', 'r') as file:
        data_extractAddress_2 = json.load(file)

    # Create a dictionary mapping SSL values to MAR_ID values
    marid_address_map = {entry['MAR_ID']: entry['ADDRESS'] for entry in data_extractAddress_2}

    # Update the entries in the first data with MAR_ID values
    for entry in data_addAddress_2:
        marid = entry["MAR_ID"]
        if marid in marid_address_map:
            entry['ADDRESS'] = marid_address_map[marid]

    # Save the updated data to a new JSON file
    with open(f'Condo({len(data_addAddress_2)}).json', 'w') as file:
        json.dump(data_addAddress_2, file, indent = 4)

    print(f'Final result (Condo) 2 : {len(data_addAddress_2)}')

if __name__ == '__main__':
    addAddress_2()