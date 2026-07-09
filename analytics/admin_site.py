from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html
from datetime import timedelta
import json
from survey.models import Response, Answer, IPLog


class CustomAdminSite(AdminSite):
    site_header = 'Problem Finder Admin'
    site_title = 'Problem Finder Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('respondent/<int:pk>/', self.admin_view(self.respondent_detail), name='respondent_detail'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        month_start = today_start.replace(day=1)

        total = Response.objects.count()
        today_count = Response.objects.filter(created_at__gte=today_start).count()
        week_count = Response.objects.filter(created_at__gte=week_start).count()
        month_count = Response.objects.filter(created_at__gte=month_start).count()

        ages = list(Response.objects.values_list('age', flat=True))
        avg_age = round(sum(ages) / len(ages), 1) if ages else 0

        regions_qs = Response.objects.values('region').annotate(count=Count('id')).order_by('-count')
        regions_list = list(regions_qs)
        top_region = regions_list[0] if regions_list else None

        last_response = Response.objects.order_by('-created_at').first()
        last_response_time = ''
        if last_response:
            local_time = timezone.localtime(last_response.created_at)
            last_response_time = local_time.strftime('%H:%M')

        answers = Answer.objects.filter(question_number=5)
        problem_counts = {}
        for ans in answers:
            try:
                items = json.loads(ans.answer)
                if isinstance(items, list):
                    for item in items:
                        problem_counts[item] = problem_counts.get(item, 0) + 1
            except (json.JSONDecodeError, TypeError):
                pass
        top_problems = sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        app_answers = Answer.objects.filter(question_number=11)
        app_counts = {}
        for ans in app_answers:
            try:
                items = json.loads(ans.answer)
                if isinstance(items, list):
                    for item in items:
                        app_counts[item] = app_counts.get(item, 0) + 1
            except (json.JSONDecodeError, TypeError):
                pass
        top_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        age_distribution = {
            '18-25': Response.objects.filter(age__gte=18, age__lte=25).count(),
            '26-35': Response.objects.filter(age__gte=26, age__lte=35).count(),
            '36-45': Response.objects.filter(age__gte=36, age__lte=45).count(),
            '46+': Response.objects.filter(age__gte=46).count(),
        }

        daily_data = []
        for i in range(6, -1, -1):
            day = today_start - timedelta(days=i)
            next_day = day + timedelta(days=1)
            count = Response.objects.filter(created_at__gte=day, created_at__lt=next_day).count()
            daily_data.append({'date': day.strftime('%d.%m'), 'count': count})

        chart_labels = [r['region'] for r in regions_list]
        chart_data = [r['count'] for r in regions_list]

        context = {
            'total_respondents': total,
            'today_respondents': today_count,
            'week_respondents': week_count,
            'month_respondents': month_count,
            'avg_age': avg_age,
            'top_region': top_region['region'] if top_region else '-',
            'top_region_count': top_region['count'] if top_region else 0,
            'last_response_time': last_response_time,
            'regions_labels': json.dumps(chart_labels),
            'regions_data': json.dumps(chart_data),
            'top_problems': top_problems,
            'top_problems_labels': json.dumps([p[0] for p in top_problems]),
            'top_problems_data': json.dumps([p[1] for p in top_problems]),
            'top_apps_labels': json.dumps([a[0] for a in top_apps]),
            'top_apps_data': json.dumps([a[1] for a in top_apps]),
            'age_labels': json.dumps(list(age_distribution.keys())),
            'age_data': json.dumps(list(age_distribution.values())),
            'daily_labels': json.dumps([d['date'] for d in daily_data]),
            'daily_counts': json.dumps([d['count'] for d in daily_data]),
        }
        return render(request, 'analytics/dashboard.html', context)

    def respondent_detail(self, request, pk):
        respondent = get_object_or_404(Response, pk=pk)
        answers = Answer.objects.filter(response=respondent).order_by('question_number')
        from survey.questions import QUESTIONS
        q_dict = {q['number']: q for q in QUESTIONS}
        for answer in answers:
            q = q_dict.get(answer.question_number)
            answer.question_title = q['title'] if q else ''
        return render(request, 'analytics/respondent_detail.html', {
            'respondent': respondent,
            'answers': answers,
            'questions': q_dict,
        })


custom_admin_site = CustomAdminSite(name='custom_admin')


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question_number', 'answer', 'created_at']
    can_delete = False
    max_num = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Response, site=custom_admin_site)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'region', 'ip_address', 'created_at']
    list_filter = ['region', 'created_at', 'age']
    search_fields = ['name', 'region', 'ip_address']
    readonly_fields = ['ip_address', 'user_agent', 'created_at']
    inlines = [AnswerInline]
    date_hierarchy = 'created_at'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Answer, site=custom_admin_site)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'response_link', 'question_number', 'answer_preview', 'created_at']
    list_filter = ['question_number', 'created_at']
    search_fields = ['answer']

    def response_link(self, obj):
        url = reverse('custom_admin:respondent_detail', args=[obj.response_id])
        return format_html('<a href="{}">{}</a>', url, f"#{obj.response_id}")
    response_link.short_description = "Respondent"

    def answer_preview(self, obj):
        return obj.answer[:100]
    answer_preview.short_description = "Javob"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(IPLog, site=custom_admin_site)
class IPLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['ip_address']
    readonly_fields = ['ip_address', 'completed_at']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
