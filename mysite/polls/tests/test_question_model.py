import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    """A unittest class for question models functions and attributes."""

    def test_is_published(self):
        """
        is_published() returns True for questions whose pub_date is before
        or is the current time.
        """
        time = timezone.now()
        recent_question = Question(
            pub_date=time, end_date=time + datetime.timedelta(hours=10))
        self.assertIs(True, recent_question.is_published())

    def test_is_published_many_cases(self):
        """
        is_published() returns True for questions whose pub_date is already passed.
        """
        time = timezone.now()

        question1 = Question(pub_date=time-datetime.timedelta(hours=10),
                             end_date=time+datetime.timedelta(hours=10))
        self.assertIs(True, question1.is_published())

        question2 = Question(pub_date=time, end_date=time++
                             datetime.timedelta(hours=10))
        self.assertIs(True, question2.is_published())

        question3 = Question(pub_date=time+datetime.timedelta(hours=10),
                             end_date=time+datetime.timedelta(hours=20))
        self.assertIs(False, question3.is_published())

        question4 = Question(
            pub_date=time+datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question4.is_published())

    def test_can_vote(self):
        """
        can_vote() returns True for questions whose pub_date is already passed 
        current time and end_date is in the future.
        """
        time = timezone.now()

        question1 = Question(pub_date=time, end_date=time)
        self.assertIs(False, question1.can_vote())

        question2 = Question(pub_date=time-datetime.timedelta(hours=10),
                             end_date=time+datetime.timedelta(hours=10))
        self.assertIs(True, question2.can_vote())

        question3 = Question(pub_date=time+datetime.timedelta(hours=10),
                             end_date=time+datetime.timedelta(hours=20))
        self.assertIs(False, question3.can_vote())

        question4 = Question(
            pub_date=time+datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question4.can_vote())

        question5 = Question(pub_date=time, end_date=time +
                             datetime.timedelta(hours=10))
        self.assertIs(True, question5.can_vote())

        question6 = Question(
            pub_date=time-datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question6.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time + datetime.timedelta(hours=10))