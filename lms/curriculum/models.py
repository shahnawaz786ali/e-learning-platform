from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from users.models import User
import os
from django.urls import reverse

# Create your models here.
class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from=name,unique=True,null=True, default=None)
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = '1. Standards'

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)

class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = '2. Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

class AISubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='AI Subject Image')
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(instance.lesson_id,instance.lesson_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id+ str('1'))
            filename =  'lesson_images/{}/{}.{}'.format(instance.lesson_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to=save_lesson_files,verbose_name="Presentations", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files,verbose_name="Notes", blank=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural='3. Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lesson_list', kwargs={'slug':self.subject.slug, 'standard':self.Standard.slug})

class AILesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    subject = models.ForeignKey(AISubject, on_delete=models.CASCADE,related_name='ai_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="AIVideo", blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural='Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lessons', kwargs={'slug':self.slug, 'subject':self.subject.slug})

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = '4. Comments'

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '5. Replies'

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
    
class CodingSubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Coding Subject Image')
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'Coding Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

class CodingLesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    subject = models.ForeignKey(AISubject, on_delete=models.CASCADE,related_name='coding_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="CodingVideo", blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural='CodingLessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:codinglessons', kwargs={'slug':self.slug, 'subject':self.subject.slug})