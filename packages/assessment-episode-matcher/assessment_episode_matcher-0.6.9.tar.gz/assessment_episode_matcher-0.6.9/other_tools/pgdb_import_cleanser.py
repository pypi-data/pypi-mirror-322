import csv
import json

def strip_problematic_fields(input_file, output_file):
    with open(input_file, 'r', encoding='windows-1252', errors='replace') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        
        # Filter out problematic field names
        fieldnames = [field for field in reader.fieldnames 
                      if not any(problematic in field 
                                 for problematic in ["Notes", "Comments", "Goals", "Issues"])]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Handle the SurveyData field specially
            if 'SurveyData' in row:
                try:
                    survey_data = json.loads(row['SurveyData'])
                    filtered_survey_data = {k: v for k, v in survey_data.items() 
                                            if not any(problematic in k 
                                                       for problematic in ["Notes", "Comments", "Goals", "Issues"])}
                    row['SurveyData'] = json.dumps(filtered_survey_data)
                except json.JSONDecodeError:
                    # If SurveyData is not valid JSON, leave it as is
                    pass
            
            # Write only the non-problematic fields
            filtered_row = {field: row[field] for field in fieldnames}
            writer.writerow(filtered_row)

# Usage
input_file = r'C:\Users\aftab.jalal\Downloads\ATOM_Jul2020-Oct2024.csv'
output_file = r'C:\Users\aftab.jalal\Downloads\ATOM_Jul2020-Oct2024.csv_cleaned.csv'
strip_problematic_fields(input_file, output_file)