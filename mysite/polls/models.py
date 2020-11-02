import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question model with publication and ending date for voting."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')
        
    def is_published(self):
        """Return True if the publish date of the questionis before or equals current time."""
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """Return True if the ending date of the question is after the publish date and current time."""
        return self.is_published() and timezone.now() < self.end_date

    def __str__(self):
        """Return this question's text."""
        return self.question_text


class Choice(models.Model):
    """Choice model with foriegnkey of the question related to the choice and amount of votes"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return this choice's text."""
        return self.choice_text


class Vote(models.Model):
    """Vote model"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
