from app import mongo
from bson.objectid import ObjectId


class Notification():
    def __init__(self, subject, message, notification_type, action,
                 users=None, event_id=None, group_id=None, _id=None):
        self._id = _id
        self.subject = subject
        self.message = message
        self.notification_type = notification_type
        self.action = action
        self.users = users if isinstance(users, list) else []
        self.event_id = event_id
        self.group_id = group_id

    def get_notification_info(self):
        info = {'subject': self.subject,
                'message': self.message,
                'notification_type': self.notification_type,
                'action': self.action,
                'users': self.users,
                'event_id': self.event_id,
                'group_id': self.group_id}
        return info

    @staticmethod
    def get_notifications_for_user(user_id):
        events = mongo.db.notifications.find({"users": ObjectId(user_id)})
        return events
