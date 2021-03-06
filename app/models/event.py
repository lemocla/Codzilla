from app import mongo
from datetime import datetime
from bson.objectid import ObjectId


class Event():
    """
    Class representing an event
    """
    def __init__(self, event_title, event_location, event_link, date_start,
                 date_end, is_endtime, event_description, event_category,
                 event_type, img_url, max_attendees, status, created_by,
                 group=None, attendees=None, questions_answers=None, _id=None):
        self._id = _id
        self.event_title = event_title
        self.event_location = event_location if isinstance(
                              event_location, str) else ""
        self.event_link = event_link if isinstance(event_link, str) else ""
        self.date_start = date_start
        self.is_endtime = is_endtime
        self.date_end = date_end
        self.event_description = event_description
        self.event_category = event_category
        self.event_type = event_type
        self.img_url = img_url if isinstance(img_url, str) else ""
        self.group = group
        self.attendees = attendees if isinstance(attendees, list) else []
        self.questions_answers = questions_answers if isinstance(
                                 questions_answers, list) else []
        self.max_attendees = max_attendees if isinstance(
                             max_attendees, str) else ""
        self.status = status
        self.created_by = created_by

    def get_event_info(self):
        info = {'event_title': self.event_title,
                'event_location': self.event_location,
                'event_link': self.event_link,
                'date_start': self.date_start,
                'is_endtime': self.is_endtime,
                'date_end': self.date_end,
                'event_description': self.event_description,
                'event_category': self.event_category,
                'event_type': self.event_type,
                'img_url': self.img_url,
                'group': self.group,
                'attendees': self.attendees,
                'max_attendees': self.max_attendees,
                'questions_answers': self.questions_answers,
                'status': self.status,
                'created_by': self.created_by}
        return info

    def insert_into_database(self):
        """
        Add an event in MongoDB and return new event id
        """
        new_id = mongo.db.events.insert_one(self.get_event_info())
        return new_id

    @staticmethod
    def update_event(event_id, info):
        """
        Update one event in MongoDB
        """
        mongo.db.events.update_one({"_id": ObjectId(event_id)},
                                   {"$set": info})

    @staticmethod
    def delete_event(event_id):
        """
        Delete one event in MongoDB
        """
        mongo.db.events.delete_one({"_id": ObjectId(event_id)})

    @staticmethod
    def find_all_active_events():
        """
        Find all active events in MongoDB
        Search by status, start date greated than today
        Sort by date
        """
        events = list(mongo.db.events.find(
                  {"date_start": {"$gte": datetime.today()},
                   "status": "active"}).sort("date_start", 1))
        return events

    @staticmethod
    def upcoming_events():
        """
        Find first 6 active events
        Search by status, start date greated than today
        Sort by date
        """
        upcoming_events = list(mongo.db.events.find(
                          {"date_start": {"$gte": datetime.today()},
                           "status": "active"}).sort(
                           "date_start", 1).limit(6))
        return upcoming_events

    @staticmethod
    def search_events(query):
        """
        Search index for events in MongoDB by query
        """
        results = mongo.db.events.find({
                 "date_start": {"$gte": datetime.today()},
                 "$text": {"$search": query}})
        return results

    @staticmethod
    def find_events_by_dates(isos, isoe):
        """
        Find events within date range in MongoDB
        """
        events = mongo.db.events.find(
                 {"date_start": {'$gte': isos, '$lte': isoe}})
        return events

    @staticmethod
    def find_events_by_id(col):
        """
        Find events matching an array of Id
        """
        events = mongo.db.events.find({"_id": {"$in": col}})
        return events

    @staticmethod
    def find_one_event(event_id):
        """
        Find one event in MongoDB and return object
        """
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        return event

    @staticmethod
    def add_to_list(event_id, field, value):
        """
        Add value to any array in events in MongoDB
        """
        mongo.db.events.update_one({"_id": ObjectId(event_id)},
                                   {"$push": {field: ObjectId(value)}})

    @staticmethod
    def remove_from_list(event_id, field, value):
        """
        Remove value from any array in events in MongoDB
        """
        mongo.db.events.update_one({"_id": ObjectId(event_id)},
                                   {"$pull": {field: ObjectId(value)}})
