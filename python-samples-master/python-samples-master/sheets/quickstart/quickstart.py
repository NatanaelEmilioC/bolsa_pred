# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1JrVEJkhHsapIga-rrMkLMh09JrsRQdvaOHiGYHa1UFc'
SAMPLE_RANGE_NAME = 'Dolar!A:G'
#SAMPLE_RANGE_NAME = 'Petrobras!A:G'
#SAMPLE_RANGE_NAME = 'SELIC!A:I'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        with open('Dolar_8.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in values:
                try:
                    # employee_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]]) #Petrobras
                    employee_writer.writerow([row[0], row[4]]) #Dolar 
                    # employee_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]) # Selic
                except:
                    employee_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]) # Selic
        
        """
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s, %s, %s, %s, %s, ' % (row[0], row[1], row[2], row[3], row[4], row[5]))
            print(type(row))
        """
		
if __name__ == '__main__':
    main()
# [END sheets_quickstart]