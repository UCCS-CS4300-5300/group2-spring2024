import datetime
import os.path
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..models import *
from django.utils.dateparse import parse_datetime

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Based on Google's documentation for using Google Calendar's API with Python
class GoogleCalendar:

    def setup(request):
        creds = None
        if os.path.exists("credentials/token.json"):
            creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES, redirect_uri='http://127.0.0.1:8001/calendar/month/'
                )
                creds = flow.run_local_server(port=8001)
            # Save the credentials for the next run
            with open("credentials/token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            
            # Previous maxResults events
            past_events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMax=now,
                    maxResults=5,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            past_events = past_events_result.get("items", [])


            upcoming_events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=5,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            upcoming_events = upcoming_events_result.get("items", [])


            if not past_events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in past_events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
                task = create_task_from_event(event, start, request)
            
            for event in upcoming_events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
                task = create_task_from_event(event, start, request)

        except HttpError as error:
            print(f"An error occurred: {error}")


def create_task_from_event(event, start, request, category=None):
    user = request.user
    
    if not user.is_authenticated:
        raise Exception("User is not logged in.")

    #start = event['start'].get('datetime') or event['start'].get('date')
    print("Start datetime:", start)

    if start is None:
        raise ValueError("No start time provided in event data")

    start_datetime = parse_datetime(start)
    if start_datetime is None:
        raise ValueError("Failed to parse datetime: {}".format(start))
    
    if not start_datetime:
        # Handle all-day events
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        start_time = datetime.time(0, 0)  # Set to midnight if no time is provided

    else:
        start_date = start_datetime.date()
        start_time = start_datetime.time()

    # Create a new Task object
    new_task = Task(
        name=event.get('summary', 'No Title'),
        description=event.get('description', ''),
        deadlineDay=start_date,
        deadlineTime=start_time,
        category=category,
        duration=datetime.timedelta(hours=1),  # Default to 1 hour if not specified
        status=False,  # Assuming False means incomplete
        user=user
    )

    # Save the new Task object
    try:
        new_task.save()

    except ValueError as e:
        print("Error in creating task:", e)

    return new_task

def import_google_calendar_events(request):
    google_calendar = GoogleCalendar()
    GoogleCalendar.setup(request)
    return redirect('index')