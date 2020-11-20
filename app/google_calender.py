from __future__ import print_function
import calendar
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import settings

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalender():
    def __init__(self):
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

        self.service = build('calendar', 'v3', credentials=creds)

    def get_events(self):
        """Shows basic usage of the Google Calendar API.
        Get the start and name of a day events on the user's calendar.
        """

        # Call the Calendar API
        day_from = datetime.datetime.now().strftime('%Y/%m/%d') + " " + "00:00:00"
        day_to = datetime.datetime.now().strftime('%Y/%m/%d') + " " + "23:59:59"
        day_from = datetime.datetime.strptime(day_from, '%Y/%m/%d %H:%M:%S').isoformat() + 'Z' # 'Z' indicates UTC time
        day_to = datetime.datetime.strptime(day_to, '%Y/%m/%d %H:%M:%S').isoformat() + 'Z'
        events_result = self.service.events().list(calendarId=settings.calendar_Id, 
                                            timeMin=day_from,
                                            timeMax=day_to,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        responce = {}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = datetime.datetime.strftime('%Y/%m/%d %H%M', start)
            event_data = {"start": start, "summary": event["summary"]}
            responce.update(event_data)
        
        return responce


if __name__ == '__main__':
    calender = GoogleCalender()
    result = calender.calender_list()
    print(result)