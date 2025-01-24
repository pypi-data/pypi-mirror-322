from pyspark.sql import DataFrame
from datetime import datetime, time
from gspread import service_account_from_dict
from typing import List, Any, Dict, Tuple


class GPP:
    """Gspread Plus Plus (GPP) class for enhanced Google Sheets operations."""

    @staticmethod
    def _init_sheets_client(spreadsheet_id: str, sheet_name: str, creds_json: Dict, create_sheet: bool = True) -> Tuple[
        Any, Any]:
        """Initialize Google Sheets client and get worksheet."""
        client = service_account_from_dict(creds_json)
        spreadsheet = client.open_by_key(spreadsheet_id)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except Exception as e:
            if create_sheet:
                worksheet = spreadsheet.add_worksheet(sheet_name, 1, 1)  # Default size: 1000 rows, 26 columns
            else:
                raise ValueError(f"Sheet '{sheet_name}' does not exist and create_sheet is False") from e

        return client, worksheet

    @staticmethod
    def _convert_value(value: Any, dtype: str) -> Any:
        """Convert Spark SQL types to appropriate Python types for Google Sheets."""
        dtype = dtype.lower()

        if value is None:
            return 0 if dtype in ["bigint", "long", "double", "decimal", "float"] else ""

        type_handlers = {
            "string": lambda x: str(x),
            "bigint": lambda x: int(x),
            "long": lambda x: int(x),
            "integer": lambda x: int(x),
            "int": lambda x: int(x),
            "tinyint": lambda x: int(x),
            "smallint": lambda x: int(x),
            "short": lambda x: int(x),
            "double": lambda x: round(float(x), 2),
            "float": lambda x: round(float(x), 2),
            "decimal": lambda x: round(float(x), 2),
            "timestamp": lambda x: x.isoformat(),
            "date": lambda x: datetime.combine(x, time.min).isoformat(),
            "boolean": lambda x: bool(x)
        }

        if dtype not in type_handlers:
            raise ValueError(f"Unsupported data type: {dtype}")

        return type_handlers[dtype](value)

    @staticmethod
    def _prepare_data(df: DataFrame, keep_header: bool) -> Tuple[List[List[Any]], List[int], List[str]]:
        """Convert DataFrame to list of lists with proper type conversion."""
        date_columns = [i for i, field in enumerate(df.schema)
                        if field.dataType.typeName().lower() == "date"]

        data = df.collect()
        header = df.columns
        converted_data = [] if keep_header else [header]

        for row in data:
            converted_row = [
                GPP._convert_value(value, df.schema[i].dataType.typeName())
                for i, value in enumerate(row)
            ]
            converted_data.append(converted_row)

        return converted_data, date_columns, header

    @staticmethod
    def _clear_sheet_data(worksheet: Any, current_rows: int, required_cols: int,
                          start_row: int, erase_whole: bool) -> None:
        """Clear sheet data based on parameters."""
        if current_rows >= start_row:
            if erase_whole:
                worksheet.batch_clear([f"{start_row}:{current_rows}"])
            else:
                end_col = chr(64 + required_cols)
                worksheet.batch_clear([f"A{start_row}:{end_col}{current_rows}"])

    @staticmethod
    def _format_date_columns(client: Any, worksheet: Any, date_columns: List[int],
                             start_row: int, required_rows: int) -> None:
        """Format date columns with proper date format."""
        if not date_columns:
            return

        spreadsheet = client.open_by_key(worksheet.spreadsheet.id)
        format_requests = [{
            "requests": [{
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": start_row - 1,
                        "endRowIndex": required_rows,
                        "startColumnIndex": col_idx,
                        "endColumnIndex": col_idx + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "DATE",
                                "pattern": "yyyy-mm-dd"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            }]
        } for col_idx in date_columns]

        for request in format_requests:
            spreadsheet.batch_update(request)

    @staticmethod
    def df_to_sheets(
            df: DataFrame,
            spreadsheet_id: str,
            sheet_name: str,
            creds_json: Dict,
            english_locale: bool = False,
            keep_header: bool = False,
            erase_whole: bool = True,
            create_sheet: bool = True
    ) -> None:
        """
        Transfer data from Spark DataFrame to Google Sheets while preserving column structure.

        Args:
            df: Spark DataFrame containing the data to transfer
            spreadsheet_id: The ID of the Google Spreadsheet (from the URL)
            sheet_name: Name of the worksheet to update
            creds_json: Dictionary containing Google service account credentials
            english_locale: If True, use '.' as decimal separator, if False use ','
            keep_header: If True, preserve the first row of the sheet
            erase_whole: If True, clear all columns and rows (maybe skipping first based on keep_header)
            create_sheet: If True, create the sheet if it doesn't exist. If False, raise an error
        """
        client, worksheet = GPP._init_sheets_client(spreadsheet_id, sheet_name, creds_json, create_sheet)
        converted_data, date_columns, header = GPP._prepare_data(df, keep_header)

        current_rows = len(worksheet.col_values(1))
        required_rows = len(converted_data) + (1 if keep_header else 0)
        required_cols = len(header)
        start_row = 2 if keep_header else 1

        GPP._clear_sheet_data(worksheet, current_rows, required_cols, start_row, erase_whole)

        if current_rows < required_rows:
            worksheet.add_rows(required_rows - current_rows)

        update_range = f'A2:{chr(64 + required_cols)}{len(converted_data) + 1}' if keep_header else 'A1'
        worksheet.update(update_range, converted_data, value_input_option='USER_ENTERED')

        GPP._format_date_columns(client, worksheet, date_columns, start_row, required_rows)
        worksheet.resize(rows=max(required_rows, 1))

    @staticmethod
    def set_config(spreadsheet_id: str, key: str, value: str, creds_json: Dict, sheet_name: str = "CONFIG") -> int:
        """
        Find a key in column A of the specified sheet and update its corresponding value in column B.

        Args:
            spreadsheet_id: The ID of the Google Spreadsheet
            key: The key to search for in column A
            value: The value to set in column B
            creds_json: Dictionary containing Google service account credentials
            sheet_name: Name of the worksheet (defaults to "CONFIG")

        Returns:
            int: 0 if successful, 1 if an error occurs
        """
        try:
            # Initialize the client and get the worksheet
            client, worksheet = GPP._init_sheets_client(spreadsheet_id, sheet_name, creds_json)

            # Get all values from column A
            keys = worksheet.col_values(1)  # Column A

            # Find the row number for the key
            try:
                row_num = keys.index(key) + 1  # Adding 1 because sheets are 1-indexed
            except ValueError:
                # Key not found, append new row
                row_num = len(keys) + 1
                worksheet.update(f'A{row_num}', [[key]])

            # Update the value in column B
            worksheet.update(f'B{row_num}', [[value]])

            return 0

        except Exception as e:
            print(f"Error in set_config: {str(e)}")
            return 1

    @staticmethod
    def debug(text="This is debug"):
        print(text)