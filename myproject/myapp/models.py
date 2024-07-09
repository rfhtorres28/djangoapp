from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime

# Create your models here.
class UserDetails(AbstractBaseUser):
    
    class Meta:
        db_table = 'UserDetails'
    

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    image_file = models.CharField(max_length=255, null=False, default='default.png')
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    instagram_link = models.CharField(max_length=255)
    facebook_link = models.CharField(max_length=255)
    bio = models.TextField(null=True, default='')
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class UserResult(models.Model):

    class Meta:
        db_table = 'UserResult'

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    subject = models.CharField(max_length=20)
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    session_id = models.CharField(max_length=50)
    score_percentage = models.CharField(max_length=5, blank=True, null=True)
    no_correct_answer = models.CharField(max_length=5, blank=True, null=True)
    posted_time = models.DateTimeField(default=timezone.now)
    latest_login = models.DateTimeField(default=timezone.now, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    difference = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255)

    @property
    def time_difference(self):
        if self.latest_login and self.posted_time:
            return self.latest_login - self.posted_time
        return None
    
    
class UserPost(models.Model):

    class Meta:
        db_table = 'UserPost'

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    post = models.TextField()
    username = models.CharField(max_length=255)
    session_id = models.CharField(max_length=50)
    posted_time = models.DateTimeField(default=timezone.now)
    latest_login = models.DateTimeField(default=timezone.now, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    difference = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)

    @property
    def time_difference(self):
        if self.latest_login:
            return self.latest_login - self.posted_time
        return None


class ElecsQuestions(models.Model):

    class Meta:
        db_table = 'elecsquestions'

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)


class ElecsOptions(models.Model):
    id = models.AutoField(primary_key=True)
    question_no = models.ForeignKey(ElecsQuestions, on_delete=models.CASCADE, related_name='options', null=False) # Automatically relates the elecsquestion.id (primary key of ElecsQuestions Table) as its foreign key
    letter = models.CharField(max_length=1, null=False)
    content = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"Options('{self.letter}', '{self.content}', '{self.is_correct}')"
    
    class Meta:
        db_table = 'elecsoptions'
    

class CommsQuestions(models.Model):

    class Meta:
        db_table = 'commsquestions'

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)


class CommsOptions(models.Model):
    id = models.AutoField(primary_key=True)
    question_no = models.ForeignKey(CommsQuestions, on_delete=models.CASCADE, related_name='options', null=False) # Automatically relates the commsquestion.id (primary key of CommsQuestions Table) as its foreign key
    letter = models.CharField(max_length=1, null=False)
    content = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"Options('{self.letter}', '{self.content}', '{self.is_correct}')"
    
    class Meta:
        db_table = 'commsoptions'


class MathQuestions(models.Model):

    class Meta:
        db_table = 'mathquestions'

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)


class MathOptions(models.Model):
    id = models.AutoField(primary_key=True)
    question_no = models.ForeignKey(MathQuestions, on_delete=models.CASCADE, related_name='options', null=False) # Automatically relates the commsquestion.id (primary key of CommsQuestions Table) as its foreign key
    letter = models.CharField(max_length=1, null=False)
    content = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"Options('{self.letter}', '{self.content}', '{self.is_correct}')"
    
    class Meta:
        db_table = 'mathoptions'



class GEASQuestions(models.Model):

    class Meta:
        db_table = 'geasquestions'

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)


class GEASOptions(models.Model):
    id = models.AutoField(primary_key=True)
    question_no = models.ForeignKey(GEASQuestions, on_delete=models.CASCADE, related_name='options', null=False) # Automatically relates the commsquestion.id (primary key of CommsQuestions Table) as its foreign key
    letter = models.CharField(max_length=1, null=False)
    content = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(null=False)

    def __str__(self):
        return f"Options('{self.letter}', '{self.content}', '{self.is_correct}')"
    
    class Meta:
        db_table = 'geasoptions'