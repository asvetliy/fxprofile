import uuid

from django.db import models
from django.conf import settings


class QuestionRequestStatus(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'question_request_status'


class QuestionMessageStatus(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'question_message_status'


class QuestionRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.ForeignKey(QuestionRequestStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'question_requests'


class QuestionMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.ForeignKey(QuestionMessageStatus, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='text', name='text', max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(QuestionRequest, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'question_message'
