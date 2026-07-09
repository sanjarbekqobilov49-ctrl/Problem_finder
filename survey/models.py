from django.db import models

class Response(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ism")
    region = models.CharField(max_length=50, verbose_name="Viloyat")
    age = models.IntegerField(verbose_name="Yosh")
    ip_address = models.GenericIPAddressField(verbose_name="IP manzil")
    user_agent = models.TextField(blank=True, verbose_name="Qurilma")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Respondent"
        verbose_name_plural = "Respondentlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name or 'Anonim'} ({self.region}, {self.age} yosh)"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers', verbose_name="Respondent")
    question_number = models.IntegerField(verbose_name="Savol raqami")
    answer = models.TextField(verbose_name="Javob")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Saqlangan vaqt")

    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"
        ordering = ['question_number']

    def __str__(self):
        return f"Savol {self.question_number}: {self.answer[:50]}"


class IPLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP manzil")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Tugatilgan vaqt")

    class Meta:
        verbose_name = "IP log"
        verbose_name_plural = "IP loglari"

    def __str__(self):
        return f"{self.ip_address} - {self.completed_at}"
