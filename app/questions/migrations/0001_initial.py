# Generated by Django 3.1.5 on 2021-03-23 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionMessageStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'question_message_status',
            },
        ),
        migrations.CreateModel(
            name='QuestionRequestStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'question_request_status',
            },
        ),
        migrations.CreateModel(
            name='QuestionRequest',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.questionrequeststatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question_requests',
            },
        ),
        migrations.CreateModel(
            name='QuestionMessage',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, verbose_name='id')),
                ('text', models.TextField(max_length=300, verbose_name='text')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.questionrequest')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.questionmessagestatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question_message',
            },
        ),
    ]
