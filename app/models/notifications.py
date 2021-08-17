from app import mongo
from bson.objectid import ObjectId
from app.models.user import User
from app.models.group import Group
from app.models.event import Event


class Notification():
    """
    Class representing a notification
    """
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
    """
    Notification initialisation
    """
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
        """
        Retrieve and return all notifications in MongoDB
        """
        notification = mongo.db.notifications.find(
                       {"users": ObjectId(user_id)})
        return notification

    @staticmethod
    def find_one_notification(notification_id):
        """
        Fetch one notification by Id in MongoDB
        Return notification object
        """
        notification = mongo.db.notifications.find_one(
                       {"_id": ObjectId(notification_id)})
        return notification

    @staticmethod
    def insert_notification(col):
        """
        Add a notification in MongoDB
        """
        mongo.db.notifications.insert_one(col)

    @staticmethod
    def remove_one_notification(notification_id, user_id):
        """
        Remove a user from list of users in MongoDB
        """
        mongo.db.notifications.update_one(
         {"_id": ObjectId(notification_id)},
         {"$pull": {"users": ObjectId(user_id)}})

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete one notification in MongoDB
        """
        mongo.db.notifications.delete_one({"_id": ObjectId(notification_id)})

    @staticmethod
    def get_read_notification(user_id):
        """
        Check if user in list of users who read notification
        """
        read = mongo.db.notifications.find(
                {"read_by": ObjectId(user_id)})
        return read

    @staticmethod
    def add_user_to_read_by(notification_id, user_id):
        """
        Add user to list of users who read notification
        """
        mongo.db.notifications.update_one(
         {"_id": ObjectId(notification_id)},
         {"$push": {"read_by": ObjectId(user_id)}})

    @staticmethod
    def set_col_new_follower(user_id, group_id, users):
        """
        Build message for new follower notification
        """
        follower = User.find_user_by_id(user_id)
        group = Group.find_one_group(group_id)

        col = {'subject': 'You have a new follower',
               'message': (f'{follower["first_name"]} {follower["last_name"]} '
                           f'started following your group '
                           f'{group["group_name"]}.'),
               'notification_type': "new follower",
               'action': 'view group',
               'users': users,
               'group_id': ObjectId(group_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_new_participant(user_id, event_id, event_admin):
        """
        Build message for new participant notification
        """
        attendee = User.find_user_by_id(user_id)
        event = Event.find_one_event(event_id)

        col = {'subject': 'You have new participant',
               'message': (f'{attendee["first_name"]} {attendee["last_name"]} '
                           f'will attend '
                           f'{event["event_title"]}.'),
               'notification_type': "new participant",
               'action': 'view event',
               'users': [ObjectId(event_admin)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_question(user_id, event_id, event_admin):
        """
        Build message for new question notification
        """
        attendee = User.find_user_by_id(user_id)
        event = Event.find_one_event(event_id)

        col = {'subject': 'You received a question about your event',
               'message': (f'{attendee["first_name"]} {attendee["last_name"]} '
                           f'asked a question about '
                           f'{event["event_title"]}.'),
               'notification_type': "event question",
               'action': 'view question',
               'users': [ObjectId(event_admin)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_answer(user_id, event_id):
        """
        Build message for answer notification
        """
        event = Event.find_one_event(event_id)
        admin = User.find_user_by_id(event["created_by"])
        col = {'subject': (f'{admin["first_name"]} {admin["last_name"]} '
                           f'answered your question'),
               'message': (f'{admin["first_name"]} {admin["last_name"]} '
                           f'answered your question about '
                           f'{event["event_title"]}.'),
               'notification_type': "event answer",
               'action': 'view answer',
               'users': [ObjectId(user_id)],
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_cancellation(attendees, event_id):
        """
        Build message for cancellaton notification
        """
        event = Event.find_one_event(event_id)
        col = {'subject': 'Event cancellation notification',
               'message': (f'An event your attending - {event["event_title"]}'
                           f' - has been cancelled.'),
               'notification_type': "event cancellation",
               'action': '',
               'users': attendees,
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_update(attendees, event_id, field_name, field_value):
        """
        Build message for event update notification
        """
        event = Event.find_one_event(event_id)
        col = {'subject': (f"One of your event's - {field_name} - has "
                           f"been updated"),
               'message': (f'Your event - {event["event_title"]} - '
                           f'{field_name} has been moved to {field_value}.'),
               'notification_type': "event update",
               'action': 'view event',
               'users': attendees,
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def set_col_reminder(attendees, event_id):
        """
        Build message of event reminder notification
        """
        event = Event.find_one_event(event_id)
        event_title = event["event_title"]
        col = {'subject': f"Reminder: {event_title} is happening soon",
               'message': (f'Your event - {event["event_title"]} is happening'
                           f' on {event["date_start"]}'),
               'notification_type': "event reminder",
               'action': 'view event',
               'users': attendees,
               'event_id': ObjectId(event_id),
               'read_by': []}
        return col

    @staticmethod
    def already_notified(event_id, user_id):
        """
        Check if user has already had notification
        for event reminder
        """
        notified = mongo.db.notifications.find(
                   {"event_id": ObjectId(event_id),
                    "notification_type": "event reminder",
                    "users": ObjectId(user_id)})
        return notified
