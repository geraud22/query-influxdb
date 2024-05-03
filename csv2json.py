import csv
import io

def dataFilter(jsonArray):
    filtered_data = []
    for item in jsonArray:
        filtered_item = {'sensor_value': item['_value'], 'uplink_time': item['_time']}
        filtered_data.append(filtered_item)
        
    return filtered_data

# Returns JSON Array
def csv_to_json(csvFile):
    jsonArray = []
    csvRows = list(csvFile)
    
    # Create Metadata row counter which increments each time a row starts with '#'
    skip_metadata = sum(1 for row in csvRows if row.startswith('#'))
    
    # Slice metadata out of csvRows. Cast it back to a file-like object that csv.DictReader can use. Create csvReader.
    csvReader = csv.DictReader(io.StringIO(''.join(csvRows[skip_metadata:])))
    
    for row in csvReader:
        jsonArray.append(row)

    return dataFilter(jsonArray)

def specifyRange(startRange, stopRange):
    if stopRange is None:
        return f"range( start: {startRange})"
    else:
        return f"range( start: {startRange}, stop: {stopRange})"