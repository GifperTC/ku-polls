from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """A class for index page view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.
        (not including those set to be published in the future)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:]


class ResultsView(generic.DetailView):
    """A class for result page view."""

    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """
    Return detail page html and redirect to index page
    if the question is out of voting period.

    Parameters:
    ----------
    request :
        object containing metadata about page's request
    question_id :
        id of that question
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def detail(request, question_id):
    """
    Return detail page html and redirect to index page
    if the question is out of voting period.

    Parameters:
    ----------
    request :
        object containing metadata about page's request
    question_id :
        id of that question

    Raise:
    ------
    Http404
        if question is not exist.
    """
    try:
        question = Question.objects.get(pk=question_id)
        if not question.can_vote():
            messages.error(request, "This poll has already ended.")
            return redirect('polls:index')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
