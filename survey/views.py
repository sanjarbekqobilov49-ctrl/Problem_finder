import json
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages

from .models import Response, Answer, IPLog
from .questions import QUESTIONS, TOTAL_QUESTIONS
from .forms import SurveyForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_ip_limit(request):
    if not settings.IP_LIMIT_ENABLED:
        return False
    ip = get_client_ip(request)
    cooldown = timedelta(hours=settings.IP_COOLDOWN_HOURS)
    since = timezone.now() - cooldown
    return IPLog.objects.filter(ip_address=ip, completed_at__gte=since).exists()


def survey_view(request):
    if not request.session.get('survey_in_progress'):
        return redirect('consent')

    step = request.session.get('current_step', 2)

    if request.GET.get('back') == '1' and step > 2:
        step -= 1
        request.session['current_step'] = step

    if step < 1 or step > TOTAL_QUESTIONS + 1:
        request.session['current_step'] = 2
        return redirect('survey')

    if step > TOTAL_QUESTIONS:
        return complete_survey(request)

    question = QUESTIONS[step - 1]
    answers = request.session.get('answers', {})

    if request.method == 'POST':
        form = SurveyForm(request.POST, question=question)
        if form.is_valid():
            save_answer_to_session(request, form, question)
            next_step = step + 1
            request.session['current_step'] = next_step
            if 'save_only' in request.POST:
                messages.success(request, 'Javob saqlandi')
                request.session['current_step'] = step
                return redirect('survey')
            return redirect('survey')
    else:
        initial = {}
        field_name = f'question_{question["number"]}'
        if field_name in answers:
            initial[field_name] = answers[field_name]
        form = SurveyForm(initial=initial, question=question)

    context = {
        'form': form,
        'question': question,
        'step': step,
        'total': TOTAL_QUESTIONS,
        'progress': int((step / TOTAL_QUESTIONS) * 100),
        'can_go_back': step > 1,
    }
    return render(request, 'survey/survey.html', context)


def save_answer_to_session(request, form, question):
    answers = request.session.get('answers', {})
    field_name = f'question_{question["number"]}'

    if question['type'] == 'checkbox':
        selected = form.cleaned_data.get(field_name, [])
        other_val = ''
        if question.get('has_other'):
            other_val = request.POST.get(f'{field_name}_other', '').strip()
            if other_val and 'Boshqa' in selected:
                selected = [x if x != 'Boshqa' else other_val for x in selected]
        answers[field_name] = selected
        if question.get('has_other'):
            answers[f'{field_name}_other'] = other_val
    elif question['type'] == 'rating':
        answers[field_name] = form.cleaned_data.get(field_name, '')
    else:
        answers[field_name] = form.cleaned_data.get(field_name, '')

    request.session['answers'] = answers
    request.session['current_step'] = question['number']


def complete_survey(request):
    answers = request.session.get('answers', {})
    if not answers:
        return redirect('consent')

    if check_ip_limit(request):
        messages.warning(request, 'Siz 24 soat ichida allaqachon so\'rovnoma to\'ldirgansiz.')
        return render(request, 'core/thank_you.html', {'already_submitted': True})

    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    response = Response.objects.create(
        name=answers.get('question_2', ''),
        region=answers.get('question_3', ''),
        age=answers.get('question_4', 0),
        ip_address=ip,
        user_agent=user_agent,
    )

    for q in QUESTIONS:
        if q['type'] == 'consent':
            continue
        field_name = f'question_{q["number"]}'
        answer_val = answers.get(field_name, '')
        if answer_val:
            if isinstance(answer_val, list):
                answer_val = json.dumps(answer_val, ensure_ascii=False)
            Answer.objects.create(
                response=response,
                question_number=q['number'],
                answer=str(answer_val),
            )

    IPLog.objects.create(ip_address=ip)

    request.session.flush()

    return redirect('thank_you')
