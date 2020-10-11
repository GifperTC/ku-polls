from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Initialize amount of extra choice after the default choices."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """CLass for details of question section in admin page."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': [
         'pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date']


admin.site.register(Question, QuestionAdmin)
