from app import mongo


class Group():
    def __init__(self, group_name, group_city, group_country,
                 group_description, img_url, events, group_members,
                 group_admin, _id=None):
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

    @staticmethod
    def find_all_groups():
        groups = list(mongo.db.groups.find())
        return groups

    @staticmethod
    def search_groups(query):
        results = mongo.db.groups.find({"$text": {"$search": query}})
        return results
