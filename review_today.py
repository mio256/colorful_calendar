import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

ColorDict = {
    '1': 'ラベンダー',
    '2': 'セージ',
    '3': 'ブドウ',
    '4': 'フラミンゴ',
    '5': 'バナナ',
    '6': 'ミカン',
    '7': 'ピーコック',
    '8': 'グラファイト',
    '9': 'ブルーベリー',
    '10': 'バジル',
    '11': 'トマト',
}

TagDict = {
    '1': 'work',
    '2': 'study',
    '3': 'work',
    '4': 'chill',
    '5': 'study',
    '6': 'meal',
    '7': 'other',
    '8': 'program',
    '9': 'business',
    '10': 'study',
    '11': 'life',
}


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    daytime = datetime.datetime.now()
    d = get_dict(daytime, creds)
    # print(daytime)
    print('時間配分')
    print('| item     | hour |')
    print('| -------- | ---- |')
    for i in d:
        print('| {:<8} | {:.1f}h |'.format(i,d[i]))


def get_dict(daytime, creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        TimeDict = {
            'work': 0,
            'study': 0,
            'chill': 0,
            'program': 0,
            'business': 0,
            'life': 0
        }

        # Call the Calendar API
        events_result = service.events().list(
            calendarId='primary',
            timeMin=daytime.replace(hour=0, minute=0).isoformat() + '+09:00',
            timeMax=daytime.replace(hour=23, minute=59).isoformat() + '+09:00',
            maxResults=50,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            if 'colorId' in event:
                color = event['colorId']
            else:
                color = '7'
            # print(start, end, ColorDict[color], event['summary'])
            time = datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)
            # print(time, TagDict[color], event['summary'])
            if TagDict[color] in TimeDict:
                TimeDict[TagDict[color]] = TimeDict[TagDict[color]] + (time.seconds / 3600)

        return TimeDict

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()