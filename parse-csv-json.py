import csv
import json
import io

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    with open(csvFilePath, 'r') as csvFile:
        #Read csvRows into memory
        csvRows = list(csvFile)
        
        # Create Metadata row counter which increments each time a row starts with '#'
        skip_metadata = sum(1 for row in csvRows if row.startswith('#'))
        
        # Slice metadata out of csvRows. Cast it back to a file-like object that csv.DictReader can use. Create csvReader.
        csvReader = csv.DictReader(io.StringIO(''.join(csvRows[skip_metadata:])))
        
        for row in csvReader:
            jsonArray.append(row)

    # Write JSON file
    with open(jsonFilePath, 'w') as jsonFile:
        json.dump(jsonArray, jsonFile, indent=4)

if __name__ == '__main__':
    # Example usage
    csv_to_json('flow-meter-3h.csv', 'flow-meter(1).json')