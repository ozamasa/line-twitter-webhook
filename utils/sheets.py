import gspread
import json
import os

def append_to_sheet(row_data):
    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_json:
        print("[Error] GOOGLE_CREDENTIALS is missing.")
        return

    creds = json.loads(credentials_json)
    gc = gspread.service_account_from_dict(creds)

    # スプレッドシートIDとシート名を設定
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    SHEET_NAME = "シート1"

    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)

    worksheet.append_row(row_data, value_input_option="USER_ENTERED")
    print("[Sheets] Row appended:", row_data)