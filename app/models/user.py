"""
Contains the User Class for retreiving,
storing, editing, and preparing data relating
to users stored in MongDB.
"""
from app import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


class User():
    """
    Class representing a user
    """
    def __init__(self, first_name, last_name, email, password, city=None,
                 country=None, user_imgUrl=None, events_attending=None,
                 events_interest=None, events_organised=None,
                 group_following=None, group_owned=None,
                 notifications_msg=None, preferences=None,
                 profile_completed=None, event_reminder=None,
                 query_answered=None, event_update=None, new_participant=None,
                 event_question=None, new_follower=None, _id=None):
        """
        User initialisation
        """
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.city = city if isinstance(city, str) else str("")
        self.country = country if isinstance(country, str) else str("")
        self.user_imgUrl = user_imgUrl if isinstance(user_imgUrl,
                                                     str) else str("")
        self.events_attending = events_attending if isinstance(
                                events_attending, list) else []
        self.events_interest = events_interest if isinstance(
                               events_interest, list) else []
        self.events_organised = events_organised if isinstance(
                                events_organised, list) else []
        self.group_following = group_following if isinstance(
                               group_following, list) else []
        self.group_owned = group_owned if isinstance(
                           group_owned, list) else []
        self.notifications_msg = notifications_msg
        self.preferences = {preferences}
        self.event_reminder = event_reminder if isinstance(
                              events_attending, bool) else True
        self.query_answered = query_answered if isinstance(
                              query_answered, bool) else True
        self.event_update = event_update if isinstance(
                            event_update, bool) else True
        self.new_participant = new_participant if isinstance(
                               new_participant, bool) else True
        self.event_question = event_question if isinstance(
                              event_question, bool) else True
        self.new_follower = new_follower if isinstance(
                            new_follower, bool) else True
        self.profile_completed = profile_completed if isinstance(
                                 profile_completed, bool) else False

    def get_preferences(self):
        pref = {"event_reminder": self.event_reminder,
                "query_answered": self.query_answered,
                "event_update": self.event_update,
                "new_participant": self.new_participant,
                "event_question": self.event_question,
                "new_follower": self.new_follower}
        return pref

    def get_user_info(self):
        info = {"first_name": self.first_name.lower(),
                "last_name": self.last_name.lower(),
                "email": self.email.lower(),
                "password": self.password,
                "city": self.city,
                "country": self.country,
                "user_imgUrl": self.user_imgUrl,
                "events_attending": self.events_attending,
                "events_interest": self.events_interest,
                "events_organised": self.events_organised,
                "group_following": self.group_following,
                "group_owned": self.group_owned,
                "notifications_msg": self.notifications_msg,
                "preferences": self.get_preferences(),
                "profile_completed": False}
        return info

    def insert_into_database(self):
        """Writes a Book to the Database.
        Writes the output of the get_info
        method directly to the database.
        """
        try:
            mongo.db.users.insert_one(self.get_user_info())
        except Exception as e:
            print(e)

    @staticmethod
    def edit_user(user_id, info):
        """
        Update record
        """
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      {"$set": info})
        except Exception as e:
            print(e)

    @staticmethod
    def append_list(user_id, field, value):
        """
        Update record
        """
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      {"$push": {field: ObjectId(value)}})
        except Exception as e:
            print(e)

    @staticmethod
    def remove_from_list(user_id, field, value):
        print(f"should pull {value} from {field} in {user_id}")
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      {"$pull": {field: ObjectId(value)}})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_one_user(user_id):
        """
        Delete record
        """
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    def check_existing_user(email):
        """
        Find record with user in MongoDB
        """
        user = mongo.db.users.find_one({"email": email})
        return user

    @staticmethod
    def find_user_by_id(user_id):
        """
        Find record with user in MongoDB
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return user

    @staticmethod
    def get_user_id(email):
        """
        Find record with user in MongoDB
        """
        user_id = mongo.db.users.find_one({"email": email.lower()})["_id"]
        return user_id

    @staticmethod
    def find_all_users():
        users = list(mongo.db.users.find())
        return users

    @staticmethod
    def find_users_by_id(col):
        users = mongo.db.users.find({"_id": {"$in": col}})
        return users

    @staticmethod
    def find_users_by_array_element(array_field, value):
        """
        find users field - ex events_interest
        """
        users = mongo.db.users.find({array_field: ObjectId(value)})
        return users
