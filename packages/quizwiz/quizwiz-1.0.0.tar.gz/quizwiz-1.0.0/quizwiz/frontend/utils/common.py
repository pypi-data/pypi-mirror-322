import json
from data.quizwiz_session import QuizwizSession
from data.quiz_status import QuizStatus

# We will REMOVE this file.
# Do NOT add content here.


class Common:
    @classmethod
    def get_method_from_label(cls):
        str_label = QuizwizSession.get().event["label"]
        multi_label = json.loads(str_label)
        if "random" in multi_label:
            method = QuizStatus.get_value(QuizStatus.READ_QUIZ_RANDOM_LABEL)
        else:
            method = QuizStatus.get_value(QuizStatus.READ_QUIZ_LABEL)
        return method


# We will REMOVE this file.
# Do NOT add content here.
