from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

def home(request):
    return redirect('consent')

def consent(request):
    return render(request, 'core/consent.html')

@require_POST
def start_survey(request):
    request.session['survey_in_progress'] = True
    request.session['answers'] = {}
    request.session['current_step'] = 2
    return redirect('survey')

def thank_you(request):
    return render(request, 'core/thank_you.html')
