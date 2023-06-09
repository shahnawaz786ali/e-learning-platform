# Generated by Django 3.2.17 on 2023-03-29 05:09

import autoslug.fields
import curriculum.models
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
            name='AISubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to=curriculum.models.save_subject_image, verbose_name='AI Subject Image')),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='CodingSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to=curriculum.models.save_subject_image, verbose_name='Coding Subject Image')),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Coding Subjects',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comm_name', models.CharField(blank=True, max_length=100)),
                ('body', models.TextField(max_length=500)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '4. Comments',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from=models.CharField(max_length=100, unique=True), unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': '1. Standards',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to=curriculum.models.save_subject_image, verbose_name='Subject Image')),
                ('description', models.TextField(blank=True, max_length=500)),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='curriculum.standard')),
            ],
            options={
                'verbose_name_plural': '2. Subjects',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_body', models.TextField(max_length=500)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='curriculum.comment')),
            ],
            options={
                'verbose_name_plural': '5. Replies',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=250)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Chapter no.')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=curriculum.models.save_lesson_files, verbose_name='Video')),
                ('ppt', models.FileField(blank=True, upload_to=curriculum.models.save_lesson_files, verbose_name='Presentations')),
                ('Notes', models.FileField(blank=True, upload_to=curriculum.models.save_lesson_files, verbose_name='Notes')),
                ('Standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.standard')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='curriculum.subject')),
            ],
            options={
                'verbose_name_plural': '3. Lessons',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='lesson_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='curriculum.lesson'),
        ),
        migrations.CreateModel(
            name='CodingLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Chapter no.')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=curriculum.models.save_lesson_files, verbose_name='CodingVideo')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coding_lessons', to='curriculum.aisubject')),
            ],
            options={
                'verbose_name_plural': 'CodingLessons',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='AILesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Chapter no.')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=curriculum.models.save_lesson_files, verbose_name='AIVideo')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_lessons', to='curriculum.aisubject')),
            ],
            options={
                'verbose_name_plural': 'Lessons',
                'ordering': ['position'],
            },
        ),
    ]
