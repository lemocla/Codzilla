from app import mongo
from bson.objectid import ObjectId
from app.models.user import User
from app.models.group import Group


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
        notification = mongo.db.notifications.find({"users": ObjectId(user_id)})
        return notification

    @staticmethod
    def find_one_notification(notification_id):
        notification = mongo.db.notifications.find_one({"_id": ObjectId(notification_id)})
        return notification

    @staticmethod
    def insert_notification(col):
        try:
            mongo.db.notifications.insert_one(col)
        except Exception as e:
            print(e)

    @staticmethod
    def remove_one_notification(notification_id, user_id):
        print(f"should pull {user_id} from users in {notification_id}")
        try:
            mongo.db.notifications.update_one({"_id": ObjectId(notification_id)},
                                              {"$pull": {"users": ObjectId(user_id)}})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_notification(notification_id):
        mongo.db.notifications.delete_one({"_id": ObjectId(notification_id)})

    @staticmethod
    def set_col_new_follower(user_id, group_id, users):
        follower = User.find_user_by_id(user_id)
        group = Group.find_one_group(group_id)

        col = {'subject': 'You have a new follower',
               'message': (f'{follower["first_name"]} {follower["last_name"]} '
                           f'started following your group '
                           f'{group["group_name"]}'),
               'notification_type': "new follower",
               'action': 'view group',
               'users': users,
               'group_id': ObjectId(group_id)}
        return col
