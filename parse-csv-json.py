import csv
import json

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # Read CSV file and add rows to jsonArray
    with open(csvFilePath, 'r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            jsonArray.append(row)

    # Write JSON file
    with open(jsonFilePath, 'w') as jsonFile:
        json.dump(jsonArray, jsonFile, indent=4)

if __name__ == '__main__':
    # Example usage
    csv_to_json('data.csv', 'data.json')