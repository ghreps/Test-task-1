from django.urls import path

from .views.poll import Poll, PollsList, PollCommit, PollResults
from .views.question import Question

app_name = "polls"

urlpatterns = [
    path('polls/list/', PollsList.as_view()),
    path('polls/poll/', Poll.as_view()),
    path('polls/commit/', PollCommit.as_view()),
    path('polls/results/', PollResults.as_view()),
    path('polls/question/', Question.as_view()),
]