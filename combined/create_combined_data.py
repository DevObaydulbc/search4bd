import csv
import json
import os
from collections import defaultdict

def read_csv_data(filepath):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Remove quotes from each field
                cleaned_row = [field.strip('"') for field in row]
                data.append(cleaned_row)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return data

def create_combined_dataset():
    
    print("Reading data files...")
    divisions_data = read_csv_data('../divisions/divisions.csv')
    districts_data = read_csv_data('../districts/districts.csv')
    upazilas_data = read_csv_data('../upazilas/upazilas.csv')
    unions_data = read_csv_data('../unions/unions.csv')
    

    divisions = {}
    for div in divisions_data:
        if len(div) >= 4:
            divisions[div[0]] = {
                'id': div[0],
                'name_en': div[1],
                'name_bn': div[2],
                'website': div[3]
            }
    
    districts = {}
    for dist in districts_data:
        if len(dist) >= 7:
            districts[dist[0]] = {
                'id': dist[0],
                'division_id': dist[1],
                'name_en': dist[2],
                'name_bn': dist[3],
                'latitude': dist[4],
                'longitude': dist[5],
                'website': dist[6]
            }
    
    upazilas = {}
    for upz in upazilas_data:
        if len(upz) >= 5:
            upazilas[upz[0]] = {
                'id': upz[0],
                'district_id': upz[1],
                'name_en': upz[2],
                'name_bn': upz[3],
                'website': upz[4]
            }
    
    # Create combined dataset
    print("Creating combined dataset...")
    combined_data = []
    
    csv_header = [
        'union_id', 'union_name_en', 'union_name_bn', 'union_website',
        'upazila_id', 'upazila_name_en', 'upazila_name_bn', 'upazila_website',
        'district_id', 'district_name_en', 'district_name_bn', 'district_latitude', 'district_longitude', 'district_website',
        'division_id', 'division_name_en', 'division_name_bn', 'division_website'
    ]
    
    combined_data.append(csv_header)
    
    for union in unions_data:
        if len(union) >= 5:
            union_id, upazila_id, union_name_en, union_name_bn, union_website = union
            
            # Get upazila info
            upazila_info = upazilas.get(upazila_id, {})
            district_id = upazila_info.get('district_id', '')
            
            # Get district info
            district_info = districts.get(district_id, {})
            division_id = district_info.get('division_id', '')
            
            # Get division info
            division_info = divisions.get(division_id, {})
            
            # Create combined row - Bottom-up: Union → Upazila → District → Division
            row = [
                union_id,
                union_name_en,
                union_name_bn,
                union_website,
                upazila_id,
                upazila_info.get('name_en', ''),
                upazila_info.get('name_bn', ''),
                upazila_info.get('website', ''),
                district_id,
                district_info.get('name_en', ''),
                district_info.get('name_bn', ''),
                district_info.get('latitude', ''),
                district_info.get('longitude', ''),
                district_info.get('website', ''),
                division_id,
                division_info.get('name_en', ''),
                division_info.get('name_bn', ''),
                division_info.get('website', '')
            ]
            combined_data.append(row)
    
    return combined_data

def save_as_csv(data, filename):

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            writer.writerow(row)
    print(f"CSV saved as: {filename}")

def save_as_json(data, filename):

    header = data[0]
    json_data = []
    
    for row in data[1:]:
        record = {}
        for i, value in enumerate(row):
            if i < len(header):
                record[header[i]] = value
        json_data.append(record)
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)
    print(f"JSON saved as: {filename}")

def save_as_sql(data, filename):
    header = data[0]
    
    with open(filename, 'w', encoding='utf-8') as file:

        file.write("-- Bangladesh Complete Geocode Data\n")
        file.write("-- Combined dataset with all administrative levels\n\n")
        file.write("CREATE TABLE IF NOT EXISTS `bangladesh_geocode_combined` (\n")
        

        columns = [
            "  `id` int(11) NOT NULL AUTO_INCREMENT,",
            "  `union_id` varchar(10) DEFAULT NULL,",
            "  `union_name_en` varchar(255) DEFAULT NULL,",
            "  `union_name_bn` varchar(255) DEFAULT NULL,",
            "  `union_website` varchar(255) DEFAULT NULL,",
            "  `upazila_id` varchar(10) DEFAULT NULL,",
            "  `upazila_name_en` varchar(255) DEFAULT NULL,",
            "  `upazila_name_bn` varchar(255) DEFAULT NULL,",
            "  `upazila_website` varchar(255) DEFAULT NULL,",
            "  `district_id` varchar(10) DEFAULT NULL,",
            "  `district_name_en` varchar(255) DEFAULT NULL,",
            "  `district_name_bn` varchar(255) DEFAULT NULL,",
            "  `district_latitude` decimal(10,8) DEFAULT NULL,",
            "  `district_longitude` decimal(11,8) DEFAULT NULL,",
            "  `district_website` varchar(255) DEFAULT NULL,",
            "  `division_id` varchar(10) DEFAULT NULL,",
            "  `division_name_en` varchar(255) DEFAULT NULL,",
            "  `division_name_bn` varchar(255) DEFAULT NULL,",
            "  `division_website` varchar(255) DEFAULT NULL,",
            "  PRIMARY KEY (`id`)",
        ]
        
        file.write("\n".join(columns))
        file.write("\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n")
        

        file.write("INSERT INTO `bangladesh_geocode_combined` (\n")
        file.write("  `" + "`, `".join(header) + "`\n")
        file.write(") VALUES\n")
        
        for i, row in enumerate(data[1:], 1):

            formatted_values = []
            for value in row:
                if value == '' or value is None:
                    formatted_values.append('NULL')
                else:

                    escaped_value = str(value).replace("'", "\\'").replace('"', '\\"')
                    formatted_values.append(f"'{escaped_value}'")
            
            line = "(" + ", ".join(formatted_values) + ")"
            if i < len(data) - 1:
                line += ","
            else:
                line += ";"
            file.write(line + "\n")
    
    print(f"SQL saved as: {filename}")

def main():
    """Main function"""
    print("Bangladesh Geocode Combined Dataset Creator")
    print("============================================")
    

    combined_data = create_combined_dataset()
    
    if not combined_data:
        print("Error: No data to process")
        return
    
    print(f"Generated {len(combined_data)-1} records (plus header)")
    
    save_as_csv(combined_data, 'bangladesh_geocode_combined.csv')
    save_as_json(combined_data, 'bangladesh_geocode_combined.json')
    save_as_sql(combined_data, 'bangladesh_geocode_combined.sql')
    
    print("\nAll files created successfully!")
    print("\nFiles generated:")
    print("- bangladesh_geocode_combined.csv")
    print("- bangladesh_geocode_combined.json")
    print("- bangladesh_geocode_combined.sql")

if __name__ == "__main__":
    main()

