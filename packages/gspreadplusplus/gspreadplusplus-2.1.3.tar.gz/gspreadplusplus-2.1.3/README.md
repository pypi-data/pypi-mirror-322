# gspreadplusplus

A Python library that enhances Google Sheets operations with additional functionality and improved data type handling.

## Features

- Transfer Spark DataFrames to Google Sheets with proper type conversion
- Intelligent handling of various data types (numbers, dates, timestamps, etc.)
- Preserve or update sheet headers
- Selective column clearing options
- Automatic date formatting
- Sheet dimension management
- Configuration management with key-value storage

## Installation

```bash
pip install gspreadplusplus
```

## Requirements

- Python 3.7+
- gspread
- pyspark
- google-auth

## Usage

### Basic DataFrame Export

```python
from gspreadplusplus import GPP
from pyspark.sql import SparkSession

# Initialize Spark and create a DataFrame
spark = SparkSession.builder.appName("example").getOrCreate()
df = spark.createDataFrame([
    ("2024-01-01", 100, "Complete"),
    ("2024-01-02", 150, "Pending")
], ["date", "amount", "status"])

# Your Google Sheets credentials
creds_json = {
    "type": "service_account",
    # ... rest of your service account credentials
}

# Export DataFrame to Google Sheets
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json
)
```

### Advanced DataFrame Export Options

```python
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json,
    english_locale=True,  # Use '.' as decimal separator
    keep_header=True,     # Preserve existing header row
    erase_whole=False     # Clear only necessary columns
)
```

### Configuration Management

The library provides functionality to store and update configuration values in a Google Sheet. By default, it uses a sheet named "CONFIG" with keys in column A and values in column B.

```python
# Store or update a configuration value
result = GPP.set_config(
    spreadsheet_id="your_spreadsheet_id",
    key="api_endpoint",
    value="https://api.example.com",
    creds_json=creds_json,
    sheet_name="CONFIG"  # Optional, defaults to "CONFIG"
)

if result == 0:
    print("Configuration updated successfully")
else:
    print("Error updating configuration")
```

The `set_config` function will:
- Search for the key in column A
- If found, update the corresponding value in column B
- If not found, append a new row with the key-value pair
- Return 0 on success, 1 on error

## Data Type Support

The library automatically handles conversion of various data types:

- Strings
- Integers (regular, long, bigint)
- Floating point numbers (double, float)
- Decimals
- Dates
- Timestamps
- Booleans

Null values are converted to:
- 0 for numeric types
- Empty string for other types

## Error Handling

The library implements comprehensive error handling:
- Returns status codes for operations (0 for success, 1 for failure)
- Prints detailed error messages for debugging
- Gracefully handles missing keys, sheet access issues, and credential problems

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
