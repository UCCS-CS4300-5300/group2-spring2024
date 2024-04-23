from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from ..models import Task
from zoneinfo import ZoneInfo
from google_auth_oauthlib.flow import Flow
from django.conf import settings

class GoogleCalendarAPI:
    def __init__(self, credentials_path='credentials/credentials.json', scopes=None, redirect_uri=None):
        self.credentials_path = credentials_path
        self.scopes = scopes or ['https://www.googleapis.com/auth/calendar.readonly']
        self.redirect_uri = redirect_uri

    def get_authorization_url(self):
        flow = Flow.from_client_secrets_file(self.credentials_path, scopes=self.scopes)
        flow.redirect_uri = self.redirect_uri
        authorization_url, state = flow.authorization_url(prompt='consent')
        return authorization_url

    def exchange_code(self, code):
        flow = Flow.from_client_secrets_file(self.credentials_path, scopes=self.scopes, state=state)
        flow.redirect_uri = self.redirect_uri
        flow.fetch_token(code=code)
        return flow.credentials

    def authenticate_google_calendar(self):
        creds = Credentials.from_authorized_user_file(self.credentials_path, scopes=['https://www.googleapis.com/auth/calendar.readonly'])
        service = build('calendar', 'v3', credentials=creds)
        return service

    def fetch_events(self, max_results=10):
        now = datetime.now(ZoneInfo("UTC")).isoformat()
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def convert_events_to_tasks(self, events):
        for event in events:
            end = event.get('end').get('dateTime')
            if end:
                end_datetime = datetime.datetime.fromisoformat(end[:-1])
                deadline_date = end_datetime.date()
                deadline_time = end_datetime.time()
                task = Task(name=event.get('summary'), description="Imported from Google Calendar",
                            deadlineDay=deadline_date, deadlineTime=deadline_time)
                task.save()

    def import_events_as_tasks(self):
        events = self.fetch_events()
        self.convert_events_to_tasks(events)
        return "Import successful"

# View function to trigger event import
def import_google_calendar_events(request):
    google_calendar = GoogleCalendarAPI('path_to_credentials/token.json')
    message = google_calendar.import_events_as_tasks()
    return HttpResponse(message)