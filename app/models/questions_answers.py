from app import mongo
from bson.objectid import ObjectId


class Question():
    def __init__(self, question, asked_by, event_id,
                 answered, answer=None, answered_by=None, _id=None):
        self._id = _id
        self.question = question
        self.asked_by = asked_by
        self.event_id = event_id
        self.answered = answered
        self.answer = answer
        self.answered_by = answered_by

    def get_qa_info(self):
        info = {'question': self.question,
                'asked_by': self.asked_by,
                'event_id': self.event_id,
                'answered': self.answered,
                'answer': self.answer,
                'answered_by': self.answered_by}
        return info

    def insert_into_database(self):
        try:
            new_id = mongo.db.questions_answers.insert_one(self.get_qa_info())
            return new_id
        except Exception as e:
            print(e)

    @staticmethod
    def update_qa(qa_id, info):
        try:
            mongo.db.questions_answers.update_one({"_id": ObjectId(qa_id)},
                                                  {"$set": info})
        except Exception as e:
            print(e)

    @staticmethod
    def delete_one_question(qa_id):
        """
        Delete record
        """
        mongo.db.questions_answers.delete_one({"_id": ObjectId(qa_id)})

    @staticmethod
    def find_one_qa(qa_id):
        qa = mongo.db.questions_answers.find_one({"_id": ObjectId(qa_id)})
        return qa

    @staticmethod
    def find_all_questions_answers(event_id):
        questions_answers = list(mongo.db.questions_answers.find(
                                 {"event_id": ObjectId(event_id)}))
        return questions_answers
