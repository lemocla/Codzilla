from app import mongo
from datetime import datetime
from bson.objectid import ObjectId


class Event():
    def __init__(self, event_title, event_location, event_link, date_start,
                 date_end, is_endtime, event_description, event_category,
                 event_type, img_url, max_attendees, status, created_by,
                 group=None, attendees=None, _id=None):
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
                'status': self.status,
                'created_by': self.created_by}
        return info

    def insert_into_database(self):
        try:
            new_id = mongo.db.events.insert_one(self.get_event_info())
            return new_id
        except Exception as e:
            print(e)

    @staticmethod
    def update_event(event_id, info):
        try:
            mongo.db.events.update_one({"_id": ObjectId(event_id)},
                                       {"$set": info})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_event(event_id):
        mongo.db.events.delete_one({"_id": ObjectId(event_id)})

    @staticmethod
    def find_all_active_events():
        events = list(mongo.db.events.find(
                  {"date_start": {"$gte": datetime.today()},
                   "status": "active"}).sort("date_start", 1))
        return events

    @staticmethod
    def upcoming_events():
        upcoming_events = list(mongo.db.events.find(
                          {"date_start": {"$gte": datetime.today()},
                           "status": "active"}).sort(
                           "date_start", 1).limit(6))
        return upcoming_events

    @staticmethod
    def search_events(query):
        results = mongo.db.events.find({"$text": {"$search": query}})
        return results

    @staticmethod
    def find_events_by_id(col):
        events = mongo.db.events.find({"_id": {"$in": col}})
        return events

    @staticmethod
    def find_one_event(event_id):
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        return event

    @staticmethod
    def add_to_list(user_id, field, value):
        """
        Update record
        """
        try:
            mongo.db.events.update_one({"_id": ObjectId(user_id)},
                                       {"$push": {field: ObjectId(value)}})
        except Exception as e:
            print(e)

    @staticmethod
    def remove_from_list(event_id, field, value):
        print(f"should pull {value} from {field} in {event_id}")
        try:
            mongo.db.events.update_one({"_id": ObjectId(event_id)},
                                       {"$pull": {field: ObjectId(value)}})
        except Exception as e:
            print(e)
