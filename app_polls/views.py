from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse

from .models import Question, Choice

# Create your views here.
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  template = loader.get_template('app_polls/index.html')
  context = {'latest_question_list': latest_question_list,}

  return render(request, 'app_polls/index.html', context)

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)

  return render(request, 'app_polls/detail.html', {'question': question})

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'app_polls/results.html', {'question': question})

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

