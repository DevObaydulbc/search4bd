# Bangladesh Geocode - Combined Dataset

This folder contains combined datasets that merge all administrative levels (Union → Upazila → District → Division) into single comprehensive files.

## Usage

### CSV with Python
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('bangladesh_geocode_combined.csv')

# Find all unions in Dhaka division
dhaka_unions = df[df['division_name_en'] == 'Dhaka']
print(f"Found {len(dhaka_unions)} unions in Dhaka")

# Get complete path for a union
subil = df[df['union_name_en'] == 'Subil']
print(subil[['union_name_en', 'upazila_name_en', 'district_name_en', 'division_name_en']])
```

### JSON with JavaScript
```javascript
fetch('bangladesh_geocode_combined.json')
  .then(response => response.json())
  .then(data => {
    // Filter by division
    const chittagong = data.filter(item => 
      item.division_name_en === 'Chattagram'
    );
    console.log(`${chittagong.length} unions in Chattagram`);
  });
```

### SQL
```sql
-- Import the file
source bangladesh_geocode_combined.sql;

-- Count unions by division
SELECT division_name_en, COUNT(*) as unions
FROM bangladesh_geocode_combined 
GROUP BY division_name_en;

-- Find areas by coordinates
SELECT union_name_en, district_name_en
FROM bangladesh_geocode_combined 
WHERE district_latitude BETWEEN 23.0 AND 24.0;
```
