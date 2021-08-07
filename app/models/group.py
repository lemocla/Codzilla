from app import mongo
from bson.objectid import ObjectId


class Group():
    def __init__(self, group_name, group_city, group_country,
                 group_description, img_url, group_admin, events=None,
                 group_members=None, _id=None):
        self._id = _id
        self.group_name = group_name
        self.group_city = group_city
        self.group_country = group_country
        self.group_description = group_description
        self.img_url = img_url
        self.events = events if isinstance(events, list) else []
        self.group_members = group_members if isinstance(group_members,
                                                         list) else []
        self.group_admin = group_admin if isinstance(
                           group_admin, list) else []

    def get_group_info(self):
        info = {'group_name': self.group_name,
                'group_city': self.group_city,
                'img_url': self.img_url,
                'group_country': self.group_country,
                'group_description': self.group_description,
                'events': self.events,
                'group_members': self.group_members,
                'group_admin': self.group_admin}
        return info

    def insert_into_database(self):
        try:
            new_id = mongo.db.groups.insert_one(self.get_group_info())
            return new_id
        except Exception as e:
            print(e)

    @staticmethod
    def update_group(group_id, info):
        try:
            mongo.db.groups.update_one({"_id": ObjectId(group_id)},
                                       {"$set": info})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_one_group(group_id):
        """
        Delete record
        """
        mongo.db.groups.delete_one({"_id": ObjectId(group_id)})

    @staticmethod
    def find_one_group(group_id):
        group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})
        return group

    @staticmethod
    def find_all_groups():
        groups = list(mongo.db.groups.find())
        return groups

    @staticmethod
    def search_groups(query):
        results = mongo.db.groups.find({"$text": {"$search": query}})
        return results

    @staticmethod
    def find_groups_by_id(col):
        groups = mongo.db.groups.find({"_id": {"$in": col}})
        return groups

    @staticmethod
    def add_to_list(group_id, field, value):
        """
        Update record
        """
        try:
            mongo.db.groups.update_one({"_id": ObjectId(group_id)},
                                       {"$push": {field: ObjectId(value)}})
        except Exception as e:
            print(e)

    @staticmethod
    def remove_from_list(group_id, field, value):
        try:
            print(f"should pull {value} from {field} in {group_id}")
            mongo.db.groups.update_one({"_id": ObjectId(group_id)},
                                       {"$pull": {field: ObjectId(value)}})
        except Exception as e:
            print(e)

    @staticmethod
    def find_group_by_name(group_name):
        result = mongo.db.groups.find_one({"group_name": group_name})
        return result
