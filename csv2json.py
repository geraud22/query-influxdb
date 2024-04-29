import csv
import io

# Returns JSON Array
def csv_to_json(csvFile, jsonFile):
    jsonArray = []
    csvRows = list(csvFile)
    
    # Create Metadata row counter which increments each time a row starts with '#'
    skip_metadata = sum(1 for row in csvRows if row.startswith('#'))
    
    # Slice metadata out of csvRows. Cast it back to a file-like object that csv.DictReader can use. Create csvReader.
    csvReader = csv.DictReader(io.StringIO(''.join(csvRows[skip_metadata:])))
    
    for row in csvReader:
        jsonArray.append(row)

    return jsonArray