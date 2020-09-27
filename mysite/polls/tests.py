import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time, end_date=time + datetime.timedelta(hours=10))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time, end_date=time + datetime.timedelta(hours=10))
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=time + datetime.timedelta(hours=10))
        self.assertIs(recent_question.was_published_recently(), True)    

    def test_is_published(self):
        """
        is_published() returns True for questions whose pub_date
        is before or is the current time.
        """
        time = timezone.now()
        recent_question = Question(pub_date=time, end_date=time + datetime.timedelta(hours=10))
        self.assertIs(True, recent_question.is_published())

    def test_is_published_many_cases(self):
        """
        is_published() returns True for questions whose pub_date is already passed.
        """
        time = timezone.now()

        question1 = Question(pub_date=time-datetime.timedelta(hours=10), end_date=time+datetime.timedelta(hours=10))
        self.assertIs(True, question1.is_published())

        question2 = Question(pub_date=time, end_date=time++ datetime.timedelta(hours=10))
        self.assertIs(True, question2.is_published())

        question3 = Question(pub_date=time+datetime.timedelta(hours=10), end_date=time+datetime.timedelta(hours=20))
        self.assertIs(False ,question3.is_published())

        question4 = Question(pub_date=time+datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question4.is_published())

    def test_can_vote(self):
        """
        can_vote() returns True for questions whose pub_date is already passed current time and end_date is in the future.
        """
        time = timezone.now()

        question1 = Question(pub_date=time, end_date=time)
        self.assertIs(False, question1.can_vote())

        question2 = Question(pub_date=time-datetime.timedelta(hours=10), end_date=time+datetime.timedelta(hours=10))
        self.assertIs(True, question2.can_vote())

        question3 = Question(pub_date=time+datetime.timedelta(hours=10), end_date=time+datetime.timedelta(hours=20))
        self.assertIs(False, question3.can_vote())

        question4 = Question(pub_date=time+datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question4.can_vote())

        question5 = Question(pub_date=time, end_date=time+datetime.timedelta(hours=10))
        self.assertIs(True, question5.can_vote())

        question6 = Question(pub_date=time-datetime.timedelta(hours=10), end_date=time)
        self.assertIs(False, question6.can_vote())

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time + datetime.timedelta(hours=10))

class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

# เอามาใช้ได้เลย แต่เรียกไม่ได้
def create_question(q_txt, pup_d):
    q = Question(question_text=q_txt, pub_date=pup_d, end_date=(pup_d+datetime.timedelta(days=30)))
    q.save()


class QuestionIndexViewTests(TestCase):

    # def setUp(self):
    #     pass

    def test_index_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_with_just_publish_polls(self):
        create_question("1+1+?", timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 1+1+?>'])

    def test_index_with_published_polls(self):
        create_question("1+1+?", timezone.now()-datetime.timedelta(days=2))
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 1+1+?>'])

    def test_index_with_no_published_polls(self):
        create_question("1+1+?", timezone.now()+datetime.timedelta(days=2))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_with_multi_published_polls(self):
        create_question("1+1+?", timezone.now())
        create_question("2+2+?", timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 2+2+?>', '<Question: 1+1+?>'])

    def test_index_with_published_and_not_published_polls(self):
        create_question("1+1+?", timezone.now()+datetime.timedelta(days=3))
        create_question("2+2+?", timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 2+2+?>'])


# เอามาใช้ได้
def create_and_return_question(q_txt, pup_d):
    q = Question.objects.create(question_text=q_txt, pub_date=pup_d, end_date=(pup_d+datetime.timedelta(days=30)))
    return q


class QuestionDetailViewTests(TestCase):

    def test_detail_not_have_question(self):
        response = self.client.get(reverse('polls:detail', args="1"))
        self.assertEqual(response.status_code, 404)

    def test_detail_with_published_question(self):
        q = create_and_return_question("A B C ...", timezone.now())
        response = self.client.get(reverse('polls:detail', args=(q.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, q.question_text)

    def test_detail_with_no_published_question(self):
        q = create_and_return_question("A B C ...", timezone.now()-datetime.timedelta(days=3))
        response = self.client.get(reverse('polls:detail', args=(q.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, q.question_text)

    def test_detail_with_ended_question(self):
        q = Question.objects.create(question_text="A B C ...", pub_date=(timezone.now()-datetime.timedelta(days=5)),
                                    end_date=(timezone.now()-datetime.timedelta(days=3)))
        response = self.client.get(reverse('polls:detail', args=(q.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('polls:index'))

    def test_post_in(self):
        q = create_and_return_question("A B C ...", timezone.now())
        q.id = 1
        c1 = Choice.objects.create(question=q, choice_text='D')
        c1 = Choice.objects.create(question=q, choice_text='E')
        c1 = Choice.objects.create(question=q, choice_text='F')
        response = self.client.post('/polls/1/', {'choice': 2})
        # self.assertRedirects(response, 'polls/1/results/')
        # self.assertTemplateUsed(response, 'polls/results.html')
        self.assertTemplateUsed(response, 'polls/detail.html')
        self.assertEqual(response.status_code, 200)


class UrlTests(TestCase):

    def setUp(self):
        self.q = create_and_return_question("A B C ...", timezone.now())
        self.q.id = 1

    def test_index_page_with_blank(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'polls/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.q.question_text)
        # self.assertRedirects(response, '/polls/')
        # self.assertRedirects(response, reverse('polls:index'))

    def test_index_page_with_polls(self):
        response = self.client.get('/polls/')
        self.assertTemplateUsed(response, 'polls/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.q.question_text)

    def test_detail_page_with_polls(self):
        response = self.client.get('/polls/1/')
        self.assertTemplateUsed(response, 'polls/detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.q.question_text)

    def test_results_page_with_polls(self):
        response = self.client.get('/polls/1/results/')
        self.assertTemplateUsed(response, 'polls/results.html')
        self.assertEqual(response.status_code, 200)