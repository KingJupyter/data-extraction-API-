import json

def extractAddress_1():
    # Load the first JSON file
    with open('output4.json', 'r') as file:
        data_output4 = json.load(file)

    # Load the second JSON file
    with open('match1_1&3.json', 'r') as file:
        data_match1_1To3 = json.load(file)

    # Create a dictionary to store elements with matching "SSL" values
    matching_elements = {}

    # Iterate through the elements in the first JSON file
    for element1 in data_output4:
        ssl_value = element1.get('MAR_ID')
        if ssl_value:
            matching_elements[ssl_value] = element1

    # Iterate through the elements in the second JSON file
    output_data = []
    for element2 in data_match1_1To3:
        ssl_value = element2.get('MAR_ID')
        if ssl_value and ssl_value in matching_elements:
            output_data.append(matching_elements[ssl_value])

    # Save the matching elements to a new JSON file
    with open('extractAddress_1.json', 'w') as file:
        json.dump(output_data, file, indent = 4)

    print(f'Extract Address using MAR_ID 1 : {len(output_data)}')

if __name__ == '__main__':
    extractAddress_1()