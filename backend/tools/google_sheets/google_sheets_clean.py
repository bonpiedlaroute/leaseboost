#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime,timedelta

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


def delete_old_rows(spreadsheet_id, sheet_name, date_filter_column, days_threshold, credentials_json):


    # authentication with account service
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scopes)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # reading all values
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values = result.get('values', [])


    if not values:
        print("no data found.")
        return
    
    header = values[0]

    try:
        date_col_idx = header.index(date_filter_column)
    except ValueError:
        print(f"column {date_filter_column} not found")
        return
    
    cutoff_date = datetime.today() - timedelta(days=days_threshold)

    rows_to_delete = []

    for i, row in enumerate(values[1:], start=2):
        if len(row) > date_col_idx:
            date_str = row[date_col_idx][:10]

            try:
                d = datetime.strptime(date_str, "%Y-%m-%d")
                if d < cutoff_date:
                    rows_to_delete.append(i)
            except Exception as e:
                print(f"error parsing line  {i}: {e}")
    
    if not rows_to_delete:
        print("no rows to delete")
        return
    

    # to avoid shift we delete in reverse order
    rows_to_delete.sort(reverse=True)

    spreadsheet = sheet.get(spreadsheetId=spreadsheet_id).execute()

    sheets = spreadsheet.get('sheets', [])
    sheet_id = None

    for s in sheets:
        properties = s.get('properties', {})
        if properties.get('title') == sheet_name:
            sheet_id = properties.get('sheetId')
            break
    if sheet_id is None:
        print(f"Impossible to find id for sheet {sheet_name}")
        return
    
    requests_body = []
    for row_index in rows_to_delete:
        requests_body.append({
            "deleteDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": row_index - 1,
                    "endIndex": row_index
                }
            }
        })
    
    body = {"requests": requests_body}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    print(f"{len(rows_to_delete)} rows deleted")

if __name__ == "__main__":

    SPREADSHEET_ID = "1EMbc_r7HHA6PoUG2f9SZV7nlAZ3oFhxjum69mr3xkpw"
    SHEET_NAME = "Feuille 1"
    DATE_COLUMN = "COLLECTED AT"
    DAYS_THRESHOLD = 60
    CREDENTIALS_JSON = "credentials.json"
    
    delete_old_rows(SPREADSHEET_ID, SHEET_NAME, DATE_COLUMN, DAYS_THRESHOLD, CREDENTIALS_JSON)