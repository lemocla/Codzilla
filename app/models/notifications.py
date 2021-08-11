from app import mongo
from bson.objectid import ObjectId
from app.models.user import User
from app.models.group import Group
from app.models.event import Event


class Notification():
    def __init__(self, subject, message, notification_type, action,
                 users=None, event_id=None, group_id=None,
                 read_by=None, _id=None):
        self._id = _id
        self.subject = subject
        self.message = message
        self.notification_type = notification_type
        self.action = action
        self.users = users if isinstance(users, list) else []
        self.event_id = event_id
        self.group_id = group_id
        self.read_by = read_by if isinstance(read_by, list) else []

    def get_notification_info(self):
        info = {'subject': self.subject,
                'message': self.message,
                'notification_type': self.notification_type,
                'action': self.action,
                'users': self.users,
                'event_id': self.event_id,
                'group_id': self.group_id,
                'read_by': self.read_by}
        return info

    @staticmethod
    def get_notifications_for_user(user_id):
        notification = mongo.db.notifications.find(
                       {"users": ObjectId(user_id)})
        return notification

    @staticmethod
    def find_one_notification(notification_id):
        notification = mongo.db.notifications.find_one(
                       {"_id": ObjectId(notification_id)})
        return notification

    @staticmethod
    def insert_notification(col):
        try:
            mongo.db.notifications.insert_one(col)
        except Exception as e:
            print(e)

    @staticmethod
    def remove_one_notification(notification_id, user_id):
        print(f"should pull {user_id} from users "
              f"in {notification_id}")
        try:
            mongo.db.notifications.update_one(
             {"_id": ObjectId(notification_id)},
             {"$pull": {"users": ObjectId(user_id)}})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_notification(notification_id):
        mongo.db.notifications.delete_one({"_id": ObjectId(notification_id)})

    @staticmethod
    def get_read_notification(user_id):
        read = mongo.db.notifications.find(
                {"read_by": ObjectId(user_id)})
        print(read)
        return read

    @staticmethod
    def add_user_to_read_by(notification_id, user_id):
        try:
            mongo.db.notifications.update_one(
             {"_id": ObjectId(notification_id)},
             {"$push": {"read_by": ObjectId(user_id)}})
        except Exception as e:
            print(e)

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
               'group_id': ObjectId(group_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_new_participant(user_id, event_id, event_admin):
        attendee = User.find_user_by_id(user_id)
        event = Event.find_one_event(event_id)

        col = {'subject': 'You have new participant',
               'message': (f'{attendee["first_name"]} {attendee["last_name"]} '
                           f'will attend '
                           f'{event["event_title"]}'),
               'notification_type': "new participant",
               'action': 'view event',
               'users': [ObjectId(event_admin)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_question(user_id, event_id, event_admin):
        attendee = User.find_user_by_id(user_id)
        event = Event.find_one_event(event_id)

        col = {'subject': 'You received a question about your event',
               'message': (f'{attendee["first_name"]} {attendee["last_name"]} '
                           f'asked a question about '
                           f'{event["event_title"]}'),
               'notification_type': "event question",
               'action': 'view question',
               'users': [ObjectId(event_admin)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_answer(user_id, event_id):
        event = Event.find_one_event(event_id)
        admin = User.find_user_by_id(event["created_by"])
        print(event)
        print(admin)
        col = {'subject': (f'{admin["first_name"]} {admin["last_name"]} '
                           f'answered your question'),
               'message': (f'{admin["first_name"]} {admin["last_name"]} '
                           f'answered your question about '
                           f'{event["event_title"]}'),
               'notification_type': "event answer",
               'action': 'view answer',
               'users': [ObjectId(user_id)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_cancellation(attendees, event_id):
        event = Event.find_one_event(event_id)
        col = {'subject': 'Event cancellation notification',
               'message': (f'Your event - {event["event_title"]} - '
                           f'has been cancelled'),
               'notification_type': "event cancellation",
               'action': '',
               'users': attendees,
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_update(attendees, event_id, field_name, field_value):

        event = Event.find_one_event(event_id)
        col = {'subject': (f"One of your event's - {field_name} - has "
                           f"been updated"),
               'message': (f'Your event - {event["event_title"]} {field_name} -'
                           f' has been moved to {field_value}'),
               'notification_type': "event update",
               'action': 'view event',
               'users': attendees,
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col
