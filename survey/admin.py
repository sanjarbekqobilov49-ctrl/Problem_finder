from django.contrib import admin
from .models import Response, Answer, IPLog


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question_number", "answer", "created_at")
    can_delete = False


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "region",
        "age",
        "ip_address",
        "created_at",
    )

    list_filter = (
        "region",
        "age",
        "created_at",
    )

    search_fields = (
        "name",
        "region",
        "ip_address",
    )

    readonly_fields = (
        "created_at",
        "ip_address",
        "user_agent",
    )

    ordering = ("-created_at",)

    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "response",
        "question_number",
        "short_answer",
        "created_at",
    )

    list_filter = (
        "question_number",
        "created_at",
    )

    search_fields = (
        "answer",
        "response__name",
        "response__region",
    )

    def short_answer(self, obj):
        if len(obj.answer) > 60:
            return obj.answer[:60] + "..."
        return obj.answer

    short_answer.short_description = "Javob"


@admin.register(IPLog)
class IPLogAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "completed_at",
    )

    search_fields = (
        "ip_address",
    )

    ordering = ("-completed_at",)