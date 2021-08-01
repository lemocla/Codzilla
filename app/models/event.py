from app import mongo
from datetime import datetime


class Event():
    def __init__(self, event_title, event_location, event_link, date_start,
                 date_end, is_endtime, event_description, event_category,
                 event_type, img_url, group, max_attendees, attendees, status,
                 created_by, _id=None):
        self._id = _id
        self.event_title = event_title
        self.event_location = event_location
        self.event_link = event_link
        self.date_start = date_start
        self.is_endtime = is_endtime
        self.date_end = date_end
        self.event_description = event_description
        self.event_category = event_category
        self.event_type = event_type
        self.img_url = img_url
        self.group = group
        self.attendees = attendees if isinstance(attendees, list) else []
        self.max_attendees = max_attendees
        self.status = status
        self.created_by = created_by

    @staticmethod
    def find_all_events():
        events = list(mongo.db.events.find(
                  {"date_start": {"$gte": datetime.today()}}).sort(
                  "date_start", 1))
        return events

    @staticmethod
    def search_events(query):
        results = mongo.db.events.find({"$text": {"$search": query}})
        return results
