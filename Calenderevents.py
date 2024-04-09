class CalendarEvent:
  def __init__(self, title, start_time, end_time, location="", description=""):
      self.title = title
      self.start_time = start_time
      self.end_time = end_time
      self.location = location
      self.description = description

  def __str__(self):
      event_info = f"Title: {self.title}\n"
      event_info += f"Start Time: {self.start_time}\n"
      event_info += f"End Time: {self.end_time}\n"
      if self.location:
          event_info += f"Location: {self.location}\n"
      if self.description:
          event_info += f"Description: {self.description}\n"
      return event_info
event1 = CalendarEvent("Meeting", "2024-04-01 09:00", "2024-04-01 10:00", "Conference Room 1", "Discuss project progress")
event2 = CalendarEvent("Lunch", "2024-04-01 12:00", "2024-04-01 13:00", "Restaurant XYZ", "Meet with clients")

print(event1)
print(event2)
