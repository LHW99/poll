from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
  template_name = 'app_polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    # returns last 5 published questions
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'app_polls/detail.html'

  def get_queryset(self):
    # excludes any questions that aren't published yet
    return Questions.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'app_polls/results.html'

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    # request.POST lets you access submitted data by keyname
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'app_polls/detail.html', {'question':question, 'error_message': "You didn't select a choice."})
  else: 
    selected_choice.votes += 1
    selected_choice.save()
    # always use HttpResponseRedirect after POST data to prevent double post
    return HttpResponseRedirect(reverse('app_polls:results', args=(question.id,)))

